from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):
    def test_delete_user_id_2(self):

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)
        Assertions.assert_code_status(response1, 200)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        response2 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        error_message = self.get_json_value(response2, "error")
        assert error_message == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Expected error message 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', got '{error_message}'"

    def test_delete_user_positive(self):

        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        user_id = self.get_json_value(response1, "id")

        login_data = {
            "email": register_data["email"],
            "password": register_data["password"]
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response3, 200)

        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response4, 404)
        error_message = response4.text
        assert error_message == "User not found", \
            f"Expected 'User not found', got '{error_message}'"

    def test_delete_another_user(self):

        user_a_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=user_a_data)
        Assertions.assert_code_status(response1, 200)
        user_a_id = self.get_json_value(response1, "id")

        user_b_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=user_b_data)
        Assertions.assert_code_status(response2, 200)

        login_data = {
            "email": user_b_data["email"],
            "password": user_b_data["password"]
        }
        response3 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        response4 = MyRequests.delete(
            f"/user/{user_a_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response4, 400)
        error_message = self.get_json_value(response4, "error")
        assert error_message == "This user can only delete their own account", \
            f"Expected 'This user can only delete their own account', got '{error_message}'"