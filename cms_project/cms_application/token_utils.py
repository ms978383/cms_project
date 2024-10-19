import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_token(user):
    
    payload = {
        'user_id': user.user_id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=24), 
        'iat': datetime.utcnow(),  
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
