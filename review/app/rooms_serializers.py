from rest_framework import serializers

from .models import (
    ModerationRoom, RoomModerator, RoomReviewer, DirectReviewee, IndirectReviewee, User)

class UserBasicInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    is_exec = serializers.BooleanField()
    email = serializers.EmailField()
    # staff_id = serializers.CharField()
    # employee_no = serializers.CharField()
    # commercial_title = serializers.CharField()

    class Meta:
        model = User
        fields = ('id', 'username', 'is_exec', 'email',)
                #   'staff_id', 'employee_no', 'commercial_title')

class ModerationRoomSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    description = serializers.CharField()
    year = serializers.IntegerField()
    closed_at = serializers.DateTimeField()
    status = serializers.CharField()
    created_by = UserBasicInfoSerializer()
    created_at = serializers.DateTimeField()

    moderators_by_room = serializers.PrimaryKeyRelatedField(queryset=RoomModerator.objects.all(), many=True)
    reviewers_by_room = serializers.PrimaryKeyRelatedField(queryset=RoomReviewer.objects.all(), many=True)
    direct_reviewees_by_room = serializers.PrimaryKeyRelatedField(queryset=DirectReviewee.objects.all(), many=True)
    indirect_reviewees_by_room = serializers.PrimaryKeyRelatedField(queryset=IndirectReviewee.objects.all(), many=True)
    
    class Meta:
        model = ModerationRoom
        fields = '__all__'


class CreateModerationRoomSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    year = serializers.CharField()
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    # moderators_by_user = serializers.PrimaryKeyRelatedField(queryset=RoomModerator.objects.all(), many=True)
    # reviewers_by_room = serializers.PrimaryKeyRelatedField(queryset=RoomReviewer.objects.all(), many=True)
    # direct_reviewees_by_room = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    # indirect_reviewees_by_room = serializers.PrimaryKeyRelatedField(queryset=IndirectReviewee.objects.all(), many=True)
    
    class Meta:
        model = ModerationRoom
        fields = '__all__'


class UpdateModerationRoomSerializer(serializers.ModelSerializer):  
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    year = serializers.CharField()

    moderators_by_room = serializers.PrimaryKeyRelatedField(queryset=RoomModerator.objects.all(), many=True)
    reviewers_by_room = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    direct_reviewees_by_room = serializers.PrimaryKeyRelatedField(queryset=DirectReviewee.objects.all(), many=True)
    indirect_reviewees_by_room = serializers.PrimaryKeyRelatedField(queryset=IndirectReviewee.objects.all(), many=True)

    class Meta:
        model = ModerationRoom
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     request = self.context.get('request')

    #     # Access restriction, if not manager or HR, deny access
    #     # Access restriction, if include reviewee with higher level, deny access
    #     return super().update(instance, validated_data)

class RoomModeratorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    moderator = UserBasicInfoSerializer()
    room = ModerationRoomSerializer()
    added_by = UserBasicInfoSerializer()

    class Meta:
        model = RoomModerator
        fields = '__all__'

class RoomReviewerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    reviewer = UserBasicInfoSerializer()
    room = ModerationRoomSerializer()
    status = serializers.CharField()
    added_by = UserBasicInfoSerializer()

    class Meta:
        model = RoomReviewer
        fields = '__all__'

class DirectRevieweeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    direct_reviewee = UserBasicInfoSerializer()
    room = ModerationRoomSerializer()
    added_by = UserBasicInfoSerializer()

    class Meta:
        model = DirectReviewee
        fields = '__all__'

class IndirectRevieweeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    indirect_reviewee = UserBasicInfoSerializer()
    room = ModerationRoomSerializer()
    added_by = UserBasicInfoSerializer()

    class Meta:
        model = IndirectReviewee
        fields = '__all__'


class AddRoomMembersSerializer(serializers.Serializer):
    moderators = RoomModeratorSerializer(many=True)
    reviewers = RoomReviewerSerializer(many=True)
    direct_reviewees = DirectRevieweeSerializer(many=True)
    indirect_reviewees = IndirectRevieweeSerializer(many=True)
    room = serializers.PrimaryKeyRelatedField(queryset=ModerationRoom.objects.all())
    added_by = UserBasicInfoSerializer()

    def create(self, validated_data):
        # Custom create logic here if needed
        pass

    def update(self, instance, validated_data):
        # Custom update logic here if needed
        pass


# class AddRoomMembersSerializer(serializers.ModelSerializer):
#     moderator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     reviewer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     direct_reviewees = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     indirect_reviewees = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     room = serializers.PrimaryKeyRelatedField(queryset=ModerationRoom.objects.all())
#     added_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

#     class Meta:
#         model = RoomModerator
#         fields = '__all__'