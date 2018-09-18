from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

from .models import Ticket

User = get_user_model()


class TicketListCreateTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@user.com', first_name='Test',
                                        last_name='User', password='masspass')
        self.headers = {"HTTP_AUTHORIZATION": "Token {}".format(self.user.auth_token.key)}

    def test_create_ticket_successfully(self):
        data = {"title": "Test title", "description": "Test Description", "reporter": self.user.id,
                "type": "minor", "status": "backlog", "tags": [{"text": "tag1"}, {"text": "tag2"}]}
        resp = self.client.post('/tickets/', data, **self.headers, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['title'], 'Test title')

    def test_create_ticket_with_invalid_type(self):
        data = {"title": "Test title", "description": "Test Description",
                "type": "severe", "status": "backlog", "tags": [{"text": "tag1"}, {"text": "tag2"}]}
        resp = self.client.post('/tickets/', data, **self.headers, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('type' in resp.data)

    def test_create_ticket_with_invalid_status(self):
        data = {"title": "Test title", "description": "Test Description",
                "type": "major", "status": "under progress", "tags": [{"text": "tag1"}, {"text": "tag2"}]}
        resp = self.client.post('/tickets/', data, **self.headers, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('status' in resp.data)

    def test_ticket_listing(self):
        Ticket.objects.create(title='Test title', description='Test desc', reporter=self.user, type='minor',
                              status='in progress')
        resp = self.client.get('/tickets/', {}, **self.headers, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['type'], 'minor')


class TicketRetrieveUpdateDeleteTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@user.com', first_name='Test',
                                        last_name='User', password='masspass')
        self.headers = {"HTTP_AUTHORIZATION": "Token {}".format(self.user.auth_token.key)}
        self.ticket = Ticket.objects.create(title='Test title', description='Test desc', reporter=self.user,
                                            type='minor', status='in progress')

    def test_retrieve_ticket(self):
        resp = self.client.get('/ticket/{}/'.format(self.ticket.id), {}, **self.headers, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['status'], 'in progress')

    def test_update_ticket(self):
        data = {"title": "Test title updated", "description": "Test Description", "reporter": self.user.id,
                "type": "blocker", "status": "in progress"}
        resp = self.client.put('/ticket/{}/'.format(self.ticket.id), data, **self.headers, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['title'], 'Test title updated')
        self.assertEqual(resp.data['type'], 'blocker')

    def test_delete_ticket(self):
        resp = self.client.delete('/ticket/{}/'.format(self.ticket.id), {}, **self.headers, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(resp.data)


class UserTicketTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@user.com', first_name='Test',
                                        last_name='User', password='masspass')
        self.headers = {"HTTP_AUTHORIZATION": "Token {}".format(self.user.auth_token.key)}
        self.ticket = Ticket.objects.create(title='Test title', description='Test desc', reporter=self.user,
                                            type='minor', status='in progress')

    def test_list_user_tickets(self):
        resp = self.client.get('/user-tickets/', {}, **self.headers, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['title'], 'Test title')


class SearchTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@user.com', first_name='Test',
                                        last_name='User', password='masspass')
        self.headers = {"HTTP_AUTHORIZATION": "Token {}".format(self.user.auth_token.key)}
        data_list = [{"title": "Test title one", "description": "Test Description one",
                      "type": "major", "status": "backlog", "tags": [{"text": "tag10"}, {"text": "tag23"}]},
                     {"title": "Test title two", "description": "Test Description two",
                      "type": "minor", "status": "backlog", "tags": [{"text": "tag12"}, {"text": "tag24"}]},
                     {"title": "Test title three", "description": "Test Description three",
                      "type": "critical", "status": "backlog", "tags": [{"text": "tag14"}, {"text": "tag25"}]},
                     {"title": "Test title four", "description": "Test Description four",
                      "type": "blocker", "status": "backlog", "tags": [{"text": "tag16"}, {"text": "critical"}]}]

        for data in data_list:
            self.client.post('/tickets/', data, **self.headers, format='json')

    def test_search_with_results_in_tag(self):
        resp = self.client.post('/search/', dict(search_text='tag1'), **self.headers, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 4)
        self.assertEqual(resp.data[0]['description'], 'Test Description one')

    def test_search_with_no_results(self):
        resp = self.client.post('/search/', dict(search_text='qwert'), **self.headers, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 0)

    def test_search_with_results_in_type(self):
        resp = self.client.post('/search/', dict(search_text='block'), **self.headers, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['title'], 'Test title four')

    def test_search_with_results_in_tag_and_type(self):
        resp = self.client.post('/search/', dict(search_text='crit'), **self.headers, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)
        self.assertEqual(resp.data[0]['title'], 'Test title three')


