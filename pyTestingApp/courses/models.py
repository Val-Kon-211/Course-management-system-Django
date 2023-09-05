from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        super(Course, self).save(*args, **kwargs)

class Authors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class LessonDocuments(models.Model):
    theory = models.FileField(upload_to='theories/')
    task = models.FileField(upload_to='tasks/')
    test = models.FileField(upload_to='tests/')

class Lesson(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    documents = models.ForeignKey(LessonDocuments, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Lesson, self).save(*args, **kwargs)


class LessonDone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Participants, self).save(*args, **kwargs)


class Participants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Participants, self).save(*args, **kwargs)

