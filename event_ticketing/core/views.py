# In accounts/views.py (or events/views.py)
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from .models import Event, Ticket
from django.shortcuts import get_object_or_404
from .serializers import (
    EventSerializer,
    EventCreateUpdateSerializer,
    TicketSerializer,
    TicketCreateUpdateSerializer,
)
from .permissions import (
    IsOrganizer,
    IsOrganizerOrReadOnly,
)  # Import the custom permission


@extend_schema(tags=["Event Management (Organizer)"])
class EventViewSet(viewsets.ModelViewSet):

    queryset = Event.objects.all()
    permission_classes = [
        IsOrganizer,
        IsOrganizerOrReadOnly,
    ]  # Only organizers can manage events

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return EventCreateUpdateSerializer
        return EventSerializer

    def get_queryset(self):
        # Organizers can only manage their own events
        return self.queryset.filter(organizer=self.request.user)

    def perform_create(self, serializer):
        # Set the organizer of the event to the logged-in user
        serializer.save(organizer=self.request.user)

@extend_schema(tags=['Ticket Management (Organizer)'])
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    permission_classes = [IsOrganizer]  # Only organizers can manage tickets

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TicketCreateUpdateSerializer
        return TicketSerializer

    def get_queryset(self):
        # Ensure tickets are fetched for a specific event and by the event's organizer
        event_id = self.kwargs.get("event_pk")
        if not event_id:
            return Ticket.objects.none()  # Or handle error appropriately

        event = get_object_or_404(Event, pk=event_id, organizer=self.request.user)
        return self.queryset.filter(event=event)

    def perform_create(self, serializer):
        # Set the event for the new ticket based on the URL and verify organizer
        event_id = self.kwargs.get("event_pk")
        event = get_object_or_404(Event, pk=event_id, organizer=self.request.user)
        serializer.save(event=event)

    def perform_update(self, serializer):
        event_id = self.kwargs.get("event_pk")
        get_object_or_404(
            Event, pk=event_id, organizer=self.request.user
        )  # Verify organizer
        serializer.save()

    def perform_destroy(self, instance):
        event_id = self.kwargs.get("event_pk")
        get_object_or_404(
            Event, pk=event_id, organizer=self.request.user
        )  # Verify organizer
        instance.delete()
