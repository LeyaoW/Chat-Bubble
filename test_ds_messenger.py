from ds_messenger import DirectMessage, DirectMessenger
import unittest
import time

class ds_messenger_test(unittest.TestCase):
    def test_DirectMessenge_init(self):
        i = {
            "sender": 'sender',
            "recipient": 'rec',
            "message": 'msg',
            "timestamp": time.time(),
        }
        dm = DirectMessage(**i)
        self.assertEqual(dm.sender, 'sender')
        self.assertEqual(dm.recipient, 'rec')
        self.assertEqual(dm.message, 'msg')
    

    def test_DirectMessenger_send(self):
        dm = DirectMessenger('168.235.86.101', 'Daddy', '123')
        test_send = dm.send('test', 'Daddy')
        self.assertTrue(test_send)


    def test_DirectMessenger_retrieve_new(self):
        dm = DirectMessenger('168.235.86.101', 'Daddy', '123')
        self.assertIs(type(dm.retrieve_new()), list)

    
    def test_DirectMessenger_retrieve_all(self):
        dm = DirectMessenger('168.235.86.101', 'Daddy', '123')
        self.assertIs(type(dm.retrieve_all()), list)


if __name__ == '__main__':
    unittest.main()
