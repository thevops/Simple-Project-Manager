
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from django.template.defaultfilters import truncatechars
from django.core.validators import MaxValueValidator, MinValueValidator

from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=80, verbose_name="nazwa projektu")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Właściciel")
    startdate = models.DateField(verbose_name="Data rozpoczęcia")  # auto_now_add=True
    enddate = models.DateField(verbose_name="Data zakończenia")
    passforjoin = models.CharField(max_length=80)
    complete_proc = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                        verbose_name="procent wykonania projektu")

    def __str__(self):
        return self.name

    def refresh_complete_proc(self, taskslist):
        level = 0
        for task in taskslist:
            level += (task.weight / 100) * task.complete_proc
        self.complete_proc = level
        if self.complete_proc == 100:
            self.enddate = timezone.now()
        self.save()

    @staticmethod
    def live_projects(user):
        return list(Project.objects.filter(owner=user, complete_proc__lt=100)) + \
                    [i.project for i in user.team_set.all() if i.project.complete_proc < 100]

    @staticmethod
    def end_projects(user):
        return list(Project.objects.filter(owner=user, complete_proc__exact=100)) + \
                   [i.project for i in user.team_set.all() if i.project.complete_proc == 100]

    class Meta:
        verbose_name_plural = "projekty"
        ordering = ['enddate']


class Team(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="projekt")
    member = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="członek")

    def __str__(self):
        return "Projekt: " + self.project.name + " User: " + self.member.username

    class Meta:
        verbose_name_plural = "zespoły"


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="nazwa projektu")
    name = models.CharField(max_length=80, verbose_name="nazwa zadania", default="zadanie")
    description = models.TextField(verbose_name="treść")
    contractor = models.ForeignKey(User, verbose_name="wykonawca", db_column='member')
    weight = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                               verbose_name="waga zadania")
    complete_proc = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                        verbose_name="procent wykonania zadania")
    create_date = models.DateField(verbose_name="Data utworzenia", default=timezone.now)

    def __str__(self):
        return self.name

    @property
    def short_description(self):
        return truncatechars(self.description, 100)

    class Meta:
        verbose_name_plural = "zadania"
        verbose_name = "zadanie"
