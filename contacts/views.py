from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse,request
from .models import Contact
# Create your views here.
def contact(request):
  if request.method == 'POST':
    listing_id = request.POST['listing_id']
    listing = request.POST['listing']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    message = request.POST['message']
    user_id = request.POST['user_id']
    realtor_email = request.POST['realtor_email']
    if request.user.is_authenticated:
      user_id = request.user.id
      has_contacted = Contact.objects.all().filter(listing_id = listing_id,user_id= user_id)
      if has_contacted:
        messages.error(request, 'you have already enquired about this properrty')
        return redirect('/listings/'+listing_id)
    contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, messages=messages, user_id=user_id )   
    contact.save()
    #send email
    'property Listing Inquiry',
    'there has been enquiry for '+ listing +'.sign into the admin panel for more infor',
    'kchandrakanth130@gmail.com'
    [realtor_email,'']
    messages.success(request, 'your request has been submitted a realtor will get back to u soon')
    return redirect('/listings/'+listing_id)