from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from Base import models
from Base.models import Contact
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings

# Create your views here.

#def home(request):
#    return render(request,'home.html')

def contact(request):
    if request.method == "POST":
        print('post')
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        number = request.POST.get('number')
        print(name,email,content,number)

        if len(name) > 1 and len(name) < 30:
            pass
        else:
            messages.error(request,'Length on name should be greater than 2 and less than 30 words')
            return render(request,'home.html')

        if len(email) > 1 and len(email) < 30:
            pass
        else:
            messages.error(request,'Invlaid email, try again') 
            return render(request,'home.html')
        
        if len(number) >2 and len(number) <=10:
            pass
        else:
            messages.error(request,'Invalid number, try again.')
            return render(request,'home.html')
        
        ins = models.Contact(name=name, email=email, content=content, number=number)
        ins.save()
        
       
        subject = f"New message from {name}"
        body = f"""
        Name: {name}
        Email: {email}
        Phone: {number}

        Contents:
        {content}
        """

        try:
            send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,   #from email
            recipient_list=[settings.EMAIL_HOST_USER], #to email (my Gmail)
            fail_silently=False
            )
            messages.success(request,"Your message has been sent successfully!")
        except BadHeaderError:
            messages.error(request,"Invalid header found.")
        except Exception as e:
            messages.error(request,f"Could not send email.")
        

    return render(request,'home.html')
