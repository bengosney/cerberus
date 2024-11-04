from datetime import timedelta

import humanize

from django import template

register = template.Library()


@register.filter
def naturaldelta(duration: timedelta):
    return humanize.naturaldelta(duration)


@register.filter
def precisedelta(duration: timedelta, minimum_unit: str = "minutes"):
    return humanize.precisedelta(duration, minimum_unit=minimum_unit)


@register.inclusion_tag("cerberus/templatetags/natural_time.html")
def natural_time(duration: timedelta):
    return {"duration": duration}
