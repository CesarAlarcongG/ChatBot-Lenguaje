from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import classify_intent, get_response

class ChatbotAPIView(APIView):
    def post(self, request):
        user_message = request.data.get("message", "")
        if not user_message:
            return Response({"error": "No message provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        intent = classify_intent(user_message)
        response_text = get_response(intent)
        return Response({"intent": intent, "response": response_text})

