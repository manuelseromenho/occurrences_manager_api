from django.contrib.auth import get_user_model  # If used custom user model
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from occurrences.filters import OccurrenceFilter
from occurrences.models import Occurrence, Category
from occurrences.permissions import DontAllowCreateAdmin
from occurrences.serializers import OccurrenceSerializer, AuthorSerializer, CreateAuthorSerializer


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
    #     category = self.request.POST.get('category')
    #     try:
    #         category_obj = Category.objects.get(type=category)
    #     except Category.DoesNotExist as e:
    #         raise NotFound(e)

        # pnt_str = self.request.POST.get('geo_location')
        # if pnt_str:
        #     pnt_obj = GEOSGeometry(f'POINT({pnt_str})')
        #     serializer.save(author=self.request.user, geo_location=pnt_obj, category=category_obj)
        # else:
        #     try:
        #         serializer.save(author=self.request.user, category=category_obj)
        #     except IntegrityError as e:
        #         print(e)

    # def perform_update(self, serializer):
    #     category = self.request.POST.get('category')
    #     try:
    #         category_obj = Category.objects.get(type=category)
    #     except Category.DoesNotExist as e:
    #         raise NotFound(e)
    #         return Response({"Error:": e} )
    #         #
    #
    #     pnt_str = self.request.POST.get('geo_location')
    #     if pnt_str:
    #         pnt_obj = GEOSGeometry(f'POINT({pnt_str})')
    #         serializer.save(author=self.request.user, geo_location=pnt_obj, category=category_obj)
    #     else:
    #         try:
    #             serializer.save(author=self.request.user, category=category_obj)
    #         except IntegrityError as e:
    #             print(e)

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
