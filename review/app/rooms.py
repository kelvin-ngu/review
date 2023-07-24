from django.db import transaction
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from .models import (
    User, ModerationRoom, RoomModerator, RoomReviewer, DirectReviewee)

from .rooms_serializers import (
    UserBasicInfoSerializer,
    ModerationRoomSerializer, CreateModerationRoomSerializer, UpdateModerationRoomSerializer, 
    RoomModeratorSerializer, AddRoomMembersSerializer)

from .utils import (
    get_room, get_room_by_POST, get_moderators_by_POST
)

class ModerationRoomView(APIView):
    # @method_decorator([get_room])
    # def get(self, request, room: ModerationRoom):
    #     if not room:
    #         return Response({
    #             'error: Please provide room id'
    #         }, status=status.HTTP_400_BAD_REQUEST)
    
    #     objs = ModerationRoom.objects.filter(room=id, is_active=True)
    #     objs_srlz = ModerationRoomSerializer(objs, many=True)
    #     return Response(objs_srlz.data)
    def get(self, request):
        queryset = ModerationRoom.objects.all()
        serializer = ModerationRoomSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
    # @method_decorator([get_room_by_POST, get_moderators_by_POST])
    def post(self, request): # moderators: RoomModerator, room: ModerationRoom):
        room_srlz = CreateModerationRoomSerializer(data=request.data)
        if room_srlz.is_valid():
            room_srlz.save()
        else:
            return Response(room_srlz.errors, status=status.HTTP_400_BAD_REQUEST)
        
        room = room_srlz.instance

        moderators = request.data.get('moderators', [])
        data = []

        for moderator_id in moderators:
            try:
                moderator = User.objects.get(pk=moderator_id)
                data.append({
                    'moderator': moderator_id,
                    'room': room.id,
                    'added_by': request.data.get('added_by') 
                })
            except User.DoesNotExist:
                return Response(f"User with ID {moderator_id} does not exist")

        mod_srlz = AddRoomMembersSerializer(
            data=data, many=True, context={
                'reqeust':request
            })
        
        if mod_srlz.is_valid():
            mod_srlz.save()
    
        else:
            room.delete()
            return Response(mod_srlz.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the updated room object with the new moderators
        updated_room = ModerationRoom.objects.get(pk=room.id)

        # Serialize the moderators associated with the room
        moderators = User.objects.filter(id__in=moderators)  # Assuming 'moderators' is a list of moderator IDs
        moderator_srlz = UserBasicInfoSerializer(moderators, many=True)

        # Serialize the updated room object along with the moderator information
        updated_room_srlz = ModerationRoomSerializer(updated_room)

        response_data = updated_room_srlz.data
        response_data['moderators'] = moderator_srlz.data
        return Response({'room': response_data})
    


        # Make sure room is present
        # print('pk:',pk)

        # room = ModerationRoom.object.get(id=pk)
        # if not room:
        #     return Response({
        #         'error': 'Room not found'
        #     }}

        # try:
        #     with transaction.atomic():
        #         moderator_srlz = AddRoomMembersSerializer(data=request.data)
        #         if moderator_srlz.is_valid():
        #             moderator_srlz.save()
        #             return Response(moderator_srlz.data, status=status.HTTP_201_CREATED)
                
        # except ValidationError:
        #     return Response({'Validation Error': 'Failed to add room members.'}, status=status.HTTP_400_BAD_REQUEST)

        # return Response({'message': 'Room members added successfully.'}, status=status.HTTP_200_OK)


        # # return Response({'message': 'Room members added successfully.'}, status=status.HTTP_200_OK)








# class ModerationRoomViewSet(ModelViewSet):
#     queryset = ModerationRoom.objects.all()
#     serializer_class = ModerationRoomSerializer
#     pagination_class = None  # Add pagination class to limit API response size

#     action_serializers = {
#             'create': CreateModerationRoomSerializer,
#             'update': UpdateModerationRoomSerializer,
#             'addmembers': AddRoomMembersSerializer,
#     }
    
#     # @action(detail=True, methods=['get','post'])
#     # # @method_decorator([get_room])
#     # def add_room_members(self, request, pk):# room: ModerationRoom):

#     #     room = self.get_object()
#     #     if request.method == 'POST':
#     #         serializer = AddRoomMembersSerializer(room, request.POST)

#     #         if serializer.is_valid():
#     #             serializer.save()
#     #             data = serializer.validated_data
#     #             print(serializer.data)
#     #             print(serializer.validated_data)

#     #             try:
#     #                 with transaction.atomic():
#     #                     # Get moderator IDs from the request data
#     #                     moderator_ids = data.get('moderators_by_room', [])
#     #                     for moderator_id in moderator_ids:
#     #                         # Create a RoomModerator instance and associate it with the ModerationRoom
#     #                         RoomModerator.objects.create(id=moderator_id, room=room)
                        
#     #             except ValidationError:
#     #                 return Response({'Validation Error': 'Failed to add room members.'}, status=status.HTTP_400_BAD_REQUEST)

#     #             return Response({'message': 'Room members added successfully.'}, status=status.HTTP_200_OK)
#     #         else:
#     #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


#                 # reviewer_ids = data.get('reviewers_by_room', [])
#                 # for reviewer_id in reviewer_ids:
#                 #     RoomReviewer.objects.create(reviewer_id=reviewer_id, room=instance)

#                 # direct_reviewee_ids = data.get('direct_reviewees_by_room', [])
#                 # for direct_reviewee_id in direct_reviewee_ids:
#                 #     DirectReviewee.objects.create(direct_reviewee_id=direct_reviewee_id, room=instance)

#     def get_serializer_class(self):
#         if hasattr(self, 'action_serializers'):
#             return self.action_serializers.get(self.action, self.serializer_class)
#         return super().get_serializer_class()

