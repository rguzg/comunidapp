from django import template
register = template.Library()
import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()


# TemplateTag personalizada para agregarle una clase CSS a un field de un form
@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return 'invalid'

register.filter('getattribute', getattribute)