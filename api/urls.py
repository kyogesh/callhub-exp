from django.urls import path

from .views import (home, TicketListApiView, TicketRetrieveUpdateDestroyApiView,
                    UserTicketsApiView, TicketsWithTagApiView, TagListCreateApiView,
                    SearchApiView)

app_name = 'api'

urlpatterns = (
    path('', home, name='home'),
    path('tickets/', TicketListApiView.as_view(), name='ticket-list'),
    path('ticket/<int:pk>/', TicketRetrieveUpdateDestroyApiView.as_view(), name='ticket-detail'),
    path('user-tickets/', UserTicketsApiView.as_view(), name='user-tickets'),
    path('tickets-with-tag/<str:tag>/', TicketsWithTagApiView.as_view(), name='tickets-with-tag'),
    path('tag/', TagListCreateApiView.as_view(), name='tag'),
    path('search/', SearchApiView.as_view(), name='search'),
)
