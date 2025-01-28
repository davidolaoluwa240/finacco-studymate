from django.urls import path
from . import views

urlpatterns = [
    # Dashboard Paths
    path("", views.dashboardAnalyticPage, name="dashboard-analytic"),

    # Session Paths
    path("sessions/", views.sessionsPage, name="dashboard-sessions"),
    path("sessions/create-time", views.createSession, name="create-session"),
    path("sessions/update-time/<str:session_id>", views.updateSession, name="update-session"),
    path("sessions/study-time/<str:session_id>", views.sessionStudyTime, name="session-study-time"),
    path("sessions/upload-notes/<str:session_id>", views.sessionUploadNotes, name="session-upload-notes"),

    # Authentication Paths
    path("login/", views.loginPage, name="login"),
    path("register/", views.registerPage, name="register"),

    # Settings Paths
     path("settings/", views.settingsPage, name="dashboard-settings"),
]
