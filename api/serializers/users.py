from rest_framework import serializers
from auctions.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "profile_picture",
            "pfp_credit",
            "banner",
            "banner_credit",
            "dark_mode"
        ]

    extra_kwargs = {
        'id': {'read_only': True},
        'username': {'read_only': True}
    }


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]

        extra_kwargs = {"password1": {"write_only": True}, "password2": {"write_only": True}}

    def create(self, validated_data):
        username = self.validated_data["username"]
        email = self.validated_data['email']
        password = self.validated_data["password1"]
        confirmation = self.validated_data["password2"]

        # Ensure password matches confirmation
        if password != confirmation:
            print("Here 1")
            raise serializers.ValidationError({"error": "Passwords must match."})

        try:
            validate_password(password)
        except ValidationError as err:
            raise serializers.ValidationError({"error": ' '.join(err.messages)})

        # Make new user and save to database
        user = User.objects.create_user(username, email, password)
        user.save()
        return user


# https://www.section.io/engineering-education/api-authentication-with-django-knox-and-postman-testing/
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError({"error": "Incorrect credentials"})