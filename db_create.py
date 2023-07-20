from app import db
from app.models.token_auth import TokenAuth
import sys 

print('Drop all')
db.drop_all()

print('Create all')
db.create_all()

print("Token time")
token_type = "Bearer"

if (len(sys.argv) > 1):
    token_token = sys.argv[1]
else:
    token_token = input("Enter token: ")
token = TokenAuth(token_type, token_token)
token.save()

print('Done')
