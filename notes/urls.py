from django.urls import path
from .views import home, search_note, get_note_details, delete_note, confirm_delete_note, edit_note_details
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(home), name='notes'),
    path('search/', search_note, name='search_note'),
    path('<slug:slug>/', login_required(get_note_details), name='note_detail'),
    path('<int:pk>/edit/', login_required(edit_note_details), name='note_details_edit'),
    path('<int:pk>/delete/', login_required(delete_note), name='delete_single_note'),
    path('<int:pk>/delete/confirm/', login_required(confirm_delete_note), name='confirm_delete_note'),
]