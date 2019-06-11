from django import template

register = template.Library()

@register.simple_tag
def debug(the_var=None):
    """
    Permet de débugger des variables de template.
    Utilisation dans un template :
    {% load debug %}
    {% debug la_variable_a_debugger %} ou juste {% debug %}
    :param the_var: La variable à passer en paramètre. Optionnel si on ne veut que tester que le code s'exécute bien
    à cet endroit
    :return:
    """
    print("--- DEBUGGING ---")
    print(type(the_var))
    print(the_var)
