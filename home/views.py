from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from .models import role, role_and_user_connex, enquete, questions, reponses, responseSelection, enqueteResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import enqueteForm, questionForm, responseForm


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
            # Creates the user and saves to User 
            new_user = User.objects.create_user(first_name = first_name, last_name = last_name, email = email, username = username, password = password1)
            new_user.save()
            # Gets the role id from the template
            new_user_role = role.objects.get(id = int(roleID))
            new_user_role.save()

            new_user_role_connection = role_and_user_connex.objects.create(userID = new_user, roleID = new_user_role)
            new_user_role_connection.save()
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

#region Admin Views

# Everything connected to the homepage of admin, names in templates and all
@login_required
def home_admin(request):
    context = {
        'enquetes' : enquete.objects.all()
    }
    return render(request, 'admin/main_admin.html', context)

# This creates and saves the enquete for the admin
@login_required
def create_enquete(request):
    if request.method == 'POST':
        form = enqueteForm(request.POST)
        if form.is_valid():
            # Create an instance of enquete via enqueteForm and saves it without commiting
            enquete = form.save(commit= False)
            
            # Fill the userID instance otherwise it won't get saved
            enquete.userID = request.user
            
            # Get user role of the user
            user_role = role_and_user_connex.objects.get(userID= request.user)
            enquete.roleID = user_role.roleID

            # Commit the instance with the userID and roleID
            enquete.save()
            return redirect('home_admin')
        else:
            form = enqueteForm()
    context = {
        'form' : enqueteForm,
    }
    return render(request, 'admin/enquete_creation.html', context)

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
def enqueteDelete_admin(request, pk):
    
    # Getting the instance to delete from the database
    enquete_instance = enquete.objects.get(id = pk)
    
    # Deleting the instance
    if request.method == 'POST':
        enquete_instance.delete()
        return redirect ('home_admin')
    return render(request, 'admin/delete.html')



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

# View all the questions and answers of an enquete for admin
@login_required
def view_admin(request, pk):
    
    # Gets the enquete instance that has questions
    enquete_instance = enquete.objects.get(id = pk)

    # Gets all the questions of a specific enquete using related name that can give access of questions to enquete
    all_questions = enquete_instance.questions.all() # is like questions.objects.filter(enqueteID = enquete_instance) which is automatically made and you can use it with the related name
    
    # Get the enquete id from the enquete_needed(this will be a number). Otherwise it's gonna see all the instances instead and we only need the id
    enqueteID = enquete_instance.id

    context = {
        'all_questions' : all_questions,
        'enqueteID' : enqueteID,
    }
    return render (request, 'admin/view_enquete.html', context)

@login_required
def addQuestion_admin(request, pk):
    # Getting the enquete instance including id
    enqueteID = enquete.objects.get(id = pk)  
    context = {
        'questionForm' : questionForm
    }
    # Adding instance to the form
    if request.method == 'POST':
        qForm = questionForm(request.POST)
        
        if qForm.is_valid():
            # Saving the instance but not commiting it
            questions = qForm.save(commit = False)
            
            # Adding value to the enqueteID which is the enquete instance we got before
            questions.enqueteID = enqueteID
            
            # Commiting it
            questions.save()
            return redirect ('view_enquete_admin', pk = pk)  # Needs a pk cause the link has a pk
        else :
           qForm = questionForm()
           
    # Gets the website cause it's a GET method 
    else:
        return render (request, 'admin/question_creation.html', context)
    
# Edit question instance
@login_required
def updQuestion_adm(request, pk):
    
    # Gets instance to edit
    question_instance = questions.objects.get(id = pk)
    
    # Gets enquete instance to comeback to the view_enquete_admin
    enquete_instance = question_instance.enqueteID
    
    # Getting the form
    qForm = questionForm(instance= question_instance)
    
    # Edit instance
    if request.method == 'POST':
        qForm = questionForm(request.POST, instance= question_instance)
        if qForm.is_valid():
            qForm.save()
            return redirect('view_enquete_admin', pk = enquete_instance)
        else:
            qForm = questionForm(instance= question_instance)  
    context = {
        'questionForm' : qForm
    }
    return render (request, 'admin/question_creation.html', context) 

@login_required
def deleteQuestion_adm(request, pk):
    questionInstance = questions.objects.get(id = pk)
    enqueteInstance = questionInstance.enqueteID
    enqueteID = enqueteInstance.id
    if request.method == 'POST':
        questionInstance.delete()
        return redirect ('view_enquete_admin', pk = enqueteID)
    
    context = {
        'enqueteID' : enqueteID
    }
    return render (request, 'admin/delete_question.html', context)

@login_required
# Creates responses
def addResponse_admin(request, pk):
    # get question instance to add responses to
    question_instance = questions.objects.get(id = pk)

    enqueteID = question_instance.enqueteID.id
    
    # add reponses
    if request.method == 'POST':
        # Stores the data from the form inside a variable otherwise it will be useless (garbage collection)
        data = responseForm(request.POST)
        if data.is_valid():
            # saves the data without commiting it
            instance =  data.save(commit= False)
            # adding data to questionID
            instance.questionID = question_instance
            # save and commit everything to create an instance to the database
            instance.save()
            return redirect ('view_enquete_admin', pk = enqueteID)
        
    context = {
        'responseForm' : responseForm,
    }
    return render(request, 'admin/addResponse.html', context)

#endregion

#region Enqueteur Views

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
            
            # Get user role of the user
            user_role = role_and_user_connex.objects.get(userID=request.user)
            enquete.roleID = user_role.roleID


            # Commit the instance with the userID and role
            enquete.save()
            
            return redirect('home_enqueteur')
        else:
            form = enqueteForm()
    context = {
        'form' : enqueteForm,
    }
    return render(request, 'enqueteur/enquete_creation_enqueteur.html', context)

@login_required
# Update enquete for enqueteur
def enqueteUPD_enqueteur(request, pk):
    # Gets the existing instance
    enquete_instance = enquete.objects.get(id = pk)
    
    if request.method == 'POST':
        
        # Updates the instance but not saving it yet, just in the memory and putting that instance into a form
        upd_enquete = enqueteForm(request.POST, instance= enquete_instance ) 
        
        # Saves it
        if upd_enquete.is_valid():
            upd_enquete.save()
            return redirect ('home_enqueteur')
    else:
        # Shows the instance in a form cause this is a get method
        upd_enquete = enqueteForm(instance= enquete_instance)
    context = {
        'form' : upd_enquete
    }
    return render(request, 'enqueteur/enquete_creation_enqueteur.html', context)
    
@login_required
def enqueteDelete_enqueteur(request, pk):
    
    # Getting the instance to delete from the database
    enquete_instance = enquete.objects.get(id = pk)
    
    # Deleting the instance
    if request.method == 'POST':
        enquete_instance.delete()
        return redirect ('home_enqueteur')
    return render(request, 'enqueteur/delete.html')

# View all the questions and answers of an enquete for enqueteur
@login_required
def view_enqueteur(request, pk):
    # Gets the instance i need
    enquete_instance = enquete.objects.get(id = pk)
    
    # Gets instance id for template
    enqueteID = enquete_instance.id
    
    # Filter the questions instances by the enquete instance and gets all of them
    all_questions = enquete_instance.questions.all()
    
    context = {
        'all_questions' : all_questions,
        'enqueteID' : enqueteID
    }
    return render (request, 'enqueteur/view_enquete.html', context)

# Adds questions to enqueteur
@login_required
def addQuestion_enqueteur(request, pk):
    context = {
        'questionForm' : questionForm
    }
    # Gets the enquete instance to add questions to
    enquete_instance = enquete.objects.get(id = pk)
    
    # Add question to that instance
    if request.method == 'POST':
        qForm = questionForm(request.POST)
        
        if qForm.is_valid():
            #Saves but no commit
            qForm.save(commit= False)
        
            # Adds the enquete instance
            qForm.enqueteID = enquete_instance
        
            # Saves
            qForm.save()
            return redirect ('view_enquete_enqueteur', pk = pk)
        else:
            qForm = questionForm()
    else:        
        return render (request, 'enqueteur/question_creation.html', context)

# Edit question instance
@login_required
def updQuestion_enqueteur(request, pk):
    
    # Gets instance to edit
    question_instance = questions.objects.get(id = pk)
    
    # Gets enquete instance to comeback to view_enqueteur
    enquete_instance = question_instance.enqueteID

    # Getting the form
    qForm = questionForm(instance= question_instance)
    
    # Edit instance
    if request.method == 'POST':
        qForm = questionForm(request.POST, instance= question_instance)
        if qForm.is_valid():
            qForm.save()
            return redirect('view_enquete_enqueteur', pk = enquete_instance.id)
        else:
            qForm = questionForm(instance= question_instance)  
    context = {
        'questionForm' : qForm
    }
    return render (request, 'enqueteur/question_creation.html', context) 

@login_required
def deleteQuestion_enqueteur(request, pk):
    questionInstance = questions.objects.get(id = pk)
    enqueteInstance = questionInstance.enqueteID
    enqueteID = enqueteInstance.id
    if request.method == 'POST':
        questionInstance.delete()
        return redirect ('view_enquete_enqueteur', pk = enqueteID)
    
    context = {
        'enqueteID' : enqueteID
    }
    return render (request, 'enqueteur/delete_question.html', context)



@login_required
# Creates answers for equeteur
def addResponses_enqueteur(request, pk):

    #Gets question to add response to
    question_instance = questions.objects.get(id = pk)

    #Gets enquete.id for redirection
    enquete_instance = question_instance.enqueteID
    enqueteID = enquete_instance.id

    if request.method == 'POST':
        # Gets the data from the form
        data = responseForm(request.POST)
        if data.is_valid():
            # Changing questionID from none to question_instance
            instance = data.save(commit = False)
            instance.questionID = question_instance
            instance.save()
            return redirect ('view_enquete_enqueteur', pk = enqueteID)
        else:
            data = responseForm()
    return render (request, 'enqueteur/addResponse.html')

#endregion

#region Participants
# Page which new participants land on
def welcomePage(request):
    return render(request, 'welcome.html')

# List all the enquetes participants can take
def enqueteList(request):
    # Gets all enquetes
    all_items = enquete.objects.all()

    context = {
        'enquetes' : all_items
    }
    return render (request, 'participants/enqueteList.html', context)

# Direct participants to the survey
def survey(request, pk):
    #Gets enquete to participate on
    enquete_instance = enquete.objects.get(id = pk)

    #Gets questions of that enquete instance.
    all_questions = enquete_instance.questions.all()

    if request.method == 'POST':
        # Gets all the data from the form submission

        # Gets the question ids list from the form created from the browser using array list
        questionIDs = request.POST.getlist('question.id[]') # we get a list of question ids
        print(questionIDs)

        # Grts the comment from the form
        comment = request.POST['responseComment']
        # Gets the email from the form
        email = request.POST['email']

        for qID in questionIDs:
            # Gets the question instance
            question_instance = questions.objects.get(id = qID)
            
            selectedOptions = request.POST.getlist(f'options_{qID}[]') # we get a list of all responses ids for every questions
            print(selectedOptions)

            if selectedOptions:
                reponse_obj = reponses.objects.create(
                    questionID = question_instance,
                    response_comment = comment
                )
                reponse_obj.responseSelectionID.set(selectedOptions)
                reponse_obj.save()
                print(reponse_obj.responseSelectionID)
    context = {
        'all_questions': all_questions,
    }
    return render(request, 'participants/survey.html', context)

def thanksPage(request):
    return render (request, 'participants/thanksPage.html')

#endregion