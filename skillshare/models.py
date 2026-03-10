from django.conf import settings  # type: ignore
from django.contrib.auth.models import (  # type: ignore
    AbstractUser,
)
from django.db import models  # type: ignore
from django.utils import timesince, timezone  # type: ignore

from .utils import get_random_slug


class Category(models.Model):
    """
    Category class represent the related Skill model
    """

    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Skill(models.Model):
    """
    Skill represent an user capability given by a `giver`, is related to a `category`
    """

    giver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name


class Schedule(models.Model):
    """
    Schedule class is associated with a Skill, through a `Skill.giver` and a `taker`
    has a `scheduled_at` Date, an `activity_description` and a `is_request` to add help requests
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # Celui qui crée la demande
    taker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="taken_schedules",
    )
    scheduled_at = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    skill = models.ForeignKey(Skill, on_delete=models.DO_NOTHING)

    activity_description = models.TextField(blank=True, null=True)
    is_request = models.BooleanField(default=False)  # true if it's an help request

    def __str__(self) -> str:
        return self.scheduled_at.isoformat()

    def time_since(self):
        return timesince.timesince(self.scheduled_at, timezone.now())


class CustomUser(AbstractUser):
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = get_random_slug()
        super().save(*args, **kwargs)
