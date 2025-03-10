from django import template
from django.template.loader import render_to_string
from ..models import Department

register = template.Library()


@register.simple_tag
def render_department_tree(department):
    sub_departments = Department.objects.filter(parent=department)

    return render_to_string(
        "departments/department_tree.html",
        {"department": department, "sub_departments": sub_departments},
    )
