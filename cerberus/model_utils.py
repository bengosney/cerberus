# Standard Library
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Transition:
    name: str
    icon: str = ""
    sort: int = 0
    meta: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return self.name

    def get(self, key: str, default: str) -> str:
        return getattr(self, key, default)


class TransitionActionsMixin:
    @property
    def available_state_transitions(self) -> Iterable[Transition]:
        transitions = [
            Transition(
                name=t.name,
                icon=t.custom.get("icon", ""),
                sort=t.custom.get("sort", 0),
                meta=t.custom,
            )
            for t in self.get_available_state_transitions()  # type: ignore
        ]
        transitions.sort(key=lambda x: x.sort)
        return transitions
