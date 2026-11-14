from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponseForbidden
from .models import Room, Topic, Message, RoomMembership
from .forms import RoomForm, MessageForm


def room_list_view(request):
    """List all rooms with search and topic filter."""
    query = request.GET.get('q', '')
    topic_filter = request.GET.get('topic', '')

    rooms = Room.objects.select_related('host', 'topic').prefetch_related('members')

    if query:
        rooms = rooms.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(topic__name__icontains=query) |
            Q(host__username__icontains=query)
        )

    if topic_filter:
        rooms = rooms.filter(topic__name__iexact=topic_filter)

    topics = Topic.objects.annotate(room_count=Count('rooms')).order_by('-room_count')
    recent_messages = Message.objects.select_related('user', 'room').order_by('-created_at')[:10]

    context = {
        'rooms': rooms,
        'topics': topics,
        'recent_messages': recent_messages,
        'query': query,
        'topic_filter': topic_filter,
        'room_count': rooms.count(),
    }
    return render(request, 'rooms/room_list.html', context)


def room_detail_view(request, pk):
    """View a single room and its discussion."""
    room = get_object_or_404(Room.objects.select_related('host', 'topic'), pk=pk)
    room_messages = room.messages.select_related('user').order_by('created_at')
    members = room.members.all()
    is_member = request.user.is_authenticated and room.members.filter(pk=request.user.pk).exists()
    is_host = request.user.is_authenticated and room.host == request.user

    form = MessageForm()
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to send messages.")
            return redirect('login')
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = request.user
            msg.room = room
            msg.save()
            # Auto-join on message
            RoomMembership.objects.get_or_create(user=request.user, room=room)
            # Update room activity
            room.save()
            return redirect('room_detail', pk=room.pk)

    context = {
        'room': room,
        'room_messages': room_messages,
        'members': members,
        'is_member': is_member,
        'is_host': is_host,
        'form': form,
    }
    return render(request, 'rooms/room_detail.html', context)


@login_required(login_url='/accounts/login/')
def create_room_view(request):
    """Create a new study room."""
    topics = Topic.objects.all().order_by('name')
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            topic_name = form.cleaned_data['topic_name'].strip()
            topic, created = Topic.objects.get_or_create(name__iexact=topic_name, defaults={'name': topic_name})

            room = form.save(commit=False)
            room.host = request.user
            room.topic = topic
            room.save()

            # Host auto-joins
            RoomMembership.objects.get_or_create(user=request.user, room=room)
            messages.success(request, f"Study room '{room.name}' created successfully! 🚀")
            return redirect('room_detail', pk=room.pk)
        else:
            messages.error(request, "Please correct the errors below.")

    context = {'form': form, 'topics': topics, 'page': 'create'}
    return render(request, 'rooms/room_form.html', context)


@login_required(login_url='/accounts/login/')
def edit_room_view(request, pk):
    """Edit an existing study room."""
    room = get_object_or_404(Room, pk=pk)

    if room.host != request.user:
        messages.error(request, "You are not authorized to edit this room.")
        return redirect('room_detail', pk=room.pk)

    topics = Topic.objects.all().order_by('name')
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            topic_name = form.cleaned_data['topic_name'].strip()
            topic, created = Topic.objects.get_or_create(name__iexact=topic_name, defaults={'name': topic_name})

            room = form.save(commit=False)
            room.topic = topic
            room.save()
            messages.success(request, f"Room '{room.name}' updated successfully! ✏️")
            return redirect('room_detail', pk=room.pk)
        else:
            messages.error(request, "Please correct the errors below.")

    context = {'form': form, 'room': room, 'topics': topics, 'page': 'edit'}
    return render(request, 'rooms/room_form.html', context)


@login_required(login_url='/accounts/login/')
def delete_room_view(request, pk):
    """Delete a study room."""
    room = get_object_or_404(Room, pk=pk)

    if room.host != request.user:
        messages.error(request, "You are not authorized to delete this room.")
        return redirect('room_detail', pk=room.pk)

    if request.method == 'POST':
        room_name = room.name
        room.delete()
        messages.success(request, f"Room '{room_name}' has been deleted.")
        return redirect('home')

    context = {'room': room}
    return render(request, 'rooms/delete_room.html', context)


@login_required(login_url='/accounts/login/')
def join_room_view(request, pk):
    """Join a study room."""
    room = get_object_or_404(Room, pk=pk)
    membership, created = RoomMembership.objects.get_or_create(user=request.user, room=room)
    if created:
        messages.success(request, f"You joined '{room.name}'! 🎓")
    else:
        messages.info(request, f"You are already a member of '{room.name}'.")
    return redirect('room_detail', pk=room.pk)


@login_required(login_url='/accounts/login/')
def leave_room_view(request, pk):
    """Leave a study room."""
    room = get_object_or_404(Room, pk=pk)
    if room.host == request.user:
        messages.warning(request, "You are the host — you cannot leave your own room. Delete it instead.")
        return redirect('room_detail', pk=room.pk)

    RoomMembership.objects.filter(user=request.user, room=room).delete()
    messages.info(request, f"You left '{room.name}'.")
    return redirect('home')


@login_required(login_url='/accounts/login/')
def delete_message_view(request, pk):
    """Delete a message."""
    message = get_object_or_404(Message, pk=pk)

    if message.user != request.user:
        messages.error(request, "You can only delete your own messages.")
        return redirect('room_detail', pk=message.room.pk)

    room_pk = message.room.pk
    message.delete()
    messages.success(request, "Message deleted.")
    return redirect('room_detail', pk=room_pk)
