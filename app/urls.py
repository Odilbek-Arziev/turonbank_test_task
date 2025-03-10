from django.urls import path, re_path
from .views import employees, departments, positions

urlpatterns = [
    # employees
    path("", employees.employee_list, name="employee_list"),
    re_path(
        r"^create_employees/(?:(?P<department_id>\d+)/)?$",
        employees.create_employees,
        name="index",
    ),
    path("get_positions/<int:department_id>/", employees.get_positions, name="get_positions"),
    path("create_employee/", employees.create_employee, name="create_employee"),
    path("employee_delete/<int:employee_id>/", employees.employee_delete, name="employee_delete"),
    re_path(
        r"^employee_edit/(?P<employee_id>\d+)(?:/(?P<department_id>\d+))?/$",
        employees.employee_edit,
        name="employee_edit",
    ),

    # departments
    path("departments/", departments.all_departments, name="departments"),
    path("add_department/<int:pk>", departments.add_department, name="add_department"),
    path("delete_department/<int:pk>", departments.delete_department, name="delete_department"),
    path("edit_department/<int:pk>", departments.edit_department, name="edit_department"),
    path("departments/tree/data/", departments.departments_tree_json, name="departments_tree_json"),

    # positions
    path("positions/", positions.all_positions, name="positions"),
    re_path(
        r"^add_position/(?P<department_id>\d+)?$", positions.add_position, name="add_position"
    ),
    re_path(
        r"^edit_position/(?P<position_id>\d+)(?P<department_id>\d+)?$",
        positions.edit_position,
        name="edit_position",
    ),
    path("delete_position/<int:pk>", positions.delete_position, name="delete_position"),
]
