from uuid import uuid4
import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_history.models import HistoricalRecords

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year()+1)(value)

class PerformanceRating(models.TextChoices):
    UNSATISFACTORY = 'UNSATISFACTORY', _('UNSATISFACTORY')
    DEVELOPMENTAL = 'DEVELOPMENTAL', _('DEVELOPMENTAL')
    SOLID = 'SOLID', _('SOLID')
    OUTSTANDING = 'OUTSTANDING', _('OUTSTANDING')
    TOP = 'TOP', _('TOP')

class CalibrationStatus(models.TextChoices):
    NOT_RATED = 'NOT_RATED', _('NOT_RATED') # default display during calibration
    RATED_NOT_CONFIRMED = 'RATED_NOT_CONFIRMED', _('RATED_NOT_CONFIRMED') # default display during calibration
    RATED_CONFIRMED = 'RATED_CONFIRMED', _('RATED_CONFIRMED')
    CONFIRMED_NOT_RELEASED = 'CONFIRMED_NOT_RELEASED', _('CONFIRMED_NOT_RELEASED')
    CONFIRMED_RELEASED = 'CONFIRMED_RELEASED', _('CONFIRMED_RELEASED')

class ReviewerStatus(models.TextChoices):
    REVIEWING = 'REVIEWING', _('REVIEWING')
    CONFIRMED = 'CONFIRMED', _('CONFIRMED')

class RoomStatus(models.TextChoices):
    UNSTARTED = 'UNSTARTED', _('UNSTARTED')
    ONGOING = 'ONGOING', _('ONGOING')
    CLOSED = 'CLOSED', _('CLOSED')

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    is_exec = models.BooleanField(default=True)
    email = models.EmailField(("email address"), unique=True, null=True, blank=True)
    ic_no = models.CharField(max_length=31, null=True, blank=True)
    passport_no = models.CharField(max_length=31, null=True, blank=True)

    # Add related_name to the groups field to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups',  # Use a unique related_name
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    # Add related_name to the user_permissions field to avoid clashes
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions',  # Use a unique related_name
        help_text='Specific permissions for this user.',
    )


class EmployeePerformance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    employee = models.ForeignKey(User,
                                 null=True, blank=True,
                                 on_delete=models.CASCADE,
                                 related_name='performances_by_employee')
    year = models.PositiveIntegerField(default=current_year(), 
                                                 validators=[MinValueValidator(2023), 
                                                             max_value_current_year])
    rating = models.CharField(max_length=15,
                              choices=PerformanceRating.choices,
                              null=True, blank=True)
    status = models.CharField(max_length=31,
                              choices=CalibrationStatus.choices,
                              default=CalibrationStatus.NOT_RATED)
    history = HistoricalRecords()


class ModerationRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=63)
    description = models.TextField(null=True, blank=True)
    year = models.PositiveIntegerField(default=current_year(), 
                                                 validators=[MinValueValidator(2023), 
                                                             max_value_current_year])
    closed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15,
                              choices=RoomStatus.choices,
                              default=RoomStatus.UNSTARTED)
    created_by = models.ForeignKey(User,
                                   null=True, blank=True,
                                   on_delete=models.CASCADE,
                                   related_name='rooms_created_by_user')
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class RoomModerator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    moderator = models.ForeignKey(User,
                                  null=True, blank=True,
                                  on_delete=models.CASCADE,
                                  related_name='moderators_by_user')
    room = models.ForeignKey(ModerationRoom,
                             null=True, blank=True,
                             on_delete=models.CASCADE,
                             related_name='moderators_by_room')
    added_by = models.ForeignKey(User,
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='moderators_added_by_user')
    history = HistoricalRecords()

    # def __str__(self):
    #     return self.moderator


class RoomReviewer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    reviewer = models.ForeignKey(User,
                                 null=True, blank=True,
                                 on_delete=models.CASCADE,
                                 related_name='reviewers_by_user')
    room = models.ForeignKey(ModerationRoom,
                             null=True, blank=True,
                             on_delete=models.CASCADE,
                             related_name='reviewers_by_room')
    status = models.CharField(max_length=15,
                              choices=ReviewerStatus.choices,
                              default=ReviewerStatus.REVIEWING)
    added_by = models.ForeignKey(User,
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='reviewers_added_by_user')
    history = HistoricalRecords()


class DirectReviewee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    direct_reviewee = models.ForeignKey(User,
                                        null=True, blank=True,
                                        on_delete=models.CASCADE,
                                        related_name='direct_reviewees_by_user')
    room = models.ForeignKey(ModerationRoom,
                             null=True, blank=True,
                             on_delete=models.CASCADE,
                             related_name='direct_reviewees_by_room')
    added_by = models.ForeignKey(User,
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='direct_reviewees_added_by_user')
    history = HistoricalRecords()


# indirect reviewees are queried during moderation and only added if rated in the room
class IndirectReviewee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    indirect_reviewee = models.ForeignKey(User,
                                          null=True, blank=True,
                                          on_delete=models.CASCADE,
                                          related_name='indirect_reviewees_by_user')
    room = models.ForeignKey(ModerationRoom,
                             null=True, blank=True,
                             on_delete=models.CASCADE,
                             related_name='indirect_reviewees_by_room')
    added_by = models.ForeignKey(User,
                                 null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='indirect_reviewees_added_by_user')
    history = HistoricalRecords()