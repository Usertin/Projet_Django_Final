from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import UserProfile , Transport ,  Recommandation , Evenement , Stage , Logement

from .models import TransportRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, UserProfile
from .forms import PostForm

from django.db import transaction

from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, UserProfile
from .forms import PostForm

from django.shortcuts import render, redirect
from .models import TransportRequest
from .forms import TransportRequestForm

def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('profile_page')
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_user.html', {'form': form})


@login_required
def index(request):
    pending_requests = TransportRequest.objects.filter(post__user=request.user).exists()
    transport_requests = TransportRequest.objects.filter(post__user=request.user)
    return render(request, 'index.html', {'pending_requests': pending_requests, 'transport_requests': transport_requests})

@login_required
def profile_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profilepage.html', {'user_profile': user_profile})


@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-date')
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'post_list.html', {'posts': posts, 'user_profile': user_profile})

def profile_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, pk=user_id)
    return render(request, 'profile_page.html', {'user_profile': user_profile})

@login_required
def create_post(request):
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        image = request.FILES.get('image')
        date_posted = request.POST.get('date')
        post = Post.objects.create(
            user=request.user,
            image=image,
            post_type=post_type,
            date=date_posted if date_posted else date.today()
        )
        if post_type == 'Evenement':
            intitule = request.POST.get('intitule')
            description = request.POST.get('description_evenement')
            lieu = request.POST.get('lieu')
            contact_info = request.POST.get('contact_info_evenement')
            subtype = request.POST.get('subtype')

            evenement = Evenement.objects.create(
                post=post,
                intitule=intitule,
                description=description,
                lieu=lieu,
                contact_info=contact_info,
                subtype=subtype
            )

        elif post_type == 'Stage':
            typeStg = request.POST.get('typeStg')
            societe = request.POST.get('societe')
            duree = request.POST.get('duree')
            subject = request.POST.get('subject')
            contactInfo_stage = request.POST.get('contactInfo_stage')

            stage = Stage.objects.create(
                post=post,
                typeStg=typeStg,
                societe=societe,
                duree=duree,
                subject=subject,
                contactInfo=contactInfo_stage
            )

        elif post_type == 'Logement':
            localisation = request.POST.get('localisation')
            description = request.POST.get('description_logement')
            contactInfo_logement = request.POST.get('contactInfo_logement')

            logement = Logement.objects.create(
                post=post,
                localisation=localisation,
                description=description,
                contactInfo=contactInfo_logement
            )

        elif post_type == 'Transport':
            depart = request.POST.get('depart')
            destination = request.POST.get('destination')
            heure_dep = request.POST.get('heure_dep')
            nbreSieges = request.POST.get('nbreSieges')
            contactInfo_transport = request.POST.get('contactInfo_transport')

            transport = Transport.objects.create(
                post=post,
                depart=depart,
                destination=destination,
                heure_dep=heure_dep,
                nbreSieges=nbreSieges,
                contactInfo=contactInfo_transport
            )

        elif post_type == 'Recommandation':
            text = request.POST.get('text')

            recommandation = Recommandation.objects.create(
                post=post,
                text=text
            )

        return redirect('post_detail', post_id=post.id)
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        return render(request, 'create_post.html', {'user_profile': user_profile})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'post_detail.html', {'post': post, 'user_profile': user_profile})


@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if post.post_type == 'Evenement':
                post.evenement.subtype = request.POST.get('subtype', None)
            post.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'update_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('post_list')
    return render(request, 'delete_post.html', {'post': post})


from django.shortcuts import render, redirect
from .models import Post, Reaction

def post_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Reaction.objects.filter(post=post)
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            pass

    return render(request, 'post_comment.html', {'post': post, 'comments': comments, 'user_profile': user_profile})

def add_comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        comment_text = request.POST.get('comment')
        user = request.user
        if comment_text:
            reaction = Reaction.objects.create(post=post, user=user, comment=comment_text)
    return redirect('post_comment', post_id=post_id)


from django.http import HttpResponseRedirect

def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        liked_posts = request.session.get('liked_posts', [])
        if post_id in liked_posts:
            liked_posts.remove(post_id)
            post.likes -= 1
        else:
            liked_posts.append(post_id)
            post.likes += 1
        request.session['liked_posts'] = liked_posts
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/') + '#post' + str(post_id))

def request_transport(request, post_id):
    if request.method == 'POST':
        form = TransportRequestForm(request.POST)
        if form.is_valid():
            transport_request = form.save(commit=False)
            transport_request.post_id = post_id
            transport_request.save()
            return redirect('post_list')
    else:
        form = TransportRequestForm()
    return render(request, 'transport_request_form.html', {'form': form})


def transport_requests(request, post_id):
    user_profile = UserProfile.objects.get(user=request.user)
    transport_requests = TransportRequest.objects.filter(post_id=post_id)
    return render(request, 'transport_requests.html', {'transport_requests': transport_requests, 'user_profile': user_profile})