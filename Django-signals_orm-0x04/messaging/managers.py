from django.db import models


class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        # ✅ Use .only() to load only required fields
        return self.get_queryset().filter(
            receiver=user,
            unread=True
        ).only("id", "sender", "content", "timestamp")
