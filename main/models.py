from django.db import models

class URLShortener(models.Model):
    original_url = models.URLField(max_length=2048, unique=True)
    short_url = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.original_url} -> {self.short_url}"
