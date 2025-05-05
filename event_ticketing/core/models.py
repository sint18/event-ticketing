from django.db import models
from django.conf import settings


class Event(models.Model):
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events"
    )
    event_name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.event_name)


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    ticket_type = models.CharField(max_length=100)  # e.g., 'General Admission', 'VIP'
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)
    quantity_sold = models.PositiveIntegerField(default=0)

    @property
    def quantity_remaining(self):
        return self.quantity_available - self.quantity_sold

    def __str__(self):
        return f"{self.ticket_type} for {self.event.event_name}"


class Purchase(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="purchases"
    )
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="purchases"
    )
    quantity = models.PositiveIntegerField()
    purchase_time = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.ticket.ticket_type} for {self.user.email}"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.ticket.price
        super().save(*args, **kwargs)
