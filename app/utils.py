from .models import Department


def get_departments(department_id=None):
    if department_id:
        departments = Department.objects.filter(parent_id=department_id)
    else:
        departments = Department.objects.filter(parent__isnull=True)

    return departments
