from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    User, ModerationRoom, RoomModerator, RoomReviewer, DirectReviewee)

from .rooms_serializers import (
    UserBasicInfoSerializer,
    ModerationRoomSerializer, CreateModerationRoomSerializer, UpdateModerationRoomSerializer, 
    AddRoomMembersSerializer)


class ModerationRoomView(APIView):
    def get(self, request):
        queryset = ModerationRoom.objects.all()
        serializer = ModerationRoomSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        room_srlz = CreateModerationRoomSerializer(data=request.data)
        if room_srlz.is_valid():
            room_srlz.save()
        else:
            return Response(room_srlz.errors, status=status.HTTP_400_BAD_REQUEST)
        
        room = room_srlz.instance

        def add_users(users, role):
            data = []
            for user_id in users:
                try:
                    user = User.objects.get(pk=user_id)
                    added_by = User.objects.get(pk=request.data.get('added_by'))
                    data.append({
                        role: UserBasicInfoSerializer(user).data,
                        'room': room.id,
                        'added_by': UserBasicInfoSerializer(added_by).data
                    })
                except User.DoesNotExist:
                    return Response(f"User with ID {user_id} does not exist.", status=status.HTTP_400_BAD_REQUEST)
            return data

        # Adding moderators
        moderators = request.data.get('moderators', [])
        moderator_data = add_users(moderators, 'moderators')

        # Adding reviewers
        reviewers = request.data.get('reviewers', [])
        reviewer_data = add_users(reviewers, 'reviewers')

        # Adding direct reviewees
        direct_reviewees = request.data.get('direct_reviewees', [])
        direct_reviewee_data = add_users(direct_reviewees, 'direct_reviewees')

        # Adding indirect reviewees
        indirect_reviewees = request.data.get('indirect_reviewees', [])
        indirect_reviewee_data = add_users(indirect_reviewees, 'indirect_reviewees')

        all_users_data = moderator_data + reviewer_data + direct_reviewee_data + indirect_reviewee_data
        
        mod_srlz = AddRoomMembersSerializer(
            data=all_users_data, many=True, context={
                'request': request
            }
        )
        print(mod_srlz.initial_data)
        if not mod_srlz.is_valid():
            # if serializer is not valid, delete the room and cancel this operation
            room.delete()
            print('adjk')
            return Response(mod_srlz.errors, status=status.HTTP_400_BAD_REQUEST)
        
        mod_srlz.save()

         # Fetch the updated room object with the new members
        updated_room = ModerationRoom.objects.get(pk=room.id)
        print("updated room", updated_room)
        # Serialize the users associated with the room
        all_user_ids = set(moderators + reviewers + direct_reviewees + indirect_reviewees)
        users = User.objects.filter(id__in=all_user_ids)
        user_srlz = UserBasicInfoSerializer(users, many=True)

        # Serialize the updated room object along with the user information
        updated_room_srlz = ModerationRoomSerializer(updated_room)

        # Include the serialized users in the response
        response_data = updated_room_srlz.data
        response_data['users'] = user_srlz.data

        return Response({'room': response_data})

        # for moderator_id in moderators:
        #     try:
        #         moderator = User.objects.get(pk=moderator_id)
        #         data.append({
        #             'moderator': moderator_id,
        #             'room': room.id,
        #             'added_by': request.data.get('added_by') 
        #         })
        #     except User.DoesNotExist:
        #         return Response(f"User with ID {moderator_id} does not exist")

        # mod_srlz = AddRoomMembersSerializer(
        #     data=data, many=True, context={
        #         'reqeust':request
        #     })
        
        # if mod_srlz.is_valid():
        #     mod_srlz.save()
    
        # else:
        #     room.delete()
        #     return Response(mod_srlz.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # # Fetch the updated room object with the new moderators
        # updated_room = ModerationRoom.objects.get(pk=room.id)

        # # Serialize the moderators associated with the room
        # moderators = User.objects.filter(id__in=moderators)  # Assuming 'moderators' is a list of moderator IDs
        # moderator_srlz = UserBasicInfoSerializer(moderators, many=True)

        # # Serialize the updated room object along with the moderator information
        # updated_room_srlz = ModerationRoomSerializer(updated_room)

        # response_data = updated_room_srlz.data
        # response_data['moderators'] = moderator_srlz.data
        # return Response({'room': response_data})










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

