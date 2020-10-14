from django import template
register = template.Library()

# TemplateTag personalizada para agregarle una clase CSS a un field de un form
@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

                   