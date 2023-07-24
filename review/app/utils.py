from functools import wraps

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from .models import (
    EmployeePerformance, ModerationRoom,
    RoomModerator, RoomReviewer, 
    DirectReviewee, IndirectReviewee
)

from rest_framework.response import Response

def get_room(f):
    @wraps(f)
    def wrapped_function(request, *args, **kwargs):
        room = None
        room_id = request.GET.get('room')
        print("Room ID:", room_id)
        if room_id:
            try:
                room = ModerationRoom.objects.get(id=room_id)
            except (ModerationRoom.DoesNotExist, ValidationError):
                return Response({
                    'error': 'Invalid room id'
                }, status=status.HTTP_400_BAD_REQUEST)

        if not room:  # Check if room is None
            return Response({
                'error': 'Room not found'
            }, status=status.HTTP_404_NOT_FOUND)

        return f(request, room, *args, **kwargs)
    
    return wrapped_function

def get_room_by_POST(f):
    '''
    Wrapper function for getting room from room id in POST request
    Return room as the model object on top of other original args

    '''
    @wraps(f)
    def wrapped_function(request, *args, **kwargs):
        room = None
        room_id = request.data.get('room')
        if room_id:
            try:
                room = ModerationRoom.objects.get(id=room_id)
            except (ModerationRoom.DoesNotExist, ValidationError):
                return Response({
                    'error': 'Invalid room id'
                }, status=status.HTTP_400_BAD_REQUEST)
        return f(request, room, *args, **kwargs)
    
    return wrapped_function

def get_moderators_by_POST(f):
    '''
    Wrapper function for getting list of moderators from moderator ids in POST request
    Return moderators as the model object on top of other original args

    '''
    @wraps(f)
    def wrapped_function(request, *args, **kwargs):
        moderators = []
        moderator_ids = request.data.getlist('moderator')
        for moderator_id in moderator_ids:
            try:
                moderator = RoomModerator.objects.get(id=moderator_id)
                moderators.append(moderator)
            except (RoomModerator.DoesNotExist, ValidationError):
                return Response({
                    'error': f'Invalid moderator id - {moderator_id}'
                }, status=status.HTTP_400_BAD_REQUEST)
        return f(request, moderators, *args, **kwargs)
    
    return wrapped_function