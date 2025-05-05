# In accounts/views.py (or events/views.py)
from rest_framework import viewsets, generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event, Purchase, Ticket
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .serializers import (
    EventSerializer,
    EventCreateUpdateSerializer,
    PurchaseSerializer,
    TicketPurchaseSerializer,
    TicketSerializer,
    TicketCreateUpdateSerializer,
    AnalyticsSerializer,
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


@extend_schema(tags=["Ticket Management (Organizer)"])
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


@extend_schema(tags=["Event Browse (User)"])
class EventUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for Browse
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["date", "location"]  # Filter by date and location
    search_fields = ["event_name"]  # Search by event name


@extend_schema(tags=["Ticket Purchase (User)"])
class TicketPurchaseView(generics.CreateAPIView):
    serializer_class = TicketPurchaseSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can purchase

    def perform_create(self, serializer):
        # The save method in the serializer handles the purchase logic
        serializer.save()


@extend_schema(tags=["Purchase History (User)"])
class PurchaseHistoryView(generics.ListAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can view history

    def get_queryset(self):
        # Get purchase history for the currently authenticated user
        return Purchase.objects.filter(user=self.request.user).order_by(
            "-purchase_time"
        )


@extend_schema(tags=["Analytics"])
class AnalyticsView(generics.GenericAPIView):

    permission_classes = [IsOrganizer]  # Restrict access

    def get(self, request, format=None):
        # Calculate Total Tickets Sold
        # Sum the 'quantity' field from the Purchase model
        total_tickets_sold = (
            Purchase.objects.aggregate(Sum("quantity"))["quantity__sum"] or 0
        )

        # Calculate Total Sales
        # Sum the 'total_price' field from the Purchase model
        total_sales = (
            Purchase.objects.aggregate(Sum("total_price"))["total_price__sum"] or 0
        )

        # Calculate Number of Events
        number_of_events = Event.objects.count()

        # Prepare data using the serializer
        analytics_data = {
            "total_tickets_sold": total_tickets_sold,
            "total_sales": total_sales,
            "number_of_events": number_of_events,
        }
        serializer = AnalyticsSerializer(analytics_data)

        return Response(serializer.data, status=status.HTTP_200_OK)
