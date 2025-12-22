from django.db import models


class Crane(models.Model):
    name = models.CharField(max_length=255)
    is_subrented = models.BooleanField(default=False)
    owner_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
