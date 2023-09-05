from django import forms

class CourseCreateForm(forms.Form):
    name = forms.CharField(max_length=50, label=u'Название курса')
    description = forms.CharField(max_length=255, label=u'Красткое описание курса')

class LessonCreateForm(forms.Form):
    name = forms.CharField(max_length=50, label=u'Название урока')
    theory = forms.FileField(label=u'Теоретический материал')
    task = forms.FileField(label=u'Текст задания')
    test = forms.FileField(label=u'Тестирующий скрипт')