from django.contrib import admin
from .models import (
    User, EmployeePerformance, ModerationRoom, RoomModerator, RoomReviewer, DirectReviewee, IndirectReviewee
)

# Register your models here.
admin.site.register(User)
admin.site.register(EmployeePerformance)
admin.site.register(ModerationRoom)
admin.site.register(RoomModerator)
admin.site.register(RoomReviewer)
admin.site.register(DirectReviewee)
admin.site.register(IndirectReviewee)