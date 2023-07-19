import ds_protocol
import unittest
import time

class ds_protocol_test(unittest.TestCase):
    def test_join(self):
        username = 'test_usr'
        password = 'test_pwd'
        join = ds_protocol.join(username, password)
        test = {"join": {"username": username, "password": password, "token": ''}}
        self.assertEqual(join, test)


    def test_post(self):
        message = 'test_msg'
        token = 'test_token'
        post = ds_protocol.post(message, token)
        test = {"token": token, "post": {"entry": message, "timestamp": time.time()}}
        self.assertEqual(post, test)


    def test_bio(self):
        bio = "test_bio"
        token = 'test_token'
        json_bio = ds_protocol.bio(bio, token)
        test_json_bio =  {"token": token, "bio": {"entry": bio, "timestamp": time.time()}}
        self.assertEqual(json_bio, test_json_bio)
        

    def test_send_message_to_user(self):
        test_token = 'test_token'
        test_entry = 'test_entry'
        test_recipient = 'test_recipient'
        data = ds_protocol.send_message_to_user(test_token, test_entry, test_recipient)
        test = data = {"token": test_token, "directmessage": {"entry": test_entry, "recipient": test_recipient, "timestamp": time.time()}}
        self.assertEqual(data, test)

    
    def test_get_unread_message(self):
        test = {'token': 'test_token', 'directmessage': 'new'}
        data = ds_protocol.get_unread_message('test_token')
        self.assertEqual(data, test)


    def test_get_all_message(self):
        test = {'token': 'test_token', 'directmessage': 'all'}
        data = ds_protocol.get_all_message('test_token')
        self.assertEqual(data, test)


if __name__ == '__main__':
    unittest.main()
