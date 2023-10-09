from rest_framework.test import APITestCase
from django.urls import reverse
from cancillaria.models import Cancillaria
from cancillaria.serializers import CancillariaSerializer
from rest_framework import status

class CancillariaApiTestCase(APITestCase):
    def test_get_list(self):
        cancillaria_1 = Cancillaria.objects.create(name='карандаш', price=15)
        cancillaria_2 = Cancillaria.objects.create(name='ручка', price=21)

        response = self.client.get(reverse('cancillaria_api_list'))

        serial_data = CancillariaSerializer([cancillaria_1, cancillaria_2], many=True).data
        serial_data = {'cancillaria_list': serial_data}

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serial_data, response.data)