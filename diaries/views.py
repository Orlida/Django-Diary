from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from .models import DiaryEntry, Follow, Like, Profile
from .forms import RegisterForm, DiaryEntryForm, CommentForm, EditUserForm, EditProfileForm


# ---------- AUTH ----------

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'diaries/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'diaries/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ---------- HOME / FEED ----------

@login_required
def home_view(request):
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    all_entries = DiaryEntry.objects.filter(
        user__in=list(following_ids) + [request.user.id]
    )

    paginator = Paginator(all_entries, 4)
    page_number = request.GET.get('page')
    entries = paginator.get_page(page_number)

    return render(request, 'diaries/home.html', {'entries': entries})


# ---------- DIARY ENTRY CRUD ----------

@login_required
def entry_create_view(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Diary entry created!')
            return redirect('home')
    else:
        form = DiaryEntryForm()
    return render(request, 'diaries/entry_form.html', {'form': form, 'action': 'Create'})


# Update entry_detail_view to include likes and comments
@login_required
def entry_detail_view(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk)
    is_owner = entry.user == request.user
    is_following = Follow.objects.filter(follower=request.user, following=entry.user).exists()

    if not is_owner and not is_following:
        messages.error(request, 'You do not have permission to view this entry.')
        return redirect('home')

    # Check mutual follow for commenting
    is_followed_back = Follow.objects.filter(follower=entry.user, following=request.user).exists()
    can_comment = is_owner or (is_following and is_followed_back)

    # Like status
    is_liked = Like.objects.filter(user=request.user, entry=entry).exists()
    likes_count = entry.likes.count()

    # Comments
    comments = entry.comments.all()
    comment_form = CommentForm()

    return render(request, 'diaries/entry_detail.html', {
        'entry': entry,
        'is_owner': is_owner,
        'is_liked': is_liked,
        'likes_count': likes_count,
        'can_comment': can_comment,
        'comments': comments,
        'comment_form': comment_form,
    })


@login_required
def entry_edit_view(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk)

    if entry.user != request.user:
        messages.error(request, 'You can only edit your own entries.')
        return redirect('home')

    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entry updated!')
            return redirect('entry_detail', pk=entry.pk)
    else:
        form = DiaryEntryForm(instance=entry)
    return render(request, 'diaries/entry_form.html', {'form': form, 'action': 'Edit'})


@login_required
def entry_delete_view(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk)

    if entry.user != request.user:
        messages.error(request, 'You can only delete your own entries.')
        return redirect('home')

    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Entry deleted.')
        return redirect('home')

    return render(request, 'diaries/entry_confirm_delete.html', {'entry': entry})


# ---------- PROFILE & FOLLOW ----------

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=profile_user)  # add this
    is_owner = profile_user == request.user
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    if is_owner or is_following:
        entries = DiaryEntry.objects.filter(user=profile_user)
    else:
        entries = None

    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()

    return render(request, 'diaries/profile.html', {
        'profile_user': profile_user,
        'profile': profile,          # add this
        'entries': entries,
        'is_owner': is_owner,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    })


@login_required
def follow_view(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        messages.error(request, 'You cannot follow yourself.')
        return redirect('profile', username=username)

    follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
    if not created:
        # Already following — do nothing
        messages.info(request, f'You are already following {target_user.username}.')

    return redirect('profile', username=username)


@login_required
def unfollow_view(request, username):
    target_user = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=target_user).delete()
    return redirect('profile', username=username)


@login_required
def search_view(request):
    query = request.GET.get('q', '')
    results = User.objects.filter(username__icontains=query).exclude(pk=request.user.pk) if query else []
    return render(request, 'diaries/search.html', {'results': results, 'query': query})


@login_required
def like_view(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, entry=entry)
    if not created:
        like.delete()  # unlike if already liked
    return redirect('entry_detail', pk=pk)


@login_required
def comment_view(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk)

    # Check mutual follow
    is_owner = entry.user == request.user
    is_following = Follow.objects.filter(follower=request.user, following=entry.user).exists()
    is_followed_back = Follow.objects.filter(follower=entry.user, following=request.user).exists()
    can_comment = is_owner or (is_following and is_followed_back)

    if not can_comment:
        messages.error(request, 'You must follow each other to comment.')
        return redirect('entry_detail', pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.entry = entry
            comment.save()

    return redirect('entry_detail', pk=pk)


@login_required
def edit_profile_view(request,username):

    if request.user.username != username:
        messages.error(request, 'You can only edit your own profile.')
        return redirect('home')

    # Make sure profile exists
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', username=request.user.username)
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=profile)

    return render(request, 'diaries/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

def followers_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    # Get all users who follow this profile_user
    followers = Follow.objects.filter(following=profile_user)

    #Check querying search
    query = request.GET.get('q')
    if query:
        followers = followers.filter(follower__username__icontains=query)

    return render(request, 'diaries/followers.html', {
        'profile_user': profile_user,
        'followers': followers,
        'query': query
    })

def following_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    # Get all users that this profile_user is following
    following = Follow.objects.filter(follower=profile_user)

    query = request.GET.get('q')
    if query:
        following = following.filter(following__username__icontains=query)

    return render(request, 'diaries/following.html', {
        'profile_user': profile_user,
        'following': following,
        'query': query
    })



