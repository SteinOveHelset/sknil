from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Category, Bookmark
from .forms import CategoryForm, BookmarkForm

@login_required
def categories(request):
    categories = request.user.categories.all()

    context = {
        'categories': categories
    }

    return render(request, 'bookmark/categories.html', context)

@login_required
def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    bookmarksstring = ''

    for bookmark in category.bookmarks.all():
        editurl = reverse('bookmark_edit', args=[category.id, bookmark.id])
        b = "{'id': '%s', 'title': '%s', 'url': '%s', 'editurl': '%s', 'description': '%s', 'visits': '%s'}," % (bookmark.id, bookmark.title, bookmark.url, editurl, bookmark.description, bookmark.visits)

        bookmarksstring = bookmarksstring + b
    
    context = {
        'category': category,
        'bookmarksstring': bookmarksstring
    }

    return render(request, 'bookmark/category.html', context)

@login_required
def category_add(request):
    canAdd = ''

    categories = request.user.categories.all().count()

    if categories >= 50 and request.user.userprofile.isPro():
        canAdd = 'You can\'t have more than 50 categories when you\'re on a pro plan!'
    if categories >= 5 and not request.user.userprofile.isPro():
        canAdd = 'You can\'t have more than 5 categories when you\'re on the basic plan'

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.save()

            messages.success(request, 'The category has been added!')

            return redirect('categories')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'canAdd': canAdd
    }
    
    return render(request, 'bookmark/category_add.html', context)

@login_required
def category_edit(request, category_id):
    category = Category.objects.filter(created_by=request.user).get(pk=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()

            messages.success(request, 'The changes was saved!')

            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category
    }
    
    return render(request, 'bookmark/category_edit.html', context)

@login_required
def category_delete(request, category_id):
    category = Category.objects.filter(created_by=request.user).get(pk=category_id)
    category.delete()

    messages.success(request, 'The category was deleted')

    return redirect('categories')

@login_required
def bookmark_add(request, category_id):
    canAdd = ''
    bookmarks = request.user.bookmarks.all().count()

    if bookmarks >= 50 and not request.user.userprofile.isPro():
        canAdd = 'You can\'t have more than 50 bookmarks when you\'re on the basic plan'

    if request.method == 'POST':
        form = BookmarkForm(request.POST)

        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.created_by = request.user
            bookmark.category_id = category_id
            bookmark.save()

            messages.success(request, 'The bookmard was added')

            return redirect('category', category_id=category_id)
    else:
        form = BookmarkForm()
    
    context = {
        'form': form,
        'canAdd': canAdd
    }
    
    return render(request, 'bookmark/bookmark_add.html', context)

@login_required
def bookmark_edit(request, category_id, bookmark_id):
    bookmark = Bookmark.objects.filter(created_by=request.user).get(pk=bookmark_id)

    if request.method == 'POST':
        form = BookmarkForm(request.POST, instance=bookmark)

        if form.is_valid():
            form.save()

            messages.success(request, 'The changes was saved')

            return redirect('category', category_id=category_id)
    else:
        form = BookmarkForm(instance=bookmark)
    
    context = {
        'form': form,
        'bookmark': bookmark
    }
    
    return render(request, 'bookmark/bookmark_edit.html', context)

@login_required
def bookmark_delete(request, category_id, bookmark_id):
    bookmark = Bookmark.objects.filter(created_by=request.user).get(pk=bookmark_id)
    bookmark.delete()

    messages.success(request, 'The bookmark was deleted')

    return redirect('category', category_id=category_id)