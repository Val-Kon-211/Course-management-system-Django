from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from courses import models as courses_models


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request, user_id):
    try:
        u_id = int(user_id)
        user = User.objects.get(id=u_id)
    except User.DoesNotExist:
        return HttpResponse("Такого пользователя нет.")
    part_object = courses_models.Participants.objects.filter(user=user)
    courses = []
    for part in part_object:
        courses.append(courses_models.Course.objects.filter(id=part.course.id))
    author_courses = courses_models.Authors.objects.filter(user=user)
    if author_courses:
        for ac in author_courses:
            courses.append(ac.course.id)

    context = {'user': user,
               'courses': courses}

    return render(request, 'users/profile.html', context)