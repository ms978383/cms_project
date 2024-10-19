from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer,UserDetailsSerializer
from .token_utils import *
from .models import *





def get_user_from_token(request):
    token = request.headers.get('Authorization', None)
    if not token:
        return Response({"success":False,"response":None,"errormsg": "authorization token required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        token = token.split(' ')[1]
    except IndexError:
        return Response({"success":False,"response":None,"errormsg": "token format is invalid"}, status=status.HTTP_400_BAD_REQUEST)

    payload = decode_token(token)
    
    if not payload:
        return Response({"success":False,"response":None,"errormsg": "token is invalid or expired"}, status=status.HTTP_401_UNAUTHORIZED)
    
    user_id = payload.get('user_id')

    if not user_id:
        return Response({"success":False,"response":None,"errormsg": "invalid token payload"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({"success":False,"response":None,"errormsg": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    return user