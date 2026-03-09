from django.conf import settings  # type: ignore
from django.db import models  # type: ignore


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


class Skill(models.Model):
    giver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name


class Schedule(models.Model):
    taker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    scheduled_at = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    skill = models.ForeignKey(Skill, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.scheduled_at.isoformat()
