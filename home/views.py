from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from .models import role, role_and_user_connex, enquete, questions
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import enqueteForm, questionForm


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

# Everything connected to the homepage of admin, names in templates and all
@login_required
def home_admin(request):
    context = {
        'enquetes' : enquete.objects.all()
    }
    return render(request, 'admin/main_admin.html', context)

# Same but in the enqueteur homepage
@login_required
def home_enqueteur(request):
    # Get all the enquete of the user (and filter it so the enqueteur sees their enquetes)
    userID = request.user
    all_enquete = enquete.objects.filter(userID = userID)
    context = {
            'all_enquete' : all_enquete
    }
    return render(request, 'enqueteur/home_enqueteur.html', context)

# This creates and saves the enquete for the admin
@login_required
def create_enquete(request):
    if request.method == 'POST':
        form = enqueteForm(request.POST)
        if form.is_valid():
            # Create an instance of enquete via enqueteForm and saves it without commiting
            enquete = form.save(commit= False)
            
            # Fill the userID instance
            enquete.userID = request.user
            
            # Get user roleID and role_name
            user_role = role_and_user_connex.objects.get(userID= request.user)
            enquete.roleID = user_role.roleID

            # Commit the instance with the userID
            enquete.save()
            return redirect('home_admin')
        else:
            form = enqueteForm()
    context = {
        'form' : enqueteForm,
    }
    return render(request, 'admin/enquete_creation.html', context)

# This creates and save the enquete for the enqueteur. The roleID is not used here btw, just there cause otherwise it won't save and have an error
@login_required
def create_enquete_enqueteur(request):
    if request.method == 'POST':
        form = enqueteForm(request.POST)
        if form.is_valid():
            # Create an instance of enquete via enqueteForm and saves it without commiting
            enquete = form.save(commit= False)
            
            # Fill the userID instance
            enquete.userID = request.user
            
            # Get user roleID and role_name
            user_role = role_and_user_connex.objects.get(userID=request.user)
            enquete.roleID = user_role.roleID


            # Commit the instance with the userID
            enquete.save()
            
            return redirect('home_enqueteur')
        else:
            form = enqueteForm()
    context = {
        'form' : enqueteForm,
    }
    return render(request, 'enqueteur/enquete_creation_enqueteur.html', context)

@login_required
# Update enquete for admin
def enqueteUPD_admin(request, pk):
    # Gets the existing instance from template pk
    enquete_instance = enquete.objects.get(id = pk)
    
    if request.method == 'POST':
        # Updates the instance but not saving it yet, just in the memory
        upd_enquete = enqueteForm(request.POST, instance= enquete_instance )
        
        # Saves it
        if upd_enquete.is_valid():
            upd_enquete.save()
            return redirect ('home_admin')
    else:
        # Just keeps the former instance cause you did nothing with it
        upd_enquete = enqueteForm(instance= enquete_instance)                                            
    context = {
            'form' : upd_enquete
    }
    return render(request, 'admin/enquete_creation.html', context)

@login_required
# Update enquete for enqueteur
def enqueteUPD_enqueteur(request, pk):
    # Gets the existing instance
    enquete_instance = enquete.objects.get(id = pk)
    
    if request.method == 'POST':
        
        # Updates the instance but not saving it yet, just in the memory
        upd_enquete = enqueteForm(request.POST, instance= enquete_instance ) 
        
        # Saves it
        if upd_enquete.is_valid():
            upd_enquete.save()
            return redirect ('home_enqueteur')
    else:
        # Just resend the former instance back
        upd_enquete = enqueteForm(instance= enquete_instance)
    context = {
        'form' : upd_enquete
    }
    return render(request, 'enqueteur/enquete_creation_enqueteur.html', context)
    
    
@login_required
def enqueteDelete_admin(request, pk):
    
    # Getting the instance to delete from the database
    enquete_instance = enquete.objects.get(id = pk)
    
    # Deleting the instance
    if request.method == 'POST':
        enquete_instance.delete()
        return redirect ('home_admin')
    return render(request, 'admin/delete.html')

@login_required
def enqueteDelete_enqueteur(request, pk):
    
    # Getting the instance to delete from the database
    enquete_instance = enquete.objects.get(id = pk)
    
    # Deleting the instance
    if request.method == 'POST':
        enquete_instance.delete()
        return redirect ('home_enqueteur')
    return render(request, 'enqueteur/delete.html')

# View all the questions and answers of an enquete for admin
@login_required
def view_admin(request, pk):
    # Gets all the questions of a specific enquete using pk arg that we got from urls
    all_questions = questions.objects.filter(enqueteID = pk)
    enquete_needed = enquete.objects.get(id = pk)
    enqueteID = enquete_needed.id
    questions.enqueteID = enqueteID
    context = {
        'all_questions' : all_questions,
        'enqueteID' : questions.enqueteID
    }
    return render (request, 'admin/view_enquete.html', context)

# View all the questions and answers of an enquete for enqueteur
@login_required
def view_enqueteur(request, pk):
    return render (request, 'enqueteur/view_enquete.html')


@login_required
def addQuestion_admin(request, pk):
    
    enqueteID = enquete.objects.get(id = pk)
    # Adding instance to the form
    if request.method == 'POST':
        qForm = questionForm(request.POST)
        
        if qForm.is_valid():
            questions = qForm.save(commit = False)
            questions.enqueteID = enqueteID
            questions.save()
            return redirect ('view_enquete_admin', pk = pk)
        else :
            qForm = questionForm()
    context = {
        'questionForm' : questionForm
    }
    return render (request, 'admin/question_creation.html', context)

    
    
        
    