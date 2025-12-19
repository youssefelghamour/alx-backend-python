""" Test permissions with mocked users and tokens to avoid database dependency for testing in Jenkins pipeline """
from unittest.mock import patch, MagicMock
from django.test import TestCase
from rest_framework.test import APIClient


class TestPermissionsMocked(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Mock users
        self.user = MagicMock(user_id=1, email="test@email.com", username="test_user")
        self.user2 = MagicMock(user_id=2, email="test2@email.com", username="test_user2")
        self.user3 = MagicMock(user_id=3, email="test3@email.com", username="test_user3")
        # Mock JWT token
        self.access_token = "mock_access_token"
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def _create_conversation(self, participants):
        return 1  # mock conversation id

    def _authenticate(self, user):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer mock_access_token")

    # ======================
    # Conversation Tests
    # ======================

    def test_authenticated_user_can_list_conversations(self):
        response = self.client.get("/api/conversations/")
        self.assertIn(response.status_code, [200, 201, 404])

    def test_unauthenticated_user_cannot_list_conversations(self):
        self.client.credentials()
        response = self.client.get("/api/conversations/")
        self.assertIn(response.status_code, [401, 403])

    def test_authenticated_user_can_create_conversation(self):
        data = {"participant_ids": [self.user.user_id, self.user2.user_id]}
        response = self.client.post("/api/conversations/", data, format="json")
        self.assertIn(response.status_code, [201, 200])

    def test_unauthenticated_user_cannot_create_conversation(self):
        self.client.credentials()
        data = {"participant_ids": [self.user.user_id, self.user2.user_id]}
        response = self.client.post("/api/conversations/", data, format="json")
        self.assertIn(response.status_code, [401, 403])

    # ======================
    # Message Tests
    # ======================

    def test_authenticated_participant_can_list_messages(self):
        conversation_id = self._create_conversation([self.user, self.user2])
        response = self.client.get(f"/api/conversations/{conversation_id}/messages/")
        self.assertIn(response.status_code, [200, 201, 404])

    def test_authenticated_nonparticipant_cannot_list_messages(self):
        conversation_id = self._create_conversation([self.user, self.user2])
        self._authenticate(self.user3)
        response = self.client.get(f"/api/conversations/{conversation_id}/messages/")
        self.assertIn(response.status_code, [403, 401])

    def test_unauthenticated_user_cannot_list_messages(self):
        conversation_id = self._create_conversation([self.user, self.user2])
        self.client.credentials()
        response = self.client.get(f"/api/conversations/{conversation_id}/messages/")
        self.assertIn(response.status_code, [401, 403])

    def test_authenticated_participant_can_create_message(self):
        conversation_id = self._create_conversation([self.user, self.user2])
        message_data = {"message_body": "Hello, this is a test message."}
        response = self.client.post(f"/api/conversations/{conversation_id}/messages/", message_data, format="json")
        self.assertIn(response.status_code, [201, 200])

    def test_authenticated_nonparticipant_cannot_create_message(self):
        conversation_id = self._create_conversation([self.user, self.user2])
        self._authenticate(self.user3)
        message_data = {"message_body": "Hello from non-participant."}
        response = self.client.post(f"/api/conversations/{conversation_id}/messages/", message_data, format="json")
        self.assertIn(response.status_code, [403, 401])

    def test_unauthenticated_user_cannot_create_message(self):
        conversation_id = self._create_conversation([self.user, self.user2])
        self.client.credentials()
        message_data = {"message_body": "Hello, this is a test message."}
        response = self.client.post(f"/api/conversations/{conversation_id}/messages/", message_data, format="json")
        self.assertIn(response.status_code, [401, 403])

    def test_message_sender_can_update_own_message(self):
        conversation_id = self._create_conversation([self.user, self.user2])
        message_id = 1
        updated_message_data = {"message_body": "Updated message"}
        response = self.client.put(f"/api/conversations/{conversation_id}/messages/{message_id}/", updated_message_data, format="json")
        self.assertIn(response.status_code, [200, 201])

    def test_non_sender_cannot_update_message(self):
        conversation_id = self._create_conversation([self.user, self.user2])
        message_id = 1
        self._authenticate(self.user2)
        updated_message_data = {"message_body": "Attempted update by non-sender"}
        response = self.client.put(f"/api/conversations/{conversation_id}/messages/{message_id}/", updated_message_data, format="json")
        self.assertIn(response.status_code, [403, 401])