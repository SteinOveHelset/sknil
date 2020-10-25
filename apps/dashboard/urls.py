from django.urls import path

from .views import dashboard, settings, plans, complete, create_sub
from apps.bookmark.views import categories, category, category_add, category_edit, category_delete, bookmark_add, bookmark_edit, bookmark_delete
from apps.bookmark.api import api_delete_category, api_delete_bookmark, api_increase_visits

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('create-sub/', create_sub, name='create_sub'),
    path('settings/', settings, name='settings'),
    path('settings/plans/', plans, name='plans'),
    path('settings/plans/complete/', complete, name='complete'),
    path('categories/', categories, name='categories'),
    path('categories/add/', category_add, name='category_add'),
    path('categories/<int:category_id>/', category, name='category'),
    path('categories/<int:category_id>/edit/', category_edit, name='category_edit'),
    path('categories/<int:category_id>/delete/', category_delete, name='category_delete'),
    path('categories/<int:category_id>/add_bookmark/', bookmark_add, name='bookmark_add'),
    path('categories/<int:category_id>/edit_bookmark/<int:bookmark_id>/', bookmark_edit, name='bookmark_edit'),
    path('categories/<int:category_id>/delete_bookmark/<int:bookmark_id>/', bookmark_delete, name='bookmark_delete'),

    path('api/delete_category/<int:category_id>/', api_delete_category, name='api_delete_category'),
    path('api/delete_bookmark/<int:bookmark_id>/', api_delete_bookmark, name='api_delete_bookmark'),
    path('api/increase_visits/<int:bookmark_id>/', api_increase_visits, name='api_increase_visits'),
]