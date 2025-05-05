from rest_framework import serializers
from .models import Event, Ticket, Purchase


# ================ Ticket Serializers ================ #
class TicketSerializer(serializers.ModelSerializer):
    quantity_remaining = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "ticket_type", "price", "quantity_remaining")


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
        fields = (
            "id",
            "event_name",
            "description",
            "date",
            "time",
            "location",
            "organizer",
            "tickets",
        )


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        # Organizer will be automatically set based on the logged-in user
        fields = ("event_name", "description", "date", "time", "location")


# =============== Purchase Serializers =============== #
class TicketPurchaseSerializer(serializers.Serializer):
    ticket_id = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())
    quantity = serializers.IntegerField()

    def validate(self, data):
        ticket = data["ticket_id"]
        quantity = data["quantity"]

        if quantity <= 0:
            raise serializers.ValidationError("Quantity must be positive.")

        if quantity > ticket.quantity_remaining:
            raise serializers.ValidationError("Not enough tickets available.")

        return data

    def save(self):
        # This save method will handle the purchase logic
        ticket = self.validated_data["ticket_id"]
        quantity = self.validated_data["quantity"]
        user = self.context["request"].user  # Get the current user from the request

        # Create the Purchase record
        purchase = Purchase.objects.create(
            user=user,
            ticket=ticket,
            quantity=quantity,
            total_price=quantity * ticket.price,
        )

        # Update the ticket's quantity sold
        ticket.quantity_sold += quantity
        ticket.save()

        return purchase


class PurchaseSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(read_only=True)  # Include ticket details

    class Meta:
        model = Purchase
        fields = ("id", "ticket", "quantity", "total_price", "purchase_time")


# ================ Analysis Serializers ================ #
class AnalyticsSerializer(serializers.Serializer):
    total_tickets_sold = serializers.IntegerField()
    total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
    number_of_events = serializers.IntegerField()
