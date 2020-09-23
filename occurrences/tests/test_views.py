# -*- coding: utf-8 -*-
import pytest
from django.contrib.auth.models import User
from pytest import mark
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate, APIRequestFactory

from occurrences.views import OccurrenceViewSet


@mark.usefixtures("create_users_registers")
class TestCreateAuthorView(APITestCase):

    @pytest.mark.urls('occurrences.urls')
    def test_get_queryset(self):
        url = reverse('occurrences-list')

        response_not_authenticated = self.client.get(url)

        factory = APIRequestFactory()
        user = User.objects.get(username='admin')
        view = OccurrenceViewSet.as_view({'get': 'list'})
        request = factory.get(url)
        force_authenticate(request, user=user)
        response_authenticated = view(request)

        assert response_not_authenticated.status_code == 403
        assert response_authenticated.status_code == 200
