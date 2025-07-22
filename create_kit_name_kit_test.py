import sender_stand_request
import data
import requests


def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


def get_kit_body(kit_name):
    current_kit_body = data.kit_body.copy()
    current_kit_body["name"] = kit_name
    return current_kit_body


def positive_assert_and_get_auth_token(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    print(user_response.content)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1

    return user_response.json()["authToken"]

def create_personal_kit(auth_token, kit_name):
    kit_body = get_kit_body(kit_name)
    kit_response = sender_stand_request.post_new_kit(kit_body, auth_token)
    return kit_response

def negative_assert(auth_token, kit_name):
    kit_body = get_kit_body(kit_name)
    print("Body enviado a la API:", kit_body)
    kit_response = sender_stand_request.post_new_kit(kit_body, auth_token)

    assert kit_response.status_code == 400, f"Esperado Status 400 al crear kit, Obtenido {kit_response.status_code}. "
    return kit_response


def test_create_a_kit_with_one_character_name():
   auth_token = positive_assert_and_get_auth_token("Andrea")
   create_personal_kit(auth_token, "a")

def test_create_a_kit_with_511_characters_name():
    auth_token = positive_assert_and_get_auth_token("Andrea")
    create_personal_kit(auth_token, "AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")

def test_create_a_kit_with_zero_characters_name():
        auth_token = positive_assert_and_get_auth_token("Andrea")
        negative_assert(auth_token, "")

def test_create_a_kit_with_512_characters_name():
        auth_token = positive_assert_and_get_auth_token("Andrea")
        long_name = "A" * 512
        response = negative_assert(auth_token, long_name)


def test_create_a_kit_with_special_characters_name():
    auth_token = positive_assert_and_get_auth_token("Andrea")
    create_personal_kit(auth_token, "№%@")

def test_create_a_kit_with_space_between_characters_name():
    auth_token = positive_assert_and_get_auth_token("Andrea")
    create_personal_kit(auth_token, "A Aaa")

def test_create_a_kit_with_str_number_name():
    auth_token = positive_assert_and_get_auth_token("Andrea")
    create_personal_kit(auth_token, "123")

def test_create_a_kit_without_name_in_the_request():
        auth_token = positive_assert_and_get_auth_token("Andrea")
        kit_body = data.kit_body.copy()
        kit_body.pop("name", None)
        response = sender_stand_request.post_new_kit(kit_body, auth_token)
        assert response.status_code == 400, f"Esperado 400 por falta de 'name', se obtuvo {response.status_code}"

def test_create_a_kit_with_numeric_type_name():
        auth_token = positive_assert_and_get_auth_token("Andrea")
        negative_assert(auth_token, 123)