from django.test import TestCase
from django.shortcuts import render, get_object_or_404, render_to_response
import pytest


# Create your tests here.

@pytest.mark.django_db
class TestViews:

    def test_views(self,request):
        response = render(request, '')
        assert response.status_code == 200
