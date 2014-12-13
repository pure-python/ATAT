from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseForbidden

from fb.models import UserPost, UserPostComment, UserProfile
from fb.forms import (
    UserPostForm, UserPostCommentForm, UserLogin, UserProfileForm,
)


@login_required
def index(request):
    posts = UserPost.objects.all()
    if request.method == 'GET':
        form = UserPostForm()
    elif request.method == 'POST':
        form = UserPostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            post = UserPost(text=text, author=request.user)
            post.save()

    context = {
        'posts': posts,
        'form': form,
    }
    return render(request, 'index.html', context)


@login_required
def post_details(request, pk):
    post = UserPost.objects.get(pk=pk)

    if request.method == 'GET':
        form = UserPostCommentForm()
    elif request.method == 'POST':
        form = UserPostCommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            comment = UserPostComment(text=cleaned_data['text'],
                                      post=post,
                                      author=request.user)
            comment.save()
            return redirect(reverse('post_details', args=[pk]))

    comments = UserPostComment.objects.filter(post=post)

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }

    return render(request, 'post_details.html', context)


def login_view(request):
    if request.method == 'GET':
        login_form = UserLogin()
        context = {
            'form': login_form,
        }
        return render(request, 'login.html', context)
    if request.method == 'POST':
        login_form = UserLogin(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {
                'form': login_form,
                'message': 'Wrong user and/or password!',
            }
            return render(request, 'login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def profile_view(request, user):
    profile = UserProfile.objects.get(user__username=user)
    context = {
        'profile': profile,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile_view(request, user):
    profile = UserProfile.objects.get(user__username=user)
    if not request.user == profile.user:
        return HttpResponseForbidden()
    if request.method == 'GET':
        data = {
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'gender': profile.gender,
            'date_of_birth': profile.date_of_birth,
        }
        avatar = SimpleUploadedFile(
            profile.avatar.name, profile.avatar.file.read()) \
            if profile.avatar else None
        file_data = {'avatar': avatar}
        form = UserProfileForm(data, file_data)
    elif request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.user.first_name = form.cleaned_data['first_name']
            profile.user.last_name = form.cleaned_data['last_name']
            profile.user.save()

            profile.gender = form.cleaned_data['gender']
            profile.date_of_birth = form.cleaned_data['date_of_birth']
            if form.cleaned_data['avatar']:
                profile.avatar = form.cleaned_data['avatar']
            profile.save()

            return redirect(reverse('profile', args=[profile.user.username]))
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'edit_profile.html', context)


@login_required
def like_view(request, pk):
    post = UserPost.objects.get(pk=pk)
    post.likers.add(request.user)
    post.save()
    return redirect(reverse('post_details', args=[post.pk]))

@login_required
def delete_post(request, pk):
    post = UserPost.objects.get(pk=pk)
    if not request.user == post.author:
        return HttpResponseForbidden()
    else:
        post.delete()
        return redirect('index')

@login_required
def edit_post(request, pk):
    post = UserPost.objects.get(pk=pk)
    if not request.user == post.author:
        return HttpResponseForbidden()
    if request.method == 'GET':
        data = {'text' : post.text}
        form = UserPostForm(data, data)
    elif request.method == 'POST':
        form = UserPostForm(request.POST)
        if form.is_valid():
            post.text = form.cleaned_data['text']
            post.save()
            return redirect('index')

    context = {
        'form': form,
    }
    return render(request, 'edit_post.html', context)

@login_required
def delete_comment(request, pk):
    comment = UserPostComment.objects.get(pk=pk)
    if not request.user == comment.author:
        return HttpResponseForbidden()
    else:
        post_pk = comment.post.pk
        comment.delete()
        return redirect(reverse('post_details', args=[post_pk]))

@login_required
def edit_comment(request, pk):
    comment = UserPostComment.objects.get(pk=pk)
    if not request.user == comment.author:
        return HttpResponseForbidden()
    if request.method == 'GET':
        data = {'text' : comment.text}
        form = UserPostCommentForm(data, data)
    elif request.method == 'POST':
        form = UserPostCommentForm(request.POST)
        if form.is_valid():
            comment.text = form.cleaned_data['text']
            comment.save()
            return redirect(reverse('post_details', args=[comment.post.pk]))
    context = {
        'form': form,
    }
    return render(request, 'edit_comment.html', context)

