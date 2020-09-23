# -*- coding: utf-8 -*-

import pytest
from django.contrib.auth.models import User


@pytest.fixture
def create_users_registers(db):  # the db argument will make sure the database access is requested for this fixture
    User.objects.create(username='admin', password='a', is_staff=True, is_active=True, is_superuser=True)
    User.objects.create(username='manuel1', password='a', is_staff=False, is_active=True, is_superuser=False)

