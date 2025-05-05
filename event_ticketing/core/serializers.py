from rest_framework import serializers
from .models import Event, Ticket


# ================ Ticket Serializers ================ #
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"  # Or list specific fields


class TicketCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        # 'event' will be set based on the URL or view logic
        fields = ("ticket_type", "price", "quantity_available")


# =============== Event Serializers =============== #
class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(
        source="organizer.username"
    )  # Display organizer's username
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = "__all__"  # Include all fields for simplicity


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        # Organizer will be automatically set based on the logged-in user
        fields = ("event_name", "description", "date", "time", "location")
