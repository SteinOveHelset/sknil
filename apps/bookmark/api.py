from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Category, Bookmark

@csrf_exempt
def api_delete_category(request, category_id):
    category = request.user.categories.all().get(pk=category_id)
    category.delete()

    return JsonResponse({'success': True})

@csrf_exempt
def api_delete_bookmark(request, bookmark_id):
    bookmark = request.user.bookmarks.all().get(pk=bookmark_id)
    bookmark.delete()

    return JsonResponse({'success': True})

@csrf_exempt
def api_increase_visits(request, bookmark_id):
    bookmark = request.user.bookmarks.all().get(pk=bookmark_id)
    bookmark.visits = bookmark.visits + 1
    bookmark.save()

    return JsonResponse({'success': True})