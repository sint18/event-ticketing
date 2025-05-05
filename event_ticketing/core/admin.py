from django.contrib import admin
from .models import Event, Ticket, Purchase # Import your models

# Register Event model
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'organizer', 'date', 'time', 'location')
    list_filter = ('date', 'location')
    search_fields = ('event_name', 'location', 'organizer__username')
    raw_id_fields = ('organizer',) # Use a raw ID field for the organizer ForeignKey for large numbers of users

# Register Ticket model
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_type', 'event', 'price', 'quantity_available', 'quantity_sold', 'quantity_remaining')
    list_filter = ('event', 'ticket_type')
    search_fields = ('ticket_type', 'event__event_name')
    raw_id_fields = ('event',) # Use a raw ID field for the event ForeignKey

# Register Purchase model
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticket', 'quantity', 'total_price', 'purchase_time')
    list_filter = ('purchase_time', 'ticket__event__event_name')
    search_fields = ('user__username', 'ticket__ticket_type', 'ticket__event__event_name')
    raw_id_fields = ('user', 'ticket') # Use raw ID fields for ForeignKeys
    readonly_fields = ('total_price', 'purchase_time') # These fields are calculated/set automatically
