from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, LessonDocuments, LessonDone, Participants

admins_group, created = Group.objects.get_or_create(name="Admins")
teacher_group, created = Group.objects.get_or_create(name="Teachers")
students_group, created = Group.objects.get_or_create(name="Students")

models_dict = {"course":Course, "lesson":Lesson, "lessondocuments":LessonDocuments,
               "lessondone":LessonDone, "participants":Participants, "author":authors}

for model in models_dict.items():
    content_type = ContentType.objects.get_for_model(model[1])
    model_permission = Permission.objects.filter(content_type=content_type)
    for perm in model_permission:
        if perm.codename == f"delete_{model[0]}":
            admins_group.permissions.add(perm)
            teacher_group.permissions.add(perm)

        elif perm.codename == f"change_{model[0]}":
            admins_group.permissions.add(perm)
            teacher_group.permissions.add(perm)

        elif perm.codename == f"add_{model[0]}":
            admins_group.permissions.add(perm)
            teacher_group.permissions.add(perm)

        else:
            admins_group.permissions.add(perm)
            teacher_group.permissions.add(perm)
            students_group.permissions.add(perm)