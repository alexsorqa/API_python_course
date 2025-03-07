from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.feature("User Editing")
class TestUserEdit(BaseCase):
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Verifies editing a newly created user's firstName")
    @allure.tag("smoke")
    def test_edit_just_created_user(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        login_data = {'email': email, 'password': password}
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response3, 200)

        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Ensures editing fails without authentication")
    @allure.tag("negative")
    def test_update_user_not_logged_in(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        user_id = self.get_json_value(response1, "id")

        new_name = "Unauthorized Update"
        response2 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response2, 400)
        error = self.get_json_value(response2, "error")
        assert error == "Auth token not supplied", f"Expected 'Auth token not supplied', got '{error}'"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Verifies that one user cannot edit another user's data")
    @allure.tag("negative")
    def test_update_another_user(self):
        user_a_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=user_a_data)
        Assertions.assert_code_status(response1, 200)
        user_a_id = self.get_json_value(response1, "id")

        user_b_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=user_b_data)
        Assertions.assert_code_status(response2, 200)

        login_data = {"email": user_b_data["email"], "password": user_b_data["password"]}
        response3 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        new_name = "Updated by Another"
        response4 = MyRequests.put(
            f"/user/{user_a_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response4, 403)

    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Ensures invalid email formats are rejected during edit")
    @allure.tag("negative")
    def test_update_email_invalid_format(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        user_id = self.get_json_value(response1, "id")

        login_data = {"email": register_data["email"], "password": register_data["password"]}
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        invalid_email = "invalidemail.com"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": invalid_email}
        )
        Assertions.assert_code_status(response3, 400)
        error = self.get_json_value(response3, "error")
        assert error == "Invalid email format", f"Expected 'Invalid email format', got '{error}'"

    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Checks rejection of too-short firstName during edit")
    @allure.tag("negative")
    def test_update_firstname_too_short(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        user_id = self.get_json_value(response1, "id")

        login_data = {"email": register_data["email"], "password": register_data["password"]}
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        short_name = "A"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": short_name}
        )
        Assertions.assert_code_status(response3, 400)
        error = self.get_json_value(response3, "error")
        assert error == "The value for field `firstName` is too short", \
            f"Expected 'The value for field `firstName` is too short', got '{error}'"