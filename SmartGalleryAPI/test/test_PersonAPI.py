import datetime

from ..models import Person, User
from ..test.baseTestCase import HelperTestCase
import json
# Create your tests here.


class PersonListAPITests(HelperTestCase):
    def test_create_person(self):
        response = self.client.post('/SmartGalleryAPI/PersonApi', {
            'Name': 'testname',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Person.objects.get().Name, 'testname')
        self.assertEqual(Person.objects.get().User, self.user)

    def test_get_persons(self):
        for _ in range(5):
            Person.objects.create(
                Name='testname',
                User=self.user
            )
        response = self.client.get('/SmartGalleryAPI/PersonApi')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0]['Name'], 'testname')
        self.assertEqual(response.data[0]['User'], self.user.id)

    def test_get_persons_not_found(self):
        response = self.client.get('/SmartGalleryAPI/PersonApi')
        self.assertEqual(response.status_code, 200)

class PersonDetalAPITests(HelperTestCase):

    def test_get_person(self):
        for _ in range(5):
            Person.objects.create(
                Name='testname',
                User=self.user
            )
        response = self.client.get('/SmartGalleryAPI/PersonApi/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['Name'], 'testname')
        self.assertEqual(response.data['User'], self.user.id)

    def test_get_person_not_found(self):
        
        response = self.client.get('/SmartGalleryAPI/PersonApi/1')

        self.assertEqual(response.status_code, 400)

    def test_delete_person(self):
        for _ in range(5):
            Person.objects.create(
                Name='testname',
                User=self.user
            )
        response = self.client.delete('/SmartGalleryAPI/PersonApi/1')
        self.assertEqual(response.status_code, 200)

    def test_delete_person_not_found(self):
        response = self.client.delete('/SmartGalleryAPI/PersonApi/1')
        self.assertEqual(response.status_code, 400)

    def test_update_person(self):
        Person.objects.create(
            Name='testname',
            User=self.user
        )
        response = self.client.put('/SmartGalleryAPI/PersonApi/1', {
            'Name': 'testname2',
        },content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Person.objects.get().Name, 'testname2')