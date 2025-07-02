"""
URL configuration for file_sharing_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import FileUploadView, ClientSignupView,SecureDownloadView,CustomLoginView,SendVerificationEmailView, VerifyEmailView,SingleFileDownloadView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
    path('api/signup/', ClientSignupView.as_view(), name='client-signup'),
    path('api/download/<str:token>/', SecureDownloadView.as_view(), name='secure-download'),
    path('api/login/', CustomLoginView.as_view(), name='login'),
     path('api/send-verification/', SendVerificationEmailView.as_view(), name='send-verification'),
    path('api/verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
     path('api/download/<str:token>/<int:file_id>/', SingleFileDownloadView.as_view(), name='download-one'),
]
