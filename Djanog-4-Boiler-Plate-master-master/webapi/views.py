from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from webapi.models import *
from passlib.hash import django_pbkdf2_sha256 as handler
# # Create your views here.



class crud(APIView):

    def get(self, request):
        data = Super_AdminAccount.objects.values('Fname','Lname','Email','Username','Role','Profile','Password')

        return Response({'status':True, 'data':data})


    def post(self, request):
        fname = request.data['Fname']
        lname = request.data['Lname']
        email = request.data['Email']
        username = request.data['Username']
        password = handler.hash(request.data['Password'])
        contact = request.data['ContactNo']
        role = request.data['Role']
        profile = request.data['Profile']
      
        data = Super_AdminAccount(Fname = fname,Lname = lname,Email = email,Username = username,Password = password,ContactNo =contact,Role = role,Profile = profile)

        data.save()

        return Response({'status':True, 'msg':'added successfully'})



class userprofile(APIView):

    def get(self, request):
        data = user.objects.values('name','alias','email','password')

        return Response({'status':True, 'data':data})


    def post(self, request):
        name = request.data['name']
        alias = request.data['alias']
        email = request.data['email']
        password = handler.hash(request.data['password'])
              
        data = user(name = name,alias = alias,email = email,password = password)

        data.save()

        return Response({'status':True, 'msg':'added successfully'})





