# custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_position(col,row ):
    files=['a','b','c','d','e','f','g','h']
    ranks = ['1','2','3','4','5','6','7','8']
    return files[int(col)] + ranks[int(row)]
