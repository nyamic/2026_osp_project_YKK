from database import DBhandler

message = {"message": "hello firebase"}

db = DBhandler().db

db.child("test").set(message)
result = db.child("test").get().val()
print(result)

assert dict(result) == message
print("Firebase 읽기/쓰기 테스트 성공")
