from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from webapi.models import *
from passlib.hash import django_pbkdf2_sha256 as handler
import jwt
from decouple import config
import webapi.emailpattern as em
from decouple import config
from django.db.models import Q
from django.db.models import F
from django.conf import settings
import webapi.usable as uc
import random
# # Create your views here.

key = 'django-insecure-zqyvd!wcb^gyb6wc5muyq%2=@sf7sa&1i04abpb8g#83bl6@#8'
def empty_key(req_fields,request):
    try:
        for i in req_fields:
            if not i in request.data:
                return False

        return True
    except:
        return False

def empty_fields(req_fields,request):
    try:
        for i in req_fields:
            if len(request.data[i]) == 0:
                return False

        return True
    except:
        return False


def status_check(Start_Date,End_Date):
    current_date = str(date.today())
    if End_Date < current_date:
        return False
    elif Start_Date <= current_date:
        return True
    else:
        print("error")

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
        try:

            checkalready = user.objects.filter(email = request.data['email']).first()
            if checkalready:
                return Response({"status":False,"message":"Email has been Already Taken !"},status=409)
            else:
                email = request.data['email']
                name = request.data['name']
                alias = request.data['alias']
                password = handler.hash(request.data['password'])

                data = user(name = name,alias = alias,email = email,password = password)

                data.save()

                return Response({'status':True, 'message':'Signup Successfully'})


        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))
            return Response(message,status=500)



class login(APIView):

    def post(self,request):
        try:
            req_fields = ['password', 'email']
            check=empty_key(req_fields ,request)
            if check :
                email = request.data['email']
                password = request.data['password']
                myobj = user.objects.filter(email = email).first()  # .first() works as myobj[0].Pass
                if myobj:
                    if handler.verify(password,myobj.password):
                        payload = {
                            'id': myobj.id,
                            # 'pass': myobj.Password
                            }
                        # print(payload)
                        access_token = jwt.encode({"access": payload}, key, algorithm="HS256")
                        return Response({'status':True,'message':"Login successfully",'access': str(access_token)})
                    else:
                        empty_field=empty_fields(req_fields,request)
                        if empty_field:
                            return Response({'status':False,'message':"Try again! Incorrect login credentials"})
                        else:
                            return Response({'status':False,'Required Fields ':req_fields ,'message':"Password Field is Empty "})
                else:
                    empty_field=empty_fields(req_fields,request)
                    if empty_field:
                        return Response({'status':False,'message':"Try again! Incorrect login credentials"})
                    else:
                        return Response({'status':False,'Required Fields ':req_fields ,'message':"Email Field is Empty "})
            else:
                return Response({'status':False,'Required Fields ':req_fields ,'message':"All feilds are required"})




        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))
            return Response(message,status=500)




class forgotPasswordlinkSend(APIView):
    def post(self,request):
        try:
            requireFields = ['email']
            validator = uc.keyValidation(True,True,request.data,requireFields)
            if validator:
                return Response(validator)

            else:
                email = request.data['email']
                fetchuser = user.objects.filter(email = email ).first()
                if fetchuser:
                    token=random.randint(1000,99999)
                    fetchuser.OtpStatus = "True"
                    fetchuser.Otp = token
                    fetchuser.save()
                    em.forgetEmailPattern("forget password",config('EMAIL_HOST_USER'),email,token)
                    return Response({'status':True,'message':"Email send successfully",'id':fetchuser.id})
                    
                
                else:
                    return Response({'status':False,'message':'Email doesnot exist'},status=409)




        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))
            return Response(message,status=500)


class forgettokenCheck(APIView):
    def post(self,request):
        try:
            ##validator keys and required
            requireFields = ['token','id']
            validator = uc.keyValidation(True,True,request.data,requireFields)
            
            if validator:
                return Response(validator)

            else:
                
                token = request.data['token']
                userid = request.data['id']
                checkExist = user.objects.filter(id = userid ).first()
                
                if checkExist:
                    if checkExist.OtpStatus == "True" and checkExist.Otp == int(token):
                        return Response({"status":True,"message":'Access Granted'})

                    else:
                        return Response({'status':False,'message':'Your token is expire'})

                else:
                    return Response({'status':False,'message':'Id is incorrect'})


        except Exception as e:
            message = {'status':False}
            message.update(message=str(e))
            return Response(message,status=500)



class forgetConfirmation(APIView):
    def post(self,request):
        ##validator keys and required
        requireFields = ['password','userid']
        validator = uc.keyValidation(True,True,request.data,requireFields)
        
        if validator:
            return Response(validator)

        #Recive data 
        password = request.POST['password']
        userid = request.POST['userid']

        #Business logic
       
        checkExist = user.objects.filter(id = userid ).first()


        if checkExist:
            ##Password Length Validator
            passwordStatus = uc.passwordLengthValidator(password)
            if not passwordStatus:
                return Response({'status':False,'message':'Password must be 8 characters or less than 20 characters'})

            if checkExist.OtpStatus == "True":
                checkExist.password = handler.hash(password)
                checkExist.OtpStatus = "False"
                checkExist.save()
                return Response({'status':True,'message':'Password Update Successfully'})

            else:
                return Response({'status':False,'message':'Token is expire'},status=403)
                


        else:
            return Response({'status':False,'message':'Id is incorrect'})