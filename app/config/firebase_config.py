import firebase_admin
from firebase_admin import credentials, initialize_app

auth_cred = credentials.Certificate("authServiceAccount.json")
auth_app = initialize_app(auth_cred, name="authorizationServiceAccount")
