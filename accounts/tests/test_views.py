from unittest.mock import patch, call

from django.test import TestCase
import accounts.views
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):

    def test_sends_mail_to_address_from_post(self):
        self.send_mail_called = False

        def fake_send_mail(subject, body, from_email, to_list):
            self.send_mail_called = True
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.to_list = to_list

        accounts.views.send_mail = fake_send_mail

        self.client.post(
            '/accounts/send_login_email',
            data={
                'email': 'edith@example.com',
            }
        )

        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, "Your login link for Superlists")
        self.assertEqual(self.from_email, 'noreply@superlists')
        self.assertEqual(self.to_list, ['edith@example.com'])

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post(
            '/accounts/send_login_email',
            data={
                'email': 'edith@example.com',
            }
        )

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_mail, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_mail, 'noreply@superlists')
        self.assertEqual(to_list, ['edith@example.com'])

    def test_adds_success_message(self):
        response = self.client.post(
            '/accounts/send_login_email',
            data={
                'email': 'edith@example.com'
            }, follow=True
        )

        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in"
        )
        self.assertEqual(message.tags, 'success')

    def test_create_token_associeted_with_email(self):
        self.client.post(
            '/accounts/send_login_email',
            data={
                'email': 'edith@example.com'
            }
        )
        token = Token.objects.first()
        self.assertEqual(token.email, 'edith@example.com')

    @patch('accounts.views.auth')
    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abcd123')
        )

    @patch('accounts.views.auth')
    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )
