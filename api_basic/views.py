from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleModelSerializer
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework import generics
from rest_framework import mixins

from rest_framework.authentication import SessionAuthentication,BasicAuthentication , TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from django.shortcuts import get_object_or_404
# Create your views here.
# @csrf_exempt  # To protect form POST form.

#Viewsets : 

class ArticleViewSet(viewsets.ViewSet):
    def get(self,request):
        articles = Article.objects.all()
        serializer = ArticleModelSerializer(articles,many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = ArticleModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset,pk=pk)
        serializer = ArticleModelSerializer(article)
        return Response(serializer.data)
    
    def update(self,request,pk=None):
        article = Article.objects.get(pk=pk)
        serializer = ArticleModelSerializer(article,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ArticleGViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    serializer_class = ArticleModelSerializer
    queryset = Article.objects.all()

class ArticleMViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleModelSerializer
    queryset = Article.objects.all()

class ArticleAPIView(APIView):
    
    def get(self,request):
        articles = Article.objects.all()
        serializer = ArticleModelSerializer(articles,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ArticleModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def article_list(request):

    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleModelSerializer(articles,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        
        serializer = ArticleModelSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Article_detail_class(APIView):
    def get_object(self,id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request,id):
        article = self.get_object(id)
        serializer = ArticleModelSerializer(article)

        return Response(serializer.data)
    
    def put(self,request,id):
        article = self.get_object(id)
        serializer = ArticleModelSerializer(article,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        article = self.get_object(id)
        article.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)



# To view single article
@api_view(['GET','PUT','DELETE'])
def article_detail(request,pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ArticleModelSerializer(article)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializer = ArticleModelSerializer(article,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# Generic Views : 

class GenericAPIView(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin):

    serializer_class = ArticleModelSerializer
    queryset = Article.objects.all()

    lookup_field = 'id'

    # authentication_classes = [SessionAuthentication,BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id=None):

        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self,request):
        return self.create(request)
    
    def put(self,request,id=None):
        return self.update(request,id)
    
    def delete(self,request,id=None):
        return self.destroy(request,id)

