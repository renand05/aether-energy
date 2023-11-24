from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from unittest import mock

from utilities.views import website_demo
from utilities.models import User

from pydantic import BaseModel

class WebsiteDemoRequest(BaseModel):
    user_address: str
    user_consumption: str
    user_percentage_scale: str

@mock.patch('django.template.context_processors.get_token', mock.Mock(return_value='predicabletoken'))
class WebsiteDemoTest(TestCase):
    def build_post_website_demo_body(self) -> WebsiteDemoRequest:
        return WebsiteDemoRequest(
            user_address='Black Star #45',
            user_consumption='15',
            user_percentage_scale='10'
        )

    def test_root_url_resolves_to_website_view(self) -> None:
        found = resolve('/')
        self.assertEqual(found.func, website_demo)
    
    def test_website_has_correct_html_title(self) -> None:
        request = HttpRequest()
        response = website_demo(request=request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Aether Energy Utilities Demo</title>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))
    
    def test_website_can_save_a_POST_request(self) -> None:
        request = HttpRequest()
        request.method = 'POST'
        request.POST = self.build_post_website_demo_body().model_dump()
        response = website_demo(request=request)
        self.assertIn('user_form', response.content.decode())
        expected_html = render_to_string(
            'website_demo.html',
            {'new_user_address': 'Black Star #45',
             'new_user_consumption': '15',
             'new_user_percentage_scale': '10'
            },
            request=request
        )
        self.assertEqual(response.content.decode(), expected_html)
 
class UserModelTest(TestCase):
    def test_saving_and_retrieving_items(self) -> None:
        first_user = User()
        first_user.firstname = 'Luke'
        first_user.lastname = 'Skywalker'
        first_user.save()
        second_user = User()
        second_user.firstname = 'Han'
        second_user.lastname = 'Solo'
        second_user.save()
        saved_users = User.objects.all()
        self.assertEqual(saved_users.count(), 2)
        first_saved_user = saved_users[0]
        second_saved_user = saved_users[1]
        self.assertEqual(first_saved_user.firstname, 'Luke')
        self.assertEqual(second_saved_user.firstname, 'Han')