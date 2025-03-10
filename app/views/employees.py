from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from ..utils import get_departments
from ..models import Position, Employee, Department
from ..forms import EmployeeForm


def create_employees(request, department_id=None):
    departments = get_departments(department_id)
    return render(
        request, "employees/create_employees.html", {"departments": departments}
    )


def get_positions(request, department_id):
    try:
        department = Department.objects.get(id=department_id)
        positions = Position.objects.filter(departments=department).values("id", "name")
        return JsonResponse({"positions": list(positions)})
    except Department.DoesNotExist:
        return JsonResponse({"positions": []})


def create_employee(request):
    if request.method == "POST":
        name = request.POST.get("name")
        position_id = request.POST.get("position")

        if name and position_id:
            position = get_object_or_404(Position, id=position_id)
            Employee.objects.create(name=name, position=position)

    return redirect("app:employee_list")


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, "employees/employee_list.html", {"employees": employees})


def employee_edit(request, employee_id, department_id=None):
    employee = get_object_or_404(Employee, id=employee_id)
    departments = get_departments(department_id)

    form = EmployeeForm(request.POST or None, instance=employee)

    if form.is_valid():
        form.save()
        return redirect("app:employee_list")

    return render(
        request,
        "employees/employee_edit.html",
        {"form": form, "employee": employee, "departments": departments},
    )


def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == "POST":
        employee.delete()
        return redirect("app:employee_list")
    return render(request, "employees/employee_delete.html", {"employee": employee})
