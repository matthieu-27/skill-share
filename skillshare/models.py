from typing import Any

from django.conf import settings  # type: ignore
from django.contrib.auth.models import AbstractUser  # type: ignore
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

    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name="skills"
    )

    def __str__(self) -> str:
        return self.name


class Schedule(models.Model):
    """
    Schedule class is associated with a Skill, a `giver` and a `taker`
    has a `scheduled_at` Date, an `activity_description` and a `is_request` to add help requests
    """

    giver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING
    )  # Celui qui crée la demande
    taker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="taken_schedules",
    )
    scheduled_at = models.DateTimeField()
    duration = models.PositiveIntegerField(
        blank=True, null=True, help_text="Nombre de jours de disponibilité"
    )
    is_active = models.BooleanField(default=False)
    skill = models.ForeignKey(Skill, on_delete=models.DO_NOTHING)

    activity_description = models.TextField(blank=True, null=True)
    is_request = models.BooleanField(default=False)  # true if it's an help request

    def __str__(self) -> str:
        return self.scheduled_at.isoformat()

    def time_since(self) -> str:
        return timesince.timesince(self.scheduled_at, timezone.now())


class CustomUser(AbstractUser):
    """
    Adds a slug field to the user model to hide user names

    Uses the get_random_slug function to generate a random slug
    """

    slug = models.SlugField(unique=True, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.slug = get_random_slug()
        super().save(*args, **kwargs)


class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)


class Connection(models.Model):
    """
    A connection is created when a user seaking help on a skill already has a user with that skill
    having a Schedule where is_request is None
    """

    taker = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="connections_taken"
    )
    giver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="connections_given"
    )
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="connections_schedule"
    )
    is_activated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ManyToManyField(Message, related_name="connections_messages")
