import itertools

from django import template

register = template.Library()

@register.filter
def chunks(value, chunk_length):
    """
    Breaks a list up into a list of lists of size <chunk_length>
    """
    clen = int(chunk_length)
    i = iter(value)
    while True:
        chunk = list(itertools.islice(i, clen))
        if chunk:
            yield chunk
        else:
            break

@register.filter(is_safe=True)
def strip_decimal(value):
    """
    Convert an integer to a string containing commas every three digits.
    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.
    """
    try:
        return int(value)
    except ValueError:
        return 0
    except TypeError:
        return value
