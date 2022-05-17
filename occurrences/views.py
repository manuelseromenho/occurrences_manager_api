from django.contrib.auth import get_user_model  # If used custom user model
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status
from rest_framework import permissions
from rest_framework import renderers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from occurrences.filters import OccurrenceFilter
from occurrences.models import Occurrence, Pizza
from occurrences.permissions import DontAllowCreateAdmin
from occurrences.serializers import OccurrenceSerializer, AuthorSerializer, CreateAuthorSerializer, \
    PizzaDetailsSerializer


class OccurrenceViewSet(viewsets.ModelViewSet):
    """ This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Occurrence.objects.all()
    serializer_class = OccurrenceSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OccurrenceFilter

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'partial_update':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """
        Overrides get_queryset method to be able to build a queryset for the geo location
        """
        qs = super().get_queryset()

        pnt_str = self.request.query_params.get('geo_location', None)
        radius = self.request.query_params.get('radius', None)
        if pnt_str and radius:
            pnt_obj = GEOSGeometry(f'POINT({pnt_str})')
            qs = qs.filter(geo_location__distance_lte=(pnt_obj, D(km=radius)))

        return qs


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class CreateAuthorView(generics.CreateAPIView):
    """
    Manage the creation of an superuser author so that only a superuser can create
    another superuser.
    """
    model = get_user_model()
    permission_classes = [
        DontAllowCreateAdmin,
        IsAuthenticated
    ]
    serializer_class = CreateAuthorSerializer


class ListCreateUpdateDeleteView(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PizzaView(ListCreateUpdateDeleteView):
    serializer_class = PizzaDetailsSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Pizza.objects.all()

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            pizza_obj = Pizza.objects.filter(pk=kwargs['id'])
        else:
            pizza_obj = Pizza.objects.all()
        serializer = self.serializer_class(pizza_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(instance='', data=data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(instance='', data=data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
