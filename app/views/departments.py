from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from ..models import Department


def all_departments(request):
    return render(request, "departments/departments.html")


def add_department(request, pk):
    if request.method == "POST":
        new_department_name = request.POST.get("name")
        if pk == 0:
            Department.objects.create(name=new_department_name)
        else:
            parent = get_object_or_404(Department, pk=pk)
            Department.objects.create(name=new_department_name, parent=parent)

        return redirect("app:departments")

    return render(request, "departments/add_department.html")


def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    sub_departments = department.get_sub_departments()

    if request.method == "POST":
        department.delete()
        return redirect("app:departments")

    return render(
        request,
        "departments/delete_department.html",
        {"department": department, "sub_departments": sub_departments},
    )


def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    departments = Department.objects.exclude(pk=pk)

    if request.method == "POST":
        new_department_name = request.POST.get("name")
        new_parent_id = request.POST.get("parent")

        if new_department_name:
            department.name = new_department_name

        if new_parent_id and new_parent_id.isdigit():
            new_parent = get_object_or_404(Department, pk=int(new_parent_id))
            if new_parent != department.parent:
                Department.objects.filter(parent=department).update(
                    parent=department.parent
                )

                department.parent = new_parent
        else:
            Department.objects.filter(parent=department).update(
                parent=department.parent
            )

            department.parent = None

        department.save()
        return redirect("app:departments")

    return render(
        request,
        "departments/edit_department.html",
        {"department": department, "departments": departments},
    )


def departments_tree_json(request):
    def build_tree(parent):
        children = Department.objects.filter(parent=parent)
        return {
            "name": parent.name,
            "pk": parent.pk,
            "children": [build_tree(child) for child in children] if children else [],
        }

    root_departments = Department.objects.filter(parent__isnull=True)
    tree_data = [build_tree(dep) for dep in root_departments]

    return JsonResponse(tree_data, safe=False)
