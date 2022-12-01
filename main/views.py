from django.shortcuts import render
from .models import About
from orders.utils import *
from orders.models import BotAdmin


# Create your views here.
def main(request):
    return HttpResponse('ok')


def about(request):
    about = About.objects.all()

    context = {
        'about': about,
    }
    return render(request, 'pages/about.html', context)



def contact(request):
    if request.method == "POST":
        name = request.POST.get("contact-name")
        message = request.POST.get("contact-message")
        print(name, message)
        admins = BotAdmin.objects.filter(is_active=True)
        for admin in admins:
            text = generate_contact_text(name, message)
            res = send_message(text, admin.user_id)
            print(res)
    return render(request, 'pages/contact.html')
