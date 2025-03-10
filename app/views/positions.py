from django.shortcuts import render, redirect, get_object_or_404
from ..models import Position
from ..utils import get_departments


def all_positions(request):
    positions = Position.objects.all()
    return render(request, "positions/positions.html", {"positions": positions})


def add_position(request, department_id=None):
    departments = get_departments(department_id)

    if request.method == "POST":
        position_name = request.POST.get("name")
        departments_id = request.POST.getlist("departments")

        if position_name and departments_id:
            position = Position.objects.create(name=position_name)
            position.departments.add(*departments_id)

        return redirect("app:positions")

    return render(
        request, "positions/positions_form.html", {"departments": departments}
    )


def edit_position(request, position_id, department_id=None):
    position = get_object_or_404(Position, pk=position_id)
    selected_departments = position.departments.values_list("id", flat=True)
    all_departments = get_departments(department_id)

    if request.method == "POST":
        position_name = request.POST.get("name")
        departments_id = request.POST.getlist("departments")

        position.name = position_name
        position.departments.clear()
        position.departments.add(*departments_id)

        position.save()
        return redirect("app:positions")

    return render(
        request,
        "positions/positions_form.html",
        {
            "position": position,
            "selected_departments": list(selected_departments),
            "departments": all_departments,
        },
    )


def delete_position(request, pk):
    position = get_object_or_404(Position, pk=pk)

    if request.method == "POST":
        position.delete()
        return redirect("app:positions")

    return render(request, "positions/delete_position.html", {"position": position})
