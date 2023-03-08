from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post,BlogComment
from django.contrib import messages
from django.contrib.auth import login 
# Create your views here.

def blogHome(request):
    allposts=Post.objects.all()
    context={'allposts':allposts}
    return render(request,"blog/blogHome.html",context)

def blogPost(request,slug):
    # return HttpResponse(f"This is blogpost: {slug}")
    post=Post.objects.filter(slug=slug).first()
    comments=BlogComment.objects.filter(post=post,parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context={'post':post,'comments':comments,'user':request.user,'replyDict':replyDict}
    return render(request,"blog/blogPost.html",context)

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno=request.POST.get("parentSno")
        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent=BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment=comment,user=user,post=post,parent=parent)
            comment.save()
            messages.success(request,"Your reply has been posted successfully")
            
    return redirect(f"/blog/{post.slug}")

def post(request): 
    return render(request,"blog/post.html")

def submitPost(request):  
    if request.method=="POST":
        slug=request.POST['heading']
        title=request.POST['title']
        content=request.POST['content'] 
        author=request.POST['author'] 
        if len(slug)<5 or len(title)<5 or len(content)<10 or len(author)<5:
            messages.error(request, "The heading must contain 5 characters, title must contain 5 characters, author name must contain 5 characters and content must contain 10 characters.")
        else:
            post=Post(slug=slug, title=title, content=content, author=author)
            post.save()
            messages.success(request, "Your post has been successfully saved")
    return render(request,"blog/post.html")

