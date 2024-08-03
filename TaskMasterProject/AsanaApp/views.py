from django.shortcuts import render,get_object_or_404
from .serializers import UserSerializer,ProjectSerializer,TeamSerializer,TaskSerializer,CommentSerializer,RegisterSerializer
from .models import Project,Team,Task,Comment
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

import jwt,datetime
# Create your views here.

class UserSignup(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Signup Successfull'},status=status.HTTP_200_OK)
        return Response({'message':'something went wrong! Signup again'},status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({'msg':'User does not Exist! try again or Signup '},status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({'msg':'Invalid! Try another password'},status=status.HTTP_400_BAD_REQUEST)
        login(request,user)
        payload = {
            'id': user.id,
            'iat':datetime.datetime.now(datetime.UTC),
            'exp':datetime.datetime.now(datetime.UTC)+datetime.timedelta(minutes=120)
        }
        token = jwt.encode(payload,'cap_01',algorithm='HS256')
        response = Response()
        response.data = ({'message':'login Successfull','token':token})
        response.status = status.HTTP_200_OK
        response.set_cookie(
            key= 'jwt',
            value=token,
            samesite=False,
            httponly= None,
            secure=None
        )
        return response

class UserLogout(APIView):

    def post(self,request):
        logout(request)        
        response = Response()
        response.data = {'message':'logout Successfull'}
        response.status = status.HTTP_200_OK
        response.delete_cookie('jwt')
        return response
    
class TeamListCreate(APIView):
    def get(self,request):
        teams = Team.objects.all()
        serializer=TeamSerializer(teams,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer= TeamSerializer(data=request.data)
        # print('line 68', serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Team Created'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class TeamDetail(APIView):
    def getObject(self,pk):
        try:
            team = Team.objects.get(id=pk)
            return team
        except Team.DoesNotExist:
            return Response({'message':'Team not Exist'})
    
    def get(self,request,pk):
        team = self.getObject(pk)
        serializer = TeamSerializer(team)
        return Response(serializer.data)
    
    def put(self,request,pk):
        team = self.getObject(pk)
        serializer = TeamSerializer(team,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        team = self.getObject(pk)
        team.delete()
        return Response({'message':'Team Deleted'},status=status.HTTP_204_NO_CONTENT)
    
class ProjectCreate(APIView):

    def get(self,request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects,many= True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Project Created'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class ProjectDetail(APIView):

    def get(self,request,pk):
        project = get_object_or_404(Project,pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        project = get_object_or_404(Project,pk=pk)
        serializer = ProjectSerializer(project,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Project Updated'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        project = get_object_or_404(Project,pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TaskCreate(APIView):

    def get(self,request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks,many= True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'task Created'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class TaskDetail(APIView):

    def get(self,request,pk):
        tasks = get_object_or_404(Task,pk=pk)
        serializer = TaskSerializer(tasks)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        tasks = get_object_or_404(Task,pk=pk)
        serializer =TaskSerializer(tasks,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'task Updated'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        tasks = get_object_or_404(Task,pk=pk)
        tasks.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CommentCreate(APIView):

    def get(self,request):
        comments= Comment.objects.all()
        serializer = CommentSerializer(comments,many= True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'project Created'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class CommentDetail(APIView):

    def get(self,request,pk):
        comments = get_object_or_404(Comment,pk=pk)
        serializer = CommentSerializer(comments)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        comments= get_object_or_404(Comment,pk=pk)
        serializer =CommentSerializer(comments,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Comment Updated'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        comments = get_object_or_404(Comment,pk=pk)
        comments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)