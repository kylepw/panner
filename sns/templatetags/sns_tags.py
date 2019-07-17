"""Custom template tags for `sns` app."""

from django import template
register = template.Library()

def get_sns(data, sns):
    """Return value of `sns` in dict `data`."""
    return data.get(sns)

register.filter('get_sns', get_sns)