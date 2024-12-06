from django.shortcuts import render
from apiApp.models import Register, Login, CommandExecutingLog
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
import random
import paramiko
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings
from apiApp.serializers import RegisterSerializer, LoginSerializer, CommandExecutingLogSerializer
from datetime import datetime
from django.http import JsonResponse
import logging


def send_otp(email):
   otp = str(random.randint(100000,999999))
   send_mail(
      'Your OTP code',
      f'Your OTP code is {otp}',
      settings.EMAIL_HOST_USER,
      [email],
      fail_silently=False
   )
   return otp



class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        try:
            user = Register.objects.get(email=email)
            
            if user and check_password(password, user.password):
                otp = send_otp(email) 

                request.session["email"] = email

                return JsonResponse({"otp": otp}, status=200)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except Register.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)



class DeleteAllLoginUsers(APIView):
   def delete(self, request):
      try:
         deleted_count,_ = Login.objects.all().delete()
         return Response(status=status.HTTP_204_NO_CONTENT)
      except Exception as e:
         return Response(status=status.HTTP_400_BAD_REQUEST)

      

class LoginDetails(APIView):
   def get_object(self,pk):
      try:
         return Login.objects.get(pk=pk)
      except Login.DoesNotExist:
         return Http404
   def get(self,request,pk):
      user = self.get_object(pk)
      serializer = LoginSerializer(user)
      return Response(serializer.data)
   
   def delete(self,request,pk):
      user = self.get_object(pk)
      user.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterView(APIView):
   def get(self,request):
      regusers = Register.objects.all()
      serializer = RegisterSerializer(regusers, many=True)
      return Response(serializer.data)
   def post(self, request):
      serializer = RegisterSerializer(data= request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RegisterDetails(APIView):
   def get_object(self,pk):
      try:
         return Register.objects.get(pk=pk)
      except Register.DoesNotExist:
         return Http404
      
   def get(self,request,pk):
      user = self.get_object(pk)
      serializer = RegisterSerializer(user)
      return Response(serializer.data)      
   def delete(self,request,pk):
      user = self.get_object(pk)
      user.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)




class ResendOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if email:
           try:
              new_otp = send_otp(email)

              logging.info(f"New OTP generated and sent:{new_otp}")

              return JsonResponse({"new_otp": new_otp, "success":True},status=200)
           except Exception as e:
              logging.error(f"Error sending OTP:{str(e)}")

              return JsonResponse({"success": False, "error": "Failed to sent new OTP, Please try Again"},status=500)
        else:
           logging.error("Email not Found in Session")

           return JsonResponse({"success":False, "error":"Email Not Found in Session."})



class CommandExecutionView(APIView):

    def post(self, request):
        serializer = CommandExecutingLogSerializer(data=request.data)
        if serializer.is_valid():
            hostname = serializer.validated_data['hostname']
            username = serializer.validated_data['username']
            command = serializer.validated_data['command']
            password = serializer.validated_data['password']  
        try:
      
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

           
            ssh.connect(hostname=hostname, username=username, password=password, timeout=10)

          
            print("SSH connection established successfully.")
            
           
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

           
            print(f"Command output: {output}")
            print(f"Command error: {error}")

           
            ssh.close()

         
            command_execution = CommandExecutingLog.objects.create(
               hostname=hostname,
               username=username,
               command=command,
               output=output,
               error=error
            )
            command_execution.save()

            
            return Response(CommandExecutingLogSerializer(command_execution).data, status=status.HTTP_201_CREATED)

        except paramiko.AuthenticationException:
            return Response({"error": "Authentication failed, please verify your credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except paramiko.SSHException as ssh_exception:
            return Response({"error": f"Failed to establish SSH connection: {str(ssh_exception)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
           
            print(f"General error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      