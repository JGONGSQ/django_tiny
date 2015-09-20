from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class":css})

@register.filter(name='addbootstrapstyle')
def addbootstrapstyle(field, placeholder):
    return field.as_widget(attrs={"class": "form-control textarea-sm", "placeholder":placeholder})

@register.filter(name='get_item')
def get_item(dictionary,key):
    return dictionary.get(key)

@register.filter(name='clean_email')
def clean_email(email):
    return email.replace(';', ' ')
