import json
from socket import *

import ds_protocol

class DirectMessage:
    def __init__(self, sender=None, recipient=None, message=None, timestamp=None):
        self.sender = sender
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp

    def save(self, p):
        try:
            f = open(p, 'a')
            json.dump(self.__dict__, f)
            f.write('\n')
            f.close()
        except:
            pass


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.username = username
        self.password = password
        self.dsuserver = dsuserver
        """
        self.socket = self._connect(dsuserver, 3021)
        self.token = self.join(username, password)
        """

    def _connect(self, server, port):
        try:
            srv = socket(AF_INET, SOCK_STREAM)
            server_address = (server, port)
            srv.connect(server_address)
            return srv
        except:
            pass
		

    def join(self, username, password):
        req = ds_protocol.join(username, password)
        self._send(req)
        json_response = self._response()
        print(json_response)
        if json_response["response"]["type"] == "ok":
            print("join success!")
        else:
            print(json_response)
        token = json_response['response']['token']
        return token


    def send(self, message:str, recipient:str) -> bool:
    # returns true if message successfully sent, false if send failed.
        self.socket = self._connect(self.dsuserver, 3021)
        self.token = self.join(self.username, self.password)
        req = ds_protocol.send_message_to_user(self.token, message, recipient)
        self._send(req)
        json_response = self._response()
        if json_response['response']['type'] == 'ok':
            print(json_response)
            self.close_socket()
            return True
        else:
            print(json_response)
            self.close_socket()
            return False

		
    def retrieve_new(self) -> list:
    # returns a list of DirectMessage objects containing all new messages
        self.socket = self._connect(self.dsuserver, 3021)
        self.token = self.join(self.username, self.password)
        req = ds_protocol.get_unread_message(self.token)
        self._send(req)
        json_response = self._response()
        message_list = []
        if json_response["response"]["type"] == "ok":
            messages = json_response["response"]["messages"]
            for msg in messages:
                i = {
                    "sender": msg["from"],
                    "recipient": self.username,
                    "message": msg["message"],
                    "timestamp": msg["timestamp"],
                }
                dm = DirectMessage(**i)
                message_list.append(dm)
        else:
            print(json_response)
        self.close_socket()
        return message_list

 
    def retrieve_all(self) -> list:
        try:
    # returns a list of DirectMessage objects containing all messages
            self.socket = self._connect(self.dsuserver, 3021)
            self.token = self.join(self.username, self.password)
            req = ds_protocol.get_all_message(self.token)
            self._send(req)
            json_response = self._response()
            message_list = []
            if json_response["response"]["type"] == "ok":
                messages = json_response["response"]["messages"]
                for msg in messages:
                    i = {
                        "sender": msg["from"],
                        "recipient": self.username,
                        "message": msg["message"],
                        "timestamp": msg["timestamp"],
                    }
                    dm = DirectMessage(**i)
                    message_list.append(dm)
            else:
                print(json_response)
            self.close_socket()
            return message_list
        except:
            pass

    
    def _response(self):
        return json.loads(self.socket.recv(10485760))


    def _send(self, req):
        self.socket.sendall(bytes(json.dumps(req), 'utf-8'))

    
    def close_socket(self):
        self.socket.close()



'''
if __name__ == '__main__':
    dm = DirectMessenger('168.235.86.101', 'Daddy', '123')
    dm.send('Hi', 'wobuzhidao')
    lst = dm.retrieve_all()
    dic = {}
    for i in lst:
        if i.sender not in dic:
            dic[i.sender] = [i]
        
    print(dic)
'''

"""
lst = [{2:1},{2,1}]
print(lst[0])
"""

'''
print(type(lst[0]))

print(lst[0].sender)
print(lst[0].recipient)
print(lst[0].message)
print(lst[0].timestamp)
{'Daddy': [Post(msg, time), Po], 'wobuzhidao': []}
{'Daddy': [Post(msg, time), Po], 'wobuzhidao': []}
{}
1. s.Profile()
s.username = sender
2. 

'''
import time
mydict = [{'Daddy': '123', 'Timestamp': '8/10/2015 13:07:38'},{'wobuzhidao': '234','Timestamp': '8/10/2015 11:51:14'},{'Counted number': '28','Timestamp': '8/10/2015 13:06:27'}, {'Counted number': '20','Timestamp': '8/10/2015 12:53:42'}]
mydict.sort(key=lambda x:time.mktime(time.strptime(x['Timestamp'], '%d/%m/%Y %H:%M:%S')))
#print(mydict)
