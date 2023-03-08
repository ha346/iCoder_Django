from django.urls import path 
from . import views

urlpatterns = [ 
#  API to post a comment
 path('postblog/', views.post, name='post'), 
 path('submitpost', views.submitPost, name='submitpost'), 
 path('postComment', views.postComment, name="postComment"),
 path('', views.blogHome, name='bloghome'),
 path('<str:slug>', views.blogPost, name='blogPost'), 
#  path('blogpost', views.blogPost, name='blogpost'), 

     
]