from django.urls import path,include
from webapi.views import *

urlpatterns = [

#web urls  home
path('superadmin',crud.as_view()),
path('usr',userprofile.as_view()),
path('login',login.as_view()),
path('forgotPasswordlinkSend',forgotPasswordlinkSend.as_view()),
path('forgettokenCheck',forgettokenCheck.as_view()),
path('forgetConfirmation',forgetConfirmation.as_view()),



]
