from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from .serializers import SiteSettingsSerializers, ContactSerializers, TeamSerializers
from rest_framework.response import Response
from rest_framework import status
from sitesetting.models import Site, Contact, Team



class SiteView(GenericAPIView):
    """
    for get the site settings infos
    """

    serializer_class = SiteSettingsSerializers

    def get(self, request, *args, **kwargs):
        return Response(self.serializer_class(Site.objects.first()).data, status=status.HTTP_200_OK)


class TeamView(ListAPIView):
    """
    for list the team infos
    """

    serializer_class = TeamSerializers
    queryset = Team.objects.filter(is_active=True).all()


class ContactView(CreateAPIView):
    """
    for create contact us obj
    """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializers

 

