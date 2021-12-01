from django.shortcuts import render
from django.conf import settings
# Create your views here.
import razorpay
from .models import book
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string

razorpay_client = razorpay.Client(auth=(settings.RAZOR_API_KEY, settings.RAZOR_SECRET_KEY))


def home(request):
    if request.method=="POST":
        name= request.POST.get('name')
        amount = int(request.POST.get('amount')) * 100
        email=request.POST.get('email')
        payment= razorpay_client.order.create({'amount':amount,"currency":'INR','payment_capture':'1'})
        print(payment)
        Book= book(name=name ,amount=amount,email=email, payment_id = payment['id'])
        Book.save()
        return render(request,'index.html',{'payment':payment})
        print(name,amount)
    return render(request,'index.html')

@csrf_exempt
def success(request):
    if request.method=="POST":
        store=request.POST
        order_id =""
        for key,val in store.items():
            if key == 'razorpay_order_id':
                order_id=val
                break
        user= book.objects.filter(payment_id=order_id).first()
        user.paid=True
        user.save()

        msg_plain =render_to_string('email.txt')
        msg_html = render_to_string('email.html')

        send_mail("Your donation has been received",msg_plain,settings.EMAIL_HOST_USER,["user.email"] , html_message= msg_html)

    return render(request,'success.html')


