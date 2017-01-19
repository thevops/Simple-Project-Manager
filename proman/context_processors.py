from directmessages.apps import Inbox

def messages(request):
    user = request.user
    if not user.is_authenticated:  # login_app try to load this context proccesor. Dont know why..
        msgs = ""
    else:
        msgs = Inbox.get_unread_messages(user).order_by('-sent_at')[:4]  # take 4 last messages
    return {'msgs': msgs}