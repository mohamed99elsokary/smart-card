from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import serializers, models
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import secrets
import string
import send_mail
from django.shortcuts import render
from treatment import models as treatment_models
from diseases import models as diseases_models
from emergency_contacts import models as emergency_contacts_models

# Create your views here.
@api_view(["POST"])
def register(request):
    serializer = serializers.RegisterUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login(request):
    serializer = serializers.LoginUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data, status=status.HTTP_200_OK)


def web(request, id):
    user = get_object_or_404(User, id=id)
    profile = models.Profile.objects.get(user=user)
    treatments = treatment_models.Treatment.objects.filter(user=user)
    diseases = diseases_models.Disease.objects.filter(user=user)

    emergency_contacts = emergency_contacts_models.EmergencyContact.objects.filter(
        user=user
    )
    context = {
        "profile": profile,
        "treatments": treatments,
        "diseases": diseases,
        "emergency_contacts": emergency_contacts,
    }
    return render(request, "html.html", context)


@api_view(["GET", "PUT"])
def profile(request, id):
    profile = get_object_or_404(models.Profile, user_id=id)
    if request.method == "GET":
        serializer = serializers.ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        if request.data.get("name") not in [None, ""]:
            profile.name = request.data.get("name")
        if request.data.get("phone_number") not in [None, ""]:
            profile.phone_number = request.data.get("phone_number")
        if request.data.get("profile_image") not in [None, ""]:
            profile.profile_image = request.data.get("profile_image")
        if request.data.get("address") not in [None, ""]:
            profile.address = request.data.get("address")
        if request.data.get("blood_type") not in [None, ""]:
            profile.blood_type = request.data.get("blood_type")
        if request.data.get("is_addictive") not in [None, ""]:
            profile.is_addictive = request.data.get("is_addictive")
        if request.data.get("national_id") not in [None, ""]:
            profile.national_id = request.data.get("national_id")

        if request.data.get("facebook") not in [None, ""]:
            profile.facebook = request.data.get("facebook")

        if request.data.get("instagram") not in [None, ""]:
            profile.instagram = request.data.get("instagram")

        if request.data.get("whatsapp") not in [None, ""]:
            profile.whatsapp = request.data.get("whatsapp")

        profile.save()
        serializer = serializers.ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def change_password(request):
    username = request.data.get("username")
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
    if user := authenticate(username=username, password=old_password):
        user.set_password(new_password)
        user.save()

        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def forget(request):
    email = request.data.get("email")
    user = get_object_or_404(User, email=email)
    profile = get_object_or_404(models.Profile, user=user)
    code = "".join(
        secrets.choice(
            string.ascii_letters + string.digits + string.punctuation
        )
        for _ in range(8)
    )

    profile.forget_pass_code = code
    profile.save()
    message = code
    send_mail.send(email, message)

    return Response({"code": message}, status=status.HTTP_200_OK)


@api_view(["POST"])
def forget_confermation(request):
    code = request.data.get("code")
    new_password = request.data.get("new_password")
    user = User.objects.get(email=request.data.get("email"))
    profile = get_object_or_404(models.Profile, user=user)
    if code == profile.forget_pass_code:
        user.set_password(new_password)
        user.save()
        profile.forget_pass_code = None
        profile.save()

        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
