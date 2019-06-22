from django import template

register = template.Library()

@register.simple_tag
def debug(the_var=None):
    """
    Debug tremplate variables
    Usage in a template :
    {% load debug %}
    {% debug variable_name %} or simply {% debug %}
    :param the_var: The variable to debug. Optional, debugs the template if not specified
    :return:
    """
    print("--- DEBUGGING ---")
    print(type(the_var))
    print(the_var)
