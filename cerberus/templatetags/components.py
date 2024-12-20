import re
from functools import lru_cache
from typing import Any

from django import template
from django.template import Node, NodeList, TemplateSyntaxError
from django.template.context import Context
from django.template.library import InclusionNode

from ..utils import rget

register = template.Library()

quote_regex = re.compile(r"^(\"|')(.*)(\"|')$")


@lru_cache
def unquote(value: str) -> str:
    return quote_regex.sub(r"\2", value)


@lru_cache
def quoted(value: str) -> bool:
    return quote_regex.match(value) is not None


def parse_extra_context(extra_context: list[str]) -> dict[str, Any]:
    return {unquote(key): value for key, value in (item.split("=") for item in extra_context)}


def nest_dict(d: dict) -> dict:
    result = {}
    for key, value in d.items():
        parts = key.split(".")
        current_dict = result
        for part in parts[:-1]:
            current_dict = current_dict.setdefault(part, {})
        current_dict[parts[-1]] = value
    return result


class ComponentNode(Node):
    extra_context: dict[str, Any]
    template_name: str
    slots: dict[str, NodeList]

    def __init__(self, slots: dict[str, NodeList], template_name: str, extra_context: dict[str, Any] | None = None):
        self.slots = slots
        self.extra_context = extra_context or {}
        self.template_name = template_name

    def render(self, context) -> str:
        extra_context = {}
        for key, value in self.extra_context.items():
            if quoted(value):
                extra_context[key] = unquote(value)
            else:
                extra_context[key] = rget(context, value, "")

        with context.update(extra_context):
            rendered_slots = nest_dict({f"{name}": slot.render(context) for name, slot in self.slots.items()})

        inclusion_node = InclusionNode(
            lambda c: {"slots": rendered_slots, "attributes": extra_context},
            args=[],
            kwargs={},
            takes_context=True,
            filename=self.template_name,
        )

        return inclusion_node.render(context)


class SlotNode(template.Node):
    name: str
    nodelist: NodeList
    extra_context: dict[str, Any]

    def __init__(
        self,
        name: str | None = None,
        nodelist: NodeList | None = None,
        extra_context: dict[str, Any] | None = None,
    ):
        self.name = name or ""
        self.nodelist = nodelist or NodeList()
        self.extra_context = extra_context or {}

    def render(self, context: Context) -> str:
        with context.update(self.extra_context):
            return self.nodelist.render(context)


@register.tag
def slot(parser, token) -> Node:
    # todo: this feels like it couuld be refactored better
    args = token.split_contents()
    if len(args) < 2:  # noqa: PLR2004
        raise TemplateSyntaxError(f"{args[0]} tag requires at least one argument")

    node_list = parser.parse(("endslot",))
    parser.delete_first_token()

    return SlotNode(unquote(args[1]), node_list, parse_extra_context(args[2:]))


@register.tag
def component(parser, token) -> Node:
    node_list = parser.parse(("endcomponent",))
    parser.delete_first_token()

    args = token.split_contents()
    template_name = unquote(args[1])

    slots: dict[str, NodeList] = {"default": NodeList()}
    default_slot = SlotNode(name="default", nodelist=NodeList())

    for node in node_list:
        if isinstance(node, SlotNode):
            slots[node.name] = node.nodelist
        else:
            default_slot.nodelist.append(node)

    slots["default"].append(default_slot)

    return ComponentNode(slots, template_name, parse_extra_context(args[2:]))
