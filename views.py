from django.shortcuts import render, redirect
from .models import Registration
from django.contrib import messages
import bcrypt

hash1 = bcrypt.hashpw('test'.encode(), bcrypt.gensalt())

def index(request):
    if 'fName' not in request.session:
        request.session['fName'] = " "
    return render(request, "logReg/index.html")

def success(request):

    return render(request, 'logReg/success.html')

def checkLogin(request):
    if (request.method == "POST") & (request.POST['hidden'] == "Register"):
        errors = Registration.objects.basic_validator(request.POST)

        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        else:
            inputFirstName = request.POST['fName']
            inputLastName = request.POST['lName']
            inputEmail = request.POST['email']
            inputPassword = request.POST['password']
            if inputPassword == request.POST['password']:
                encryptedPW = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            Registration.objects.create(first_name=inputFirstName, last_name=inputLastName, email=inputEmail, password=encryptedPW)
            messages.success(request, "Successfully Registered!")
            request.session["fName"] = inputFirstName
            return redirect("/success")

    if (request.method == "POST") & (request.POST['hidden'] == "Login"):
        errors = {}
        logEmail = Registration.objects.filter(email=request.POST['LEmail'])
        if bcrypt.checkpw(request.POST['LPassword'].encode(), logEmail[0].password.encode()):
            messages.success(request, "You're logged in!")
            return redirect("/success")
        else:
            errors['confirmPW'] = "That password or e-mail did not match"
            return redirect('/')