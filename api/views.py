from django.shortcuts import render
from django.db.models.expressions import Q
from django.contrib.auth import get_user_model
from rest_framework import generics, authentication, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ticket, Tag
from .serializers import TicketSerializer, TagSerializer

app_label = 'api'

User = get_user_model()


def home(request):
    return render(request, 'index.html')


class TicketListApiView(APIView):
    """
    get:
    Return a list of all the Tickets.

    post:
    Create a new Ticket instance.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request):
        tags = request.data.get('tags', [])
        data = dict(request.data)
        data['reporter'] = request.user.id
        serializer = TicketSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        ticket = serializer.save()
        tags_ = [{'tag': tag['text'], 'ticket': [ticket.pk]} for tag in tags if 'text' in tag]
        tag_serializer = TagSerializer(data=tags_, many=True)
        if not tag_serializer.is_valid():
            ticket.delete()
            return Response(tag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        tag_objs = tag_serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TicketsWithTagApiView(APIView):
    """
    get:
    Returns list of all the tickets with a given tag
    """

    def get(self, request, tag):
        tag = Tag.objects.filter(tag=tag).prefetch_related('ticket')
        serializer = TicketSerializer(tag.first().ticket.all(), many=True)
        return Response(serializer.data)


class SearchApiView(APIView):
    """
    post:
    Returns search result for a 'search_text' in tag or tickets' type.
    """

    def post(self, request):
        search_text = request.data['search_text']
        tags = Tag.objects.filter(tag__icontains=search_text).prefetch_related('ticket')
        tickets = Ticket.objects.filter(type__icontains=search_text)
        tickets_list = list(tickets)
        [tickets_list.extend(tag.ticket.all()) for tag in tags]
        tickets_list = list(set(tickets_list))
        serializer = TicketSerializer(tickets_list, many=True)
        return Response(serializer.data)


class TagListCreateApiView(generics.ListCreateAPIView):
    """
    get:
    Returns all Tag instances

    post:
    Creates a new Tag instance
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TicketRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns a Ticket instance for given 'pk'

    put:
    Update a Ticket instance for given 'pk'

    delete:
    Deletes a Ticket instance for given 'pk'
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Ticket.objects.all().order_by('-created')
    serializer_class = TicketSerializer


class UserTicketsApiView(APIView):
    """
    get:
    Returns all the Tickets where user is a 'reporter' or 'assignee'.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        tickets = Ticket.objects.filter(Q(reporter=request.user) | Q(assignee=request.user))
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
