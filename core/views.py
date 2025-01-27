from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages as message
from datetime import timedelta
from .form import CustomCreateUserForm, SettingsForm, CreateSessionForm
from .models import Exam, Session, SessionNote

'''
    Handler for the login page
'''
def loginPage(request):
    # Navigate User to the dashboard page if they are already authenticated
    if request.user.is_authenticated:
        return redirect("dashboard-analytic")


    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard-analytic")
        else:
            message.error(request, "Email or Password is incorrect")

    context = {"title": "Login"}
    return render(request, "account/login.html", context)

'''
    Handler for the register page
'''
def registerPage(request):
    form  = CustomCreateUserForm()

    # Navigate User to the dashboard page if they are already authenticated
    if request.user.is_authenticated:
        return redirect("dashboard-analytic")

    if request.method == "POST":
        form = CustomCreateUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get("email")
            user.save()

            # Login the user
            login(request, user)

            # Return to the dashboard page
            return redirect("dashboard-analytic")
        else:
            message.error(request, form.errors)

    context = {"form": form, "title": "Register"}
    return render(request, "account/register.html", context)


'''
    Handler for the dashboard analytic page
'''
@login_required(login_url="login")
def dashboardAnalyticPage(request):
    return redirect("dashboard-settings")

'''
    Handler for the sessions page
'''
@login_required(login_url="login")
def sessionsPage(request):
    context = {"title": "Sessions /"}
    return render(request, "dashboard/session/sessions.html", context)

'''
    Handler for the create session page`
'''
@login_required(login_url="login")
def createSession(request):
    exams = Exam.objects.all()
    form  = CreateSessionForm()

    if request.method == "POST":
        exam = Exam.objects.get_or_create(name=request.POST.get("exam"))[0]

        try:
            session = Session.objects.create(name=request.POST.get("name"), exam=exam, user=request.user)
            message.success(request, "Session created successfully")
            return redirect("session-study-time", session_id=session.id)
        except Exception:
            message.error(request, "Something went wrong, please try again")
            return redirect("create-session")

    context = {"title": "Sessions / Create", "form": form, "exams": exams}
    return render(request, "dashboard/session/create-session.html", context)

'''
    Handler for updating a session
'''
@login_required(login_url="login")
def updateSession(request, session_id):
    session = Session.objects.get(id=session_id)
    exams = Exam.objects.all()
    form = CreateSessionForm(instance=session)

    if request.method == "POST":
        try:
            exam = Exam.objects.get_or_create(name=request.POST.get("exam"))[0]
            session.exam = exam
            session.name = request.POST.get("name")
            session.save()
            message.success(request, "Session updated successfully")
            return redirect("session-study-time", session_id=session.id)
        except Exception:
            message.error(request, "Something went wrong, please try again")
            return redirect("update-session", session_id=session_id)

    context = {"title": "Sessions / Update", "form": form, "mode": "Update", "session": session, "exams": exams, "session_id": session_id}
    return render(request, "dashboard/session/create-session.html", context)

'''
    Handler for the session study time page
'''
@login_required(login_url="login")
def sessionStudyTime(request, session_id):
    session = Session.objects.get(id=session_id)


    if request.method == "POST":
        duration_value = request.POST.get('duration')
        hours, minutes, seconds = map(int, duration_value.split(':'))
        duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        session.duration = duration
        session.save()
        return redirect("session-upload-notes", session_id=session_id)

    context = {"title": "Sessions / Study Time", "session_id": session_id, "mode": "Update", "session":session}
    return render(request, "dashboard/session/study-time.html", context)

'''
    Handler for the settings page
'''
@login_required(login_url="login")
def settingsPage(request):
    form = SettingsForm(instance=request.user)

    if request.method == "POST":
        form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if request.FILES.get("avatar"):
                user.avatar = request.FILES.get("avatar")
            user.save()
            message.success(request, "Settings updated successfully")
        else:
            message.error(request, "Something went wrong, please try again")
        # Redirect to the settings page
        return redirect("dashboard-settings")

    context = {"title": "Settings /", "form": form}
    return render(request, "dashboard/setting/settings.html", context)
