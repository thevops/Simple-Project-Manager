# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden

from django.contrib.auth.models import User
from .models import Project, Team, Task
from .forms import ProjectAddForm, ProjectJoinForm, MessageForm,\
    TaskCompleteProcentForm, TaskAddForm, TaskWeightForm
from django.contrib.auth.forms import PasswordChangeForm

from directmessages.apps import Inbox
from directmessages.models import Message

from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash

from django.db.models.functions import TruncMonth
from django.db.models import Count


"""
Auxiliary function
"""
def get_count(tas, month_num):
    for t in tas:
        if t["month"].month == month_num:
            return t["c"]
    return 0

def month_order(tas):
    names = [
                "styczeń","luty","marzec","kwiecień","maj","czerwiec","lipiec","sierpień","wrzesień",
                "październik","listopad","grudzień"
             ]
    ordered = []
    for i in range(1,13):
        ordered.append([names[i-1], get_count(tas, i)])

    return ordered

"""
Main page with overview
"""
@login_required(login_url='/login/')
def index(request):
    live_projects_count = len(Project.live_projects(request.user))
    end_projects_count = len(Project.end_projects(request.user))
    my_live_tasks = Task.objects.filter(contractor=request.user, complete_proc__lt=100).count
    my_end_tasks = Task.objects.filter(contractor=request.user, complete_proc__exact=100).count

    # how many time the project was carried out? EVERY project which I participated.
    projects_timedelta_chart = []
    for p in Project.objects.filter(complete_proc__exact=100).filter(owner=request.user):
        delta = p.enddate - p.startdate
        projects_timedelta_chart.append([p.name, delta.days])

    # Tasks order by months. Every task. Finished and not finished.
    tmp = Task.objects\
    					.filter(contractor=request.user)\
                        .annotate(month=TruncMonth('create_date'))\
                        .values('month')\
                        .annotate(c=Count('id'))
    tasks_month_count = month_order(tmp)

    data = {
            'projects_timedelta_chart': projects_timedelta_chart,
            'tasks_month_count': tasks_month_count,
            'live_projects_count': live_projects_count,
            'end_projects_count': end_projects_count,
            'my_live_tasks': my_live_tasks,
            'my_end_tasks': my_end_tasks,
            'default_password': check_password('password123', request.user.password)
    }
    return render(request, 'proman/index.html', data)

"""
Shows all projects
"""
@login_required(login_url='/login/')
def projects(request):
    user = request.user
    myprojects = Project.objects.filter(owner=user, complete_proc__lt=100)  # my projects
    end_myprojects = Project.objects.filter(owner=user, complete_proc__exact=100)
    notmyprojects = [i for i in user.team_set.all() if i.project.complete_proc < 100]  # projects which i participate
    end_notmyprojects = [i for i in user.team_set.all() if i.project.complete_proc == 100]
    end_projects = list(end_myprojects) + list(end_notmyprojects)
    data = {'myprojects': myprojects,
            'notmyprojects': notmyprojects,
            'end_projects': end_projects
            }
    return render(request, 'proman/projects.html', data)

"""
Shows form to add project
"""
@login_required(login_url='/login/')
def project_add(request):
    if request.method == 'POST':
        form = ProjectAddForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            startdate = form.cleaned_data['startdate']
            enddate = form.cleaned_data['enddate']
            Project.objects.create(name=name, owner=request.user, startdate=startdate,
                                   enddate=enddate, passforjoin=User.objects.make_random_password())
            return redirect('proman:projects')
    else:
        form = ProjectAddForm()
        return render(request, 'proman/project_add.html', {'form': form})

"""
Method to remove project
"""
@login_required(login_url='/login/')
def project_remove(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner == request.user:
        project.delete()
    return redirect('proman:projects')

"""
Shows form to edit project
"""
@login_required(login_url='/login/')
def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user != project.owner:
        return HttpResponseForbidden()
    form = ProjectAddForm(request.POST or None, instance=project)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('proman:projects')
    else:
        return render(request, 'proman/project_edit.html', {'form': form, 'project': project})

"""
Shows project page with details
"""
@login_required(login_url='/login/')
def project_show(request, project_id):
    user = request.user
    project = get_object_or_404(Project, pk=project_id)
    members = project.team_set.all()
    proj_tasks = project.task_set.all()
    project.refresh_complete_proc(proj_tasks)
    if project.owner == user:  # owner
        data = {
                'owner': True,
                'project': project,
                'members': members,
                'tasks': proj_tasks,
                'level': project.complete_proc
        }
        return render(request, 'proman/project_show.html', data)
    else:
        if Team.objects.filter(project=project, member=user).exists():
            data = {
                'owner': False,
                'project': project,
                'members': members,
                'tasks': proj_tasks,
                'level': project.complete_proc
            }
            return render(request, 'proman/project_show.html', data)
        else:
            # user not in members
            return HttpResponseForbidden()

"""
Shows form to join to project. User sign in to project himself.
"""
@login_required(login_url='/login/')
def project_join(request):
    user = request.user
    if request.method == 'POST':
        form = ProjectJoinForm(request.POST)
        if form.is_valid():
            jointext = form.cleaned_data["passforjoin"]
            try:
                proj_id = int(jointext.split("_")[0])
                proj_password = jointext.split("_")[1]
            except ValueError:
                error = "Błędny kod dostępu !"
                form = ProjectJoinForm()
                data = {
                    'error': error,
                    'form': form
                    }
                return render(request, 'proman/project_join.html', data)

            project = get_object_or_404(Project, pk=proj_id)
            if project.passforjoin == proj_password:
                Team.objects.create(project=project, member=user)
                return redirect('proman:projects')
            else:
                error = "Błędny kod dostępu !"
                form = ProjectJoinForm()
                data = {
                    'error': error,
                    'form': form
                    }
                return render(request, 'proman/project_join.html', data)
    else:
        form = ProjectJoinForm()
        data = {
                'form': form
                }
        return render(request, 'proman/project_join.html', data)

"""
Method to delete user from project
"""
@login_required(login_url='/login/')
def project_del_member(request, project_id, member_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner == request.user:
        member = get_object_or_404(User, pk=member_id)
        membership = Team.objects.get(project=project, member=member)
        if membership:
            membership.delete()
    return redirect('proman:project_show', project_id)

"""
Shows form to add user to project. Owner joins other users
"""
@login_required(login_url='/login/')
def project_add_member(request, project_id, member_id=None):
    project = get_object_or_404(Project, pk=project_id)
    if member_id:
        if project.owner == request.user:
            member = get_object_or_404(User, pk=member_id)
            Team.objects.create(project=project, member=member)
            return redirect('proman:project_add_member', project_id)
    else:
        t = project.team_set.all()
        tlist = [i.member.id for i in t]  # id list of members of project
        tlist.append(project.owner.id)  # add owner id to list
        restusers = User.objects.exclude(id__in=tlist).order_by('username')  # queryset of the rest of Users
        data = {
                'project': project,
                'restusers': restusers
            }
        return render(request, 'proman/project_add_member.html', data)

"""
Shows form to send a message between users.
"""
@login_required(login_url='/login/')
def message_send(request):
    user = request.user
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            recipient = get_object_or_404(User, username=form.cleaned_data["recipient"])
            msg = form.cleaned_data["content"]
            Inbox.send_message(user, recipient, msg)
            success = "Wiadomość wysłana"
            form = MessageForm()  # clear Form
            data = {'form': form,
                    'success': success}
            return render(request, 'proman/message_send.html', data)
        else:
            form = MessageForm()  # clear Form
            error = "Nie udało się wysłać wiadomości"
            data = {'form': form,
                    'error': error}
            return render(request, 'proman/message_send.html', data)
    else:
        form = MessageForm()
        form.fields["recipient"].queryset = User.objects.exclude(id=user.id)  # block messages to yourself
        data = {'form': form}
        return render(request, 'proman/message_send.html', data)

"""
Shows messages
"""
@login_required(login_url='/login/')
def message_show(request, friend_id=None):
    if friend_id:
        friend = get_object_or_404(User, id=friend_id)
        friend_and_me = Inbox.get_conversation(request.user, friend)
        conversation = []
        for i in friend_and_me:
            tmp = Inbox.read_message_formatted(i.id).split(' ',1)
            sent_at = Message.objects.get(id=i.id).sent_at
            tmp[0] = tmp[0].replace(":","")
            msg = {'name': tmp[0], 'txt': tmp[1], 'sent_at': sent_at}
            conversation.append(msg)
    else:
        conversation = None

    conversations_users = Inbox.get_conversations(request.user)
    data = {
            'conv_users': conversations_users,
            'conversation': conversation
    }
    return render(request, 'proman/message_show.html', data)


"""
User profile
"""
@login_required(login_url='/login/')
def user_profile(request, user_id):
    curr_user = get_object_or_404(User, id=user_id)
    if request.user == curr_user:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('proman:index')
            else:
                form = PasswordChangeForm(user=request.user)
                data = {
                    'curr_user': curr_user,
                    'me': True,
                    'form': form,
                    'error': "Błąd. Wpisz poprawnie nowe i stare hasło."
                }
                return render(request, 'proman/user_profile.html', data)
        else:
            form = PasswordChangeForm(user=request.user)
            data = {
                'curr_user': curr_user,
                'me': True,
                'form': form
            }
            return render(request, 'proman/user_profile.html', data)
    else:
        data = {
            'curr_user': curr_user,
            'me': False
        }
        return render(request, 'proman/user_profile.html', data)


"""
Shows task
"""
@login_required(login_url='/login/')
def task_show(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskCompleteProcentForm(request.POST)
        if form.is_valid():
            num = form.cleaned_data['task_progress']
            task.complete_proc = int(num)
            task.save()
            task.project.refresh_complete_proc(task.project.task_set.all())
    else:
        form = TaskCompleteProcentForm()
    data = {
            'task': task,
            'form': form
    }
    return render(request, 'proman/task_show.html', data)

"""
Form to add task
"""
@login_required(login_url='/login/')
def task_add(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = TaskAddForm(request.POST, users=User.objects.all())  # users param must be, because of errors
        if form.is_valid():
            # TODO can add the same task more then once !!!
            Task.objects.create(project=project,
                                name=form.cleaned_data['name'],
                                description=form.cleaned_data['description'],
                                contractor=form.cleaned_data['contractor'])
            return redirect('proman:project_show', project_id)
        else:
            # TODO TaskAdd form is invalid
            return redirect('proman:project_show', project_id)
    else:
        ids_team = [m.member.id for m in project.team_set.all()]
        ids_team.append(project.owner.id)
        users_team = User.objects.filter(pk__in=set(ids_team))
        form = TaskAddForm(users=users_team)
        data = {'form': form,
                'project': project}
        return render(request, 'proman/task_add.html', data)

"""
Method to remove task
"""
@login_required(login_url='/login/')
def task_remove(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.project.owner == request.user:
        task.delete()
    return redirect('proman:project_show', task.project.id)

"""
Edit task
"""
@login_required(login_url='/login/')
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.user != task.project.owner:
        return HttpResponseForbidden()
    ids_team = [m.member.id for m in task.project.team_set.all()]
    users_team = User.objects.filter(pk__in=set(ids_team))
    form = TaskAddForm(request.POST or None, instance=task, users=users_team)
    if request.method == 'POST' and form.is_valid():
        form.save()
        """task.update(name=form.cleaned_data['name'],
                    description=form.cleaned_data['description'],
                    contractor=form.cleaned_data['contractor'])"""
        return redirect('proman:project_show', task.project.id)
    else:
        data = {'form': form,
                'task': task}
        return render(request, 'proman/task_edit.html', data)


"""
Shows user tasks
"""
@login_required(login_url='/login/')
def tasks(request):
    my_live_tasks = Task.objects.filter(contractor=request.user, complete_proc__lt=100).order_by('project')
    my_end_tasks = Task.objects.filter(contractor=request.user, complete_proc__exact=100).order_by('project')
    data = {
            'my_live_tasks': my_live_tasks,
            'my_end_tasks' : my_end_tasks
    }
    return render(request, 'proman/tasks.html', data)


"""
Used below
"""
def check_forms_list(forms):
    for f in forms:
        if not f.is_valid():
            return False
    return True

"""
Shows form to change task weights
"""
@login_required(login_url='/login/')
def task_change_weight(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user != project.owner:
        return HttpResponseForbidden
    forms = []
    for t in list(project.task_set.all()):
        forms.append(TaskWeightForm(request.POST or None, instance=t, txt=t.name, prefix=t.id))
    if request.method == "POST" and check_forms_list(forms):
        sum = 0
        for f in forms:
            sum += f.cleaned_data["weight"]
        if sum != 100:  # check if sum of weights is 100
            data = {
                'project': project,
                'forms': forms,
                'error': "Suma wag musi być równa 100",
                'tasksnum': project.task_set.all().count()
            }
            return render(request, 'proman/task_change_weight.html', data)

        for f in forms:
            f.save()
        return redirect('proman:project_show', project.id)
    else:
        data = {
                'project': project,
                'forms': forms,
                'error': None,
                'tasksnum': project.task_set.all().count()
        }
        return render(request, 'proman/task_change_weight.html', data)

"""
Apply task to done
"""
@login_required(login_url='/login/')
def task_done(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user == task.contractor:
        task.complete_proc = 100
        task.save()
    return redirect('proman:task_show', task_id)
