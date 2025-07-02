from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .utils import encrypt_id,decrypt_id
from .serializers import FileUploadSerializer,ClientSignupSerializer
from .models import FileUpload,UserProfile
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404


class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if not request.user.is_staff:
            return Response({"error": "Only Ops Users can upload files."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClientSignupView(APIView):
    def post(self, request):
        serializer = ClientSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            encrypted_id = encrypt_id(user.id)
            download_url = f"http://127.0.0.1:8000/api/download/{encrypted_id}/"
            return Response({
                "message": "Signup successful",
                "download-link": download_url
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SecureDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token):
        try:
            user_id = decrypt_id(token)
            if request.user.id != user_id or request.user.is_staff:
                return Response({"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

            # Return files uploaded by Ops for client to view/download
            files = FileUpload.objects.all()
            serializer = FileUploadSerializer(files, many=True)
            return Response({
                "message": "success",
                "files": serializer.data
            })

        except Exception as e:
            return Response({"error": "Invalid or expired link"}, status=status.HTTP_400_BAD_REQUEST)
        

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username
        })
    
class SendVerificationEmailView(APIView):
    def get(self, request):
        user = request.user
        encrypted_id = encrypt_id(user.id)
        verify_link = f"http://127.0.0.1:8000/api/verify-email/{encrypted_id}/"
        send_mail(
            'Verify your email',
            f'Click here to verify: {verify_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response({"message": "Verification email sent (console)."}, status=200)

class VerifyEmailView(APIView):
    def get(self, request, token,format=None):
        try:
            user_id = decrypt_id(token)
            profile = get_object_or_404(UserProfile, user_id=user_id)
            profile.is_verified = True
            profile.save()
            return Response({"message": "Email verified successfully."})
        except Exception:
            return Response({"error": "Invalid or expired token"}, status=400)
        
class SingleFileDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token, file_id):
        try:
            user_id = decrypt_id(token)
            if request.user.id != user_id or request.user.is_staff:
                return Response({"error": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

            file = get_object_or_404(FileUpload, id=file_id)
            return Response({
                "file": file.file.url,
                "uploaded_at": file.uploaded_at
            })
        except Exception:
            return Response({"error": "Invalid token or file"}, status=400)