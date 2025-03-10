from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sub_departments",
    )

    def __str__(self):
        return self.name

    def get_sub_departments(self):
        return ", ".join([d.name for d in Department.objects.filter(parent=self)])

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"
        db_table = "departments"


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)
    departments = models.ManyToManyField(Department, related_name="positions")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"
        db_table = "positions"


class Employee(models.Model):
    name = models.CharField(max_length=255)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        db_table = "employees"
