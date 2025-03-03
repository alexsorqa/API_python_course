from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
import allure


@allure.feature("User Registration")
class TestUserRegister(BaseCase):
    required_fields = ["username", "firstName", "lastName", "email", "password"]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Verifies successful user creation")
    @allure.tag("smoke")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Checks rejection of duplicate email")
    @allure.tag("negative")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Ensures invalid email format is rejected")
    @allure.tag("negative")
    def test_create_user_with_incorrect_email(self):
        email = 'abracadabra_example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response message: {response.content.decode('utf-8')}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Verifies rejection when required fields are missing")
    @allure.tag("negative")
    @pytest.mark.parametrize("missing_field", required_fields)
    def test_create_user_with_missing_parameter(self, missing_field):
        data = self.prepare_registration_data()
        data.pop(missing_field)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missing_field}", \
            f"Unexpected response message: {response.content.decode('utf-8')}"

    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Checks rejection of too-short firstName")
    @allure.tag("negative")
    def test_create_user_with_short_first_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'A'
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert "too short" in response.content.decode("utf-8"), \
            f"Unexpected response message: {response.content.decode('utf-8')}"

    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Checks rejection of too-long firstName")
    @allure.tag("negative")
    def test_create_user_with_long_first_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'A' * 251
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert "too long" in response.content.decode("utf-8"), \
            f"Unexpected response message: {response.content.decode('utf-8')}"