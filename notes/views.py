from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import Note, AddNoteForm
from django.contrib import messages
import json

def home(request):
    print(request)
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user).order_by('-updated_at')[:10]
        all_notes = Note.objects.filter(user=request.user).order_by('-updated_at')

        if request.method == 'POST':
            form = AddNoteForm(request.POST)
            if form.is_valid():
                form_data = form.save(commit=False)
                form_data.user = request.user
                form_data.save()
                form = AddNoteForm()
                messages.success(request, 'Note added successfully!')
                return redirect('notes')
        else:
            form = AddNoteForm()
        context = {
            'notes': notes,
            'all_notes': all_notes,
            'add_note_form': form,
            'script_name': request.META['SCRIPT_NAME'],
        }
        return render(request, 'notes.html', context)
    else:
        return render(request, 'index.html')


def get_note_details(request, slug):
    note = get_object_or_404(Note, slug=slug)
    print('========')
    print(note.user)
    if note.user != request.user:
        messages.error(request, 'You are not authenticated to perform this action')
        return redirect('notes')

    notes = Note.objects.filter(user=request.user).order_by('-updated_at')[:10]
    add_note_form = AddNoteForm()

    context = {
        'notes': notes,
        'note_detail': note,
        'add_note_form': add_note_form,
    }
    return render(request, 'note_details.html', context)


def edit_note_details(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if note.user != request.user:
        messages.error(request, 'You are not authenticated to perform this action')
        return redirect('notes')
    if request.method == 'POST':
        form = AddNoteForm(request.POST, instance=note)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            form.save_m2m()
            return redirect('note_detail', slug=note.slug)
    else:
        form = AddNoteForm(initial={
            'note_title': note.note_title,
            'note_content': note.note_content,
        }, instance=note)
        return render(request, 'modals/edit_note_modal.html', {'form': form})


def confirm_delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if note.user != request.user:
        messages.error(request, 'You are not authenticated to perform this action')
        return redirect('notes')
    # note.delete()
    context = {
        'note_detail': note,
    }
    return render(request, 'modals/delete_note_modal.html', context)

def delete_note(request, pk):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=pk)
        if note.user != request.user:
            messages.error(request, 'You are not authenticated to perform this action')
            return redirect('notes')
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('notes')
    else:
        return render(request, 'index.html')


def search_note(request):
    if request.method == 'GET':
        q = request.GET.get('term')
        notes = Note.objects.filter(
                note_title__icontains=q,
                user=request.user
            )[:10]
        results = []
        for note in notes:
            note_json = {}
            note_json['slug'] = note.slug
            note_json['label'] = note.note_title
            note_json['value'] = note.note_title
            results.append(note_json)
        data = json.dumps(results)
    else:
        note_json = {}
        note_json['slug'] = None
        note_json['label'] = None
        note_json['value'] = None
        data = json.dumps(note_json)
    return HttpResponse(data)
