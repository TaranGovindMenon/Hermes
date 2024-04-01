from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import views as auth_views
from .models import Company,Job
from django.contrib.auth.hashers import make_password
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request, 'index.html')
     
def student_index(request):
    return render(request, 'student_index.html')

def company_index(request): 
    return render(request, 'company_index.html')


from django.contrib.auth import authenticate
from django.contrib import messages

def company_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['username'] = user.username
                request.session['email'] = user.email
                return redirect('company_dashboard')
            else:
                messages.add_message(request, messages.ERROR, 'User is not active.')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid login details.')
        return redirect('company_login')
    return render(request, 'company_login.html')

def company_register(request):
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        comp_name = request.POST['comp_name']
        email = request.POST['email']
        website = request.POST['website']
        user = User.objects.create_user(username=username, password=password,email=email)
        company = Company.objects.create(user=user, comp_name=comp_name, email=email, website=website)
        login(request, user)
        return redirect('company_dashboard')
     else:
        return render(request, 'company_register.html')
     
def company_dashboard(request):
    username = request.session.get('username')
    email = request.session.get('email')
    user = User.objects.filter(Q(username=username) | Q(email=email)).first()
    if user is not None:
        user_details = {
            'username': user.username,
            'comp_name': user.company.comp_name,
            'email': user.company.email,
            'website': user.company.website,
        }
        return render(request, 'company_dashboard.html', {'user_details': user_details})
    else:
        messages.error(request, 'You are not logged in.')
        return redirect('company_login')


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            request.session['email'] = email 
            return redirect('password_reset_form') 
        else:
            messages.error(request, 'No account with this email exists.')
    return render(request, 'password_reset_request.html')


# views.py
def password_reset_form(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            email = request.session.get('email')  # Get the email from the session
            if email is not None and User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                user.password = make_password(password1)  # Hash the password before saving
                user.save()
                request.session['email'] = email  # Store the email in the session
                messages.success(request, 'Password reset successful.')
                return redirect('company_dashboard')
            else:
                messages.error(request, 'Password reset failed.')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'password_reset_form.html')

def post_job(request):
    company_name = request.GET.get('company')
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        location = request.POST['location']
        is_active = 'is_active' in request.POST
        openings = request.POST['openings']
        email = request.session.get('email')
        company = Company.objects.filter(email=email).first()
        if company is not None:
            Job.objects.create(
                company=company,
                title=title,
                description=description,
                location=location,
                is_active=is_active,
                openings=openings,
            )
            return redirect('company_dashboard')
        else:
            return HttpResponse('Company not found.')
    return render(request, 'job_post.html', {'company_name': company_name})