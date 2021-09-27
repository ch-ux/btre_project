from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages,auth
from contacts.models import Contact
from django.contrib.auth.models import User

# Create your views here.
def register(request):
  if request.method == 'POST':
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

      #check if passwords match
    if password ==  password2:
      #check username
      if User.objects.filter(username=username).exists():
          messages.error(request,'that username is taken')
          return redirect('register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request,'that email is taken')
          return redirect('register')
        else:
           #looks good
           user = User.objects.create_user(username=username, password=password,
           email=email, first_name=first_name, last_name=last_name) 
            #login after register
            #auth.login(request, user)
            #messages.success(request, 'you are logged in')
            #return redirect('index')
           user.save()
           messages.success(request, 'you are registered and can log in')
           return redirect('login')

    else:
      messages.error(request,'passwords dont match')
      return redirect('register')
  else:
    return render(request, 'accounts/register.html')
  

def login(request):
  if request.method == 'POST':
    #login user
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username = username, password = password)
    if user is not None:
      auth.login(request,user)
      messages.success(request,'you are now logged in')
      return redirect('dashboard')
    else:
      messages.error(request,'Invalid credentials')
      return redirect('login')
  else:
    return render(request,'accounts/login.html')
    

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request,'you are now logged out')
    return redirect('index')
  return redirect(request,'index.html')

def dashboard(request):
  user_contacts = Contact.objects.order_by('-contact_date').filter(user_id = request.user.id)
  context = {'contacts':user_contacts}
  return render(request,'accounts/dashboard.html', context)

