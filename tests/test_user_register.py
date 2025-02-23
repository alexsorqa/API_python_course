from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest


class TestUserRegister(BaseCase):
    required_fields = ["username", "firstName", "lastName", "email", "password"]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'

        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'abracadabra_example.com'

        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        response_text = response.content.decode("utf-8")
        assert response_text == "Invalid email format", f"Unexpected response message: {response_text}"

    @pytest.mark.parametrize("missing_field", required_fields)
    def test_create_user_with_missing_parameter(self, missing_field):
        data = self.prepare_registration_data()
        data.pop(missing_field)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missing_field}", \
            f"Unexpected response message: {response.content.decode('utf-8')}"

    def test_create_user_with_short_first_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'A'

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert "The value of 'firstName' field is too short" in response.content.decode("utf-8"), \
            f"Unexpected response message: {response.content.decode('utf-8')}"

    def test_create_user_with_long_first_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'A' * 251

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert "The value of 'firstName' field is too long" in response.content.decode("utf-8"), \
            f"Unexpected response message: {response.content.decode('utf-8')}"


