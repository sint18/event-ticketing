# In accounts/urls.py (or events/urls.py)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsView, EventUserViewSet, EventViewSet, PurchaseHistoryView, TicketPurchaseView, TicketViewSet  # Import other views as needed

router = DefaultRouter()
router.register(r"events", EventViewSet)

# Router for user event Browse (read-only)
user_event_router = DefaultRouter()
user_event_router.register(r'events', EventUserViewSet, basename='user-event')

urlpatterns = [
    path("", include(router.urls)),
    # Nested URLs for Tickets under Events
    path(
        "events/<int:event_pk>/tickets/",
        TicketViewSet.as_view({"get": "list", "post": "create"}),
        name="event_tickets_list",
    ),
    path(
        "events/<int:event_pk>/tickets/<int:pk>/",
        TicketViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="event_tickets_detail",
    ),
    # User URLs
    path("", include(user_event_router.urls)),  # User event Browse
    path("tickets/purchase/", TicketPurchaseView.as_view(), name="ticket_purchase"),
    path("purchases/history/", PurchaseHistoryView.as_view(), name="purchase_history"),

    # Analytics URL
     path('analytics/', AnalyticsView.as_view(), name='analytics'),
]
