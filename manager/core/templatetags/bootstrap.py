from django import template

register = template.Library()

@register.filter(name='bootstrap_field')
def bootstrap_field(field):
    return field.as_widget(attrs={'class':'form-control'})