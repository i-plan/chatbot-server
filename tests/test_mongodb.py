from pymongo import MongoClient

client = MongoClient(
    "mongodb://mongo:p5b67avO9383spNYAXYt@containers-us-west-32.railway.app:5746")

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
# db = client.test
db = client.chatai
cs = db.list_collection_names()
print(cs)
if 'chat_users' not in cs:
    db.create_collection('chat_users')
if 'chat_users_ban' not in cs:
    db.create_collection('chat_users_ban')
if 'chat_msgs' not in cs:
    db.create_collection('chat_msgs')
if 'chat_msgs_ban' not in cs:
    db.create_collection('chat_msgs_ban')

# db.chat_users.insert_one({'openid': "菜鸟教程", 'userInfo': {}})
# db.mycol2.insert({"name": "菜鸟教程"})
