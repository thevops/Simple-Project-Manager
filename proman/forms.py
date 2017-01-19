# coding=utf-8
from django import forms
from .models import Project, Task
from django.contrib.auth.models import User


class ProjectAddForm(forms.ModelForm):
    startdate = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}), label="Data rozpoczęcia")
    enddate = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}), label="Data zakończenia")

    class Meta:
        model = Project
        fields = ['name', 'startdate', 'enddate']

class ProjectJoinForm(forms.Form):
    passforjoin = forms.CharField(required=True, label="Kod dostępu")

class MessageForm(forms.Form):
    recipient = forms.ModelChoiceField(required=True, queryset=User.objects.all(), label="Odbiorca")
    content = forms.CharField(widget=forms.Textarea, required=True, label="Treść")


class TaskCompleteProcentForm(forms.Form):
    task_progress = forms.IntegerField(label="Wykonano", min_value=0, max_value=100)


class TaskAddForm(forms.ModelForm):
    contractor = forms.ModelChoiceField(queryset=User.objects.all(), label="Wykonawca")

    def __init__(self, *args, **kwargs):
        users = kwargs.pop('users')  # pop must be before super method
        super(TaskAddForm, self).__init__(*args, **kwargs)
        self.fields['contractor'].queryset = users

    class Meta:
        model = Task
        fields = ('name', 'description', 'contractor')

class TaskWeightForm(forms.ModelForm):
    weight = forms.IntegerField(min_value=0, max_value=100,)

    def __init__(self, *args, **kwargs):
        txt = kwargs.pop('txt')
        super(TaskWeightForm, self).__init__(*args, **kwargs)
        self.fields['weight'].label = txt

    class Meta:
        model = Task
        fields = ['weight']
