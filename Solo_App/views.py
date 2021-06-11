from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

## Rendering Views

def index(request):
    context = {
        "user": User.objects.all()
    }
    return render(request, 'index.html', context)

def success(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'likes': Post.objects.all()
    }
    return render(request, 'feed.html', context)

def main(request):
    return render(request, 'main.html')

def archive(request):
    return render(request, 'archive.html')

def users(request):
    images = Upload.objects.all()
    context = {
        "images": images
    }
    return render(request, 'users.html', context)

def feed(request):
    context = {
        'comments': Post.objects.all(),
    }
    return render(request, 'feed.html', context)

def register(request):
    if request.method == "POST":
        errors = User.objects.validation(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect("/")
        name = request.POST['name']
        alias = request.POST['alias']
        email = request.POST['email']
        password = request.POST['password']
        hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(name=name, alias=alias, email=email, password=hash_pw)
    return redirect('/main')

def login_user(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'User email and password dont match.')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    request.session['alias'] = user.alias
    return redirect("/main")

def add_comment(request):
    commenter = User.objects.get(id=request.session['user_id'])
    text = request.POST['comments']
    Post.objects.create(user=commenter, text=text)
    return redirect('/feed')

def like_comment(request, id):
    like_comment = Post.objects.get(id=id)
    user_likes = User.objects.get(id=request.session['user_id'])
    like_comment.user_likes.add(user_likes)
    return redirect('/feed')

def delete(request, id):
    destroyed = Post.objects.get(id=id)
    destroyed.delete()
    return redirect('/feed')

def edit_comment(request, comment_id):
    edit_to_comment = Post.objects.get(id=comment_id)
    context = {
        "comment": edit_to_comment
    }
    return render(request, 'edit-comment.html', context)

def modify_comment(request):
    if request.method == "POST":
        comment_id = request.POST['comment_id']
        new_text = request.POST['comment_text']
        errors = Post.objects.validate_comment(new_text)
        if len(errors) > 0: 
            for key, val in errors.items():
                messages.error(request, val)
            return redirect('/feed')
        comment_to_edit = Post.objects.get(id=comment_id)
        comment_to_edit.text = new_text
        comment_to_edit.save()
        return redirect('/feed')

def add_image(request):
    if request.method == "POST":
        new_file = Upload(file=request.FILES['image'])
        new_file.save()
    return redirect('/users')

def logout(request):
    del request.session['user_id']
    return redirect('/')