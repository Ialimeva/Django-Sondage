from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from .models import role, role_and_user_connex, enquete
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import enqueteForm


def registration(request):
    all_roles = role.objects.all()
    context = {
        'all_roles': all_roles
    }
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        roleID = request.POST['roleID']  
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            new_user = User.objects.create_user(first_name = first_name, last_name = last_name, email = email, username = username, password = password1)
            new_user.save()

            new_user_role = role.objects.get(id = int(roleID))
            new_user_role.save()

            new_user_role_connection = role_and_user_connex.objects.create(userID = new_user, roleID = new_user_role)
            new_user_role_connection.save()
        return render(request, 'register.html', context)
    return render(request, 'register.html', context)

def login(request):
    context = {
        'all_roles' : role.objects.all()
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role_name = request.POST['role']
        user = auth.authenticate(username = username, password = password, role = role_name)

        if user is not None:
            if role_name == 'Admin':
                auth.login(request, user)
                return redirect('home_admin')
            elif role_name == 'Enqueteur':
                auth.login(request, user)
                return redirect('home_enqueteur')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'login.html', context)

@login_required
def home_admin(request):
    context = {
        'enquetes' : enquete.objects.all()
    }
    return render(request, 'admin/main_admin.html', context)

@login_required
def home_enqueteur(request):
    return render(request, 'enqueteur/home_enqueteur.html')

@login_required
def create_enquete(request):
    if request.method == 'POST':
        form = enqueteForm(request.POST)
        if form.is_valid():
            # Create an instance of enquete via enqueteForm and saves it without commiting
            enquete = form.save(commit= False)
            # Fill the userID instance
            enquete.userID = request.user
            # Commit the instance with the userID
            enquete.save()
            return redirect('home_admin')
        else:
            form = enqueteForm()
    context = {
        'form' : enqueteForm
    }
    return render(request, 'admin/enquete_creation.html', context)