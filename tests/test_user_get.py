from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.feature("User Data Retrieval")
class TestUserGet(BaseCase):
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Verifies limited data access without authentication")
    @allure.tag("smoke")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Checks full data access when authenticated as the same user")
    @allure.tag("smoke")
    def test_get_user_details_auth_as_same_user(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={'x-csrf-token': token},
            cookies={"auth_sid": auth_sid}
        )
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Ensures limited data access when authenticated as a different user")
    @allure.tag("regression")
    def test_get_other_user_details_when_authorized(self):
        register_data = self.prepare_registration_data()
        response_create = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response_create, 200)
        different_user_id = self.get_json_value(response_create, "id")

        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth = self.get_json_value(response1, "user_id")

        assert different_user_id != user_id_from_auth, "Test requires different user IDs"
        response2 = MyRequests.get(
            f"/user/{different_user_id}",
            headers={'x-csrf-token': token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")