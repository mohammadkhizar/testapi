from django.urls import path,include
from webapi.views import *

urlpatterns = [

#web urls  home
path('superadmin',crud.as_view()),
path('usr',userprofile.as_view()),




]






