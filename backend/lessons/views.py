from rest_framework import generics, permissions, viewsets

from django.shortcuts import render

# Create your views here.

class LessonList(generics.ListCreateAPIView):
	# permission_classes = [IsAuthorOrReadOnly, permissions.IsAuthenticated]
	# queryset = Post.objects.all()
	# serializer_class = PostSerializer
	pass