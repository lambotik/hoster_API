import json

import allure
import pytest

from utils.checking import Checking

from utils.reqres_api import HosterAPI

"""Create, edit and delete a new user"""
user_id = '2'


@allure.feature('Test Hoster')
class TestHoster:

    @allure.step('test_create_new_user')
    def test_create_new_user(self):
        print('\nMethod POST: Create User')
        result_post = HosterAPI.create_new_user()
        Checking.check_json_token(result_post, ['name', 'job', 'id', 'createdAt'])
        Checking.check_status_code(result_post, 201)
        Checking.check_json_value(result_post, 'name', "lambotik")
        new_id = json.loads(result_post.text)['id']
        Checking.check_json_search_word_in_value(result_post, 'id', new_id)
        Checking.check_json_search_word_in_value(result_post, 'job', 'qa')

    @allure.step('test_info_user')
    @pytest.mark.xfail
    def test_info_user(self):
        print('\nMethod GET: Check user info')
        result_get = HosterAPI.checking_new_user(user_id)
        result_get_new_user = json.loads(result_get.text)
        Checking.check_status_code(result_get, 200)
        Checking.check_json_token(result_get, ['data', 'support'])
        Checking.check_json_many_tokens(result_get, 'data', ['id', 'email', 'first_name', 'last_name', 'avatar'])
        Checking.check_json_many_tokens(result_get, 'support', ['url', 'text'])
        Checking.check_json_search_word_in_values(result_get_new_user['support'], 'url',
                                                  "https://reqres.in/#support-heading")
        Checking.check_json_search_word_in_values(result_get_new_user['data'], 'id', user_id)

    @allure.step('test_update_user_info')
    def test_update_user_info(self):
        print('\nMethod PUT: Update user data')
        result_put = HosterAPI.put_new_user(user_id)
        Checking.check_status_code(result_put, 200)
        Checking.check_json_token(result_put, ['name', 'job', 'updatedAt'])
        Checking.check_json_value(result_put, 'name', 'morpheus')
        Checking.check_json_value(result_put, 'job', 'zion resident')

    @allure.step('test_delete_user')
    def test_delete_user(self):
        print('\nMethod DELETE: Delete user data')
        result_delete = HosterAPI.delete_new_user(user_id)
        Checking.check_status_code(result_delete, 204)
