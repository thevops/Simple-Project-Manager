from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from datetime import datetime, timedelta

@login_required(login_url='/login/')
def index(request):
    msgs = ChatMessage.objects.filter(timestamp__gte=datetime.now()-timedelta(days=1))
    data = {
            'user': request.user,
            'messages': msgs
    }
    return render(request, 'shoutbox/czat.html', data)
