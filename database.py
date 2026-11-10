import pyrebase
import json
import hashlib


class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    def insert_item(self, name, data, img_path):
        item_info = {
            "seller_id": data["seller_id"],
            "price": int(data["price"]),
            "address": data["address"],
            "status": data["status"],
            "email": data["email"],
            "img_path": img_path
        }

        self.db.child("item").child(name).set(item_info)
        return True
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        if users.val() is None:
            return True
        for res in users.each():
            if res.val()['id'] == id_string:
                return False
        return True

    def insert_user(self, data, pw):
        if not self.user_duplicate_check(str(data['id'])):
            return False
        user_info = {
            "id": data['id'],
            "pw": hashlib.sha256(pw.encode('utf-8')).hexdigest(),
            "nickname": data['nickname']
        }
        self.db.child("user").push(user_info)
        return True

    def find_user(self, id_, pw_hash):
        users = self.db.child("user").get()
        if users.val() is None:
            return False
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_hash:
                return True
        return False

    def get_items(self):
        return self.db.child("item").get().val()

    def get_item_byname(self, name):
        return self.db.child("item").child(name).get().val()