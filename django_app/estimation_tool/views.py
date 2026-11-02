from rest_framework import viewsets
from rest_framework.generics import CreateAPIView

from .models import Estimation, Platform
from .serializers import EstimationSerializer, PlatformSerializer, RetrievePlatformSerializer


class PlatformListViewSet(viewsets.ReadOnlyModelViewSet):
    """Returns list of platform id's or retrieve detailed information about chosen platform."""

    queryset = Platform.objects
    serializer_class = PlatformSerializer

    def get_serializer_class(self):
        # Such architecture made to minimise the amount of information sent as a response

        if self.action == "list":  # Get all platforms id's
            return PlatformSerializer

        # Retrieve detailed information about chosen platform
        return RetrievePlatformSerializer


class EstimationCreationView(CreateAPIView):
    """Returns estimation based on chosen options and hourly rate."""

    queryset = Estimation.objects
    serializer_class = EstimationSerializer
