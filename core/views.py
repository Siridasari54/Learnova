from django.shortcuts import render, redirect
from django.db.models import Q, Count
from rooms.models import Room, Topic, Message


def home_view(request):
    """Main dashboard/homepage."""
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
    recent_messages = Message.objects.select_related('user', 'room').order_by('-created_at')[:8]

    total_rooms = Room.objects.count()
    total_topics = Topic.objects.count()

    context = {
        'rooms': rooms,
        'topics': topics,
        'recent_messages': recent_messages,
        'query': query,
        'topic_filter': topic_filter,
        'room_count': rooms.count(),
        'total_rooms': total_rooms,
        'total_topics': total_topics,
    }
    return render(request, 'core/home.html', context)
