from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .serializers import UserLoginSerializer, UserSignUpSerializer
from .utils import api_response, get_status_message


class UserLoginAPIView(APIView):
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                return self._extracted_from_post_(serializer)
            return Response(
                api_response(status_code=400, data=serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                api_response(status_code=500, data=str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


    def _extracted_from_post_(self, serializer):
        validated_data = serializer.validated_data
        if not isinstance(validated_data, dict):
            return Response(
                api_response(
                    status_code=400,
                    data={"error": "Invalid data format."},
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = validated_data.get("user")
        if user is None:
            # User authentication failed
            return Response(
                api_response(
                    status_code=400,
                    data={"error": "Invalid username or password."},
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        access = AccessToken.for_user(user)
        print(
            "Access token:", access
        )
        return (
            Response(
                api_response(
                    status_code=200,
                    data={
                        "access": str(access),
                        "expires_in": access.payload.get("exp"),
                    },
                ),
                status=status.HTTP_200_OK,
            )
            if access
            else Response(
                api_response(
                    status_code=400,
                    data={"error": "Failed to generate access token."},
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        )


class UserSignUpAPIView(APIView):
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
