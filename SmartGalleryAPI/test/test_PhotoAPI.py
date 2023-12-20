import datetime

from django.test import TestCase
from ..models import Photo, User
from ..test.baseTestCase import HelperTestCase
import json
# Create your tests here.


class PhotoListAPITests(HelperTestCase):
    def test_create_photo(self):
        response = self.client.post('/SmartGalleryAPI/PhotoApi', {
            'Path': 'testpath',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Photo.objects.count(), 1)
        self.assertEqual(Photo.objects.get().Path, 'testpath')
        self.assertEqual(Photo.objects.get().User, self.user)

    def test_get_photos(self):
        for _ in range(5):
            Photo.objects.create(
                Path='testpath',
                User=self.user
            )
        response = self.client.get('/SmartGalleryAPI/PhotoApi')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0]['Path'], 'testpath')
        self.assertEqual(response.data[0]['User'], self.user.id)


class PhotoDetalAPITests(HelperTestCase):
    def test_get_photo(self):
        for _ in range(5):
            Photo.objects.create(
                Path='testpath',
                User=self.user
            )
        response = self.client.get('/SmartGalleryAPI/PhotoApi/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Path'], 'testpath')
        self.assertEqual(response.data['User'], self.user.id)

    def test_get_photo_not_found(self):
        response = self.client.get('/SmartGalleryAPI/PhotoApi/1')
        self.assertEqual(response.status_code, 400)

    def test_delete_photo(self):
        for _ in range(5):
            Photo.objects.create(
                Path='testpath',
                User=self.user
            )
        response = self.client.delete('/SmartGalleryAPI/PhotoApi/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Photo.objects.count(), 4)

    def test_delete_photo_not_found(self):
        response = self.client.delete('/SmartGalleryAPI/PhotoApi/1')
        self.assertEqual(response.status_code, 400)

    def test_update_photo(self):
        Photo.objects.create(
            Path='testpath',
            User=self.user
        )
        response = self.client.put('/SmartGalleryAPI/PhotoApi/1', json.dumps({
            'Path': 'testpath1',
            'Date': '2020-01-01'
        }),content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Photo.objects.get().Path, 'testpath1')
        self.assertEqual(Photo.objects.get().User, self.user)
