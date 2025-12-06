from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Tip, Like, Comment
from agriapp.models import FarmerProfile
from .forms import TipForm, CommentForm

# Create your views here.
def tips_list(request):
    """Display all tips"""
    tips = Tip.objects.all()
    
    # Add like count and user liked status for each tip
    for tip in tips:
        tip.like_count = tip.likes
        tip.user_liked = Like.objects.filter(user=request.user, tip=tip).exists() if request.user.is_authenticated else False
        tip.comment_count = tip.comments.count()
    
    context = {
        'tips': tips,
    }
    return render(request, 'tips/tips_list.html', context)


@login_required(login_url='login')
def create_tip(request):
    """Create a new tip"""
    try:
        farmer_profile = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = TipForm(request.POST, request.FILES)
        if form.is_valid():
            tip = form.save(commit=False)
            tip.author = farmer_profile
            tip.save()
            messages.success(request, 'Tip posted successfully!')
            return redirect('tips_list')
    else:
        form = TipForm()
    
    context = {
        'form': form,
    }
    return render(request, 'tips/create_tip.html', context)


def tip_detail(request, pk):
    """Display full tip details"""
    tip = get_object_or_404(Tip, pk=pk)
    comments = tip.comments.all()
    comment_form = CommentForm()
    
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(user=request.user, tip=tip).exists()
    
    context = {
        'tip': tip,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
    }
    return render(request, 'tips/tip_detail.html', context)


@login_required(login_url='login')
def like_tip(request, pk):
    """Like/Unlike a tip"""
    tip = get_object_or_404(Tip, pk=pk)
    
    like = Like.objects.filter(user=request.user, tip=tip).first()
    
    if like:
        like.delete()
        tip.likes -= 1
    else:
        Like.objects.create(user=request.user, tip=tip)
        tip.likes += 1
    
    tip.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': Like.objects.filter(user=request.user, tip=tip).exists(),
            'likes': tip.likes
        })
    
    return redirect('tips_list')


@login_required(login_url='login')
def add_comment(request, pk):
    """Add a comment to a tip"""
    tip = get_object_or_404(Tip, pk=pk)
    
    try:
        farmer_profile = FarmerProfile.objects.get(user=request.user)
    except FarmerProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('tips_list')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = farmer_profile
            comment.tip = tip
            comment.save()
            messages.success(request, 'Comment added!')
    
    return redirect('tip_detail', pk=pk)