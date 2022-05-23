from lib2to3.pgen2.pgen import DFAState
from django import template

register = template.Library()


@register.filter(name="star_display")
def star_display(num):
    star = ""
    for _ in range(int(num)):
        star += "★"

    return star
