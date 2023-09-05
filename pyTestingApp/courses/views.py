from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.contrib import messages
from django.http import HttpResponse
from .models import Authors, Course, Lesson, Participants, LessonDone, LessonDocuments
from .forms import LessonCreateForm, CourseCreateForm
import sys, subprocess, os, docx, markdown
from subprocess import PIPE

@login_required(login_url="login")
def courses_show(request):
    courses_dict = {}
    courses = Course.objects.all()
    for course in courses:
        authors = Authors.objects.filter(course=course)
        courses_dict[course] = authors
    context = {'courses': courses_dict}
    return render(request, "courses/courses.html", context)

@login_required(login_url="login")
def course_create(request):
    if request.method == 'POST':
        form = CourseCreateForm(request.POST)
        # создание нового курса
        course = Course.objects.create(name=request.POST["name"], description=request.POST["description"])
        course.save()
        # указание автора курса
        author = Authors.objects.create(user=request.user, course=course)
        author.save()

        return redirect('app-courses')
    else:
        form = CourseCreateForm()

    return render(request, 'courses/course-create.html', {"form": form})

@login_required(login_url="login")
def course_open(request, course_id):
    course = Course.objects.get(id=course_id)
    part = False
    parts = Participants.objects.filter(course=course, user=request.user)
    author = Authors.objects.filter(course=course, user=request.user)
    if parts or author:
        part = True
    cur_lessons = Lesson.objects.filter(course=course_id)
    if not cur_lessons:
        context = {'course': course,
                   'lessons': '',
                   'part': part}
    else:
        context = {'course': course,
                   'lessons': cur_lessons,
                   'part': part}

    return render(request, "course/course.html", context)

@login_required(login_url="login")
def course_delete(request, course_id):
    participants = Participants.objects.filter(course=course_id)
    for p in participants:
        Participants.objects.get(p.id).delete()
    lessons = Lesson.objects.filter(course=course_id).delete()
    for l in lessons:
        Lesson.objects.get(l.id).delete()
    Course.objects.get(id=course_id).delete()

    return redirect('course-open', course_id=course_id)

@login_required(login_url="login")
def course_edit(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        form = CourseCreateForm(request.POST)
        course.name = request.POST["name"]
        course.description = request.POST["description"]
        course.save()

        return redirect('course-open')
    else:
        form = CourseCreateForm()
        form.fields['name'].initial = course.name
        form.fields['description'].initial = course.description

    return render(request, 'courses/course-create.html', {"form": form})

@login_required(login_url="login")
def enroll_in_course(request, course_id):
    if not Participants.objects.filter(user=request.user):
        print("enroll_in_course inside")
        parts = Participants.objects.create(user = request.user,course = Course.objects.get(id=course_id))
        parts.save()
        return redirect('course-open', course_id=course_id)
    return course_open(request, course_id)

@login_required(login_url="login")
def back_to_course(request, course_id):
    return redirect('course-open', course_id=course_id)

@login_required(login_url="login")
def lesson_create(request, course_id):
    if request.method == 'POST':
        form = LessonCreateForm(request.POST, request.FILES)
        documents = LessonDocuments.objects.create(theory=request.FILES["theory"], task=request.FILES["task"], test=request.FILES["test"])
        documents.save()
        course = Course.objects.get(id=course_id)
        lesson = Lesson.objects.create(name=request.POST["name"], course=course, documents=documents)
        lesson.save()

        return redirect('course-open', course_id=course_id)
    else:
        form = LessonCreateForm()

    return render(request, 'course/lesson-create.html', {"form": form})

@login_required(login_url="login")
def lesson_edit(request, course_id, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    documents = LessonDocuments.objects.get(id=lesson.documents.id)
    if request.method == 'POST':
        form = LessonCreateForm(request.POST, request.FILES)
        if request.FILES.get("theory", False):
            documents.theory = request.FILES["theory"]
        if request.FILES.get("task", False):
            documents.task = request.FILES["task"]
        if request.FILES.get("test", False):
            documents.test = request.FILES["test"]
        documents.save()
        lesson.name = request.POST["name"]
        lesson.documents = documents
        lesson.save()
        return redirect('lesson-open', course_id=course_id, lesson_id=lesson_id)
    else:
        form = LessonCreateForm()
        form.fields['name'].initial = lesson.name
        form.fields['theory'].initial = documents.theory
        form.fields['task'].initial = documents.task
        form.fields['test'].initial = documents.test

    return render(request, 'course/lesson-create.html', {"form": form})

@login_required(login_url="login")
def lesson_delete(request, course_id, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    doc = lesson.documents
    LessonDocuments.objects.get(id=doc.id).delete()
    LessonDone.objects.filter(lesson=lesson).delete()
    lesson.delete()

    return redirect('course-open', course_id=course_id)

@login_required(login_url="login")
def lesson_theory(request, lesson_id, course_id):
    cur_lessons = Lesson.objects.filter(course=course_id)
    lesson = Lesson.objects.get(id=lesson_id)
    theoryDoc = lesson.documents.theory.path
    extension = theoryDoc[theoryDoc.rfind('.')+1:]
    if extension == 'docx':
        doc = docx.Document(theoryDoc)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        text = '\n\n'.join(fullText)
    else:
        with open(theoryDoc, encoding="utf-8") as f:
            lines = f.readlines()
            text = '\n\n'.join(lines)

    context = {'lessons': cur_lessons,
               'course_id': course_id,
               'lesson': lesson,
               'text': text}

    return render(request, "course/theory.html", context)

@login_required(login_url="login")
def lesson_task(request, lesson_id, course_id):
    cur_lessons = Lesson.objects.filter(course=course_id)
    lesson = Lesson.objects.get(id=lesson_id)
    taskDoc = lesson.documents.task.path
    extension = taskDoc[taskDoc.rfind('.') + 1:]
    if extension == 'docx':
        doc = docx.Document(taskDoc)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        text = '\n\n'.join(fullText)
    else:
        with open(taskDoc, encoding="utf-8") as f:
            lines = f.readlines()
            text = '\n\n'.join(lines)

    context = {'lessons': cur_lessons,
               'course_id': course_id,
               'lesson': lesson,
               'text': text}

    return render(request, "course/task.html", context)

@login_required(login_url="login")
def lesson_practice(request, lesson_id, course_id):
    cur_lessons = Lesson.objects.filter(course=course_id)
    lesson = Lesson.objects.get(id=lesson_id)
    context = {'lessons': cur_lessons,
               'course_id': course_id,
               'lesson': lesson}

    return render(request, "course/practice.html", context)

@login_required(login_url="login")
def runcode(request, lesson_id, course_id):
    if request.method == "POST":
        codeareadata = request.POST['codearea']
        try:
            # создаём python файл, куда запишем код
            if not os.path.exists('media/tests/function.py'):
                os.open('media/tests/function.py', os.O_CREAT)
            progFile = os.open('media/tests/function.py', os.O_WRONLY)
            # обрезаем содержимое файла до 0 байтов, чтобы не было перезаписи каким-либо образом
            # с помощью операции записи.
            os.truncate(progFile, 0)
            # кодируем строку в байты
            progText = str.encode(codeareadata)
            # записываем в файл
            os.write(progFile, progText)
            # закрываем файл
            os.close(progFile)

            lesson = Lesson.objects.get(id=lesson_id)

            # запускаем компиляцию файла в режиме pytest
            process = subprocess.Popen(['pytest', '-v', lesson.documents.test.path], stderr=PIPE, stdout=PIPE)
            stdout, stderr = process.communicate()

            outputText = stdout.decode("utf-8")

            if "ERRORS" in outputText:
                indexError = outputText.index("Error")
                indexSpace = outputText.rfind(' ', 0, indexError)
                indexNewLine = outputText.index('\n', indexError)
                outputTextFin = ' '
                messages.add_message(request, messages.WARNING, 'Ошибка:' + outputText[indexSpace + 1:indexNewLine])

            elif "PASSED" or "FAILED" in outputText:
                indexPoints = outputText.index("::")
                preText = outputText[indexPoints:]
                indexEqual = preText.index("=")
                resultsText = preText[:indexEqual]

                resultStrings = []
                for string in resultsText.split('\n'):
                    if "::" in string:
                        inxPoints = string.index("::")
                        inxBracket = string.index("[")
                        resultStrings.append(string[inxPoints+2:inxBracket].split("  ")[0])
                    else:
                        continue
                outputTextFin = '\n'.join(resultStrings)
                if "FAILED" in outputTextFin:
                    messages.add_message(request, messages.ERROR, f'Задание не выполнено. Пройдены не все тесты.')
                else:
                    messages.add_message(request, messages.SUCCESS, f'Задание выполнено успешно.')

            # outputTextFin = resultsText

            #message.success(request, f'Задание выполнено успешно.')
            #message.warning(request, 'Ошибка:' + error)
            #message.error(request, f'Задание выполнена неверно!')

            # сохраняем оргинальный стандартный вывод
            f = open("file.txt", "w")
            f.write(outputTextFin)
            f.close()
            # читаем вывод с файла и сохраняем
            output = open('file.txt', 'r').read()

        except Exception as e:
            output = e

    lesson = Lesson.objects.get(id=lesson_id)
    cur_lessons = Lesson.objects.filter(id=course_id)
    context = {"code":codeareadata,
               "output":output,
               "lesson": lesson,
               "lessons": cur_lessons,
               "course_id": course_id}

    return render(request, 'course/practice.html', context)