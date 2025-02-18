import secrets 
 # Generating a secret key 
secret_key = secrets.token_urlsafe(16)
print(secret_key)