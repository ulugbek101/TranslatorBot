from django.db import models


class Profile(models.Model):
    chat_id = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200, null=True)
    word = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = ('chat_id', "word")

    def __str__(self):
        return self.chat_id



