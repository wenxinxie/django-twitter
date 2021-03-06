from django.contrib.auth.models import User, Group
from rest_framework import serializers, exceptions

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data['username'].lower()
        if not User.objects.filter(username=username).exists():
            raise exceptions.ValidationError({
                'username': "User does not exist."
            })
        data['username'] = username
        return data

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, min_length = 6)
    password = serializers.CharField(max_length=20, min_length = 6)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


    def validate(self, data):
        if User.objects.filter(username= data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'This username has been occupied.'
            })
        if User.objects.filter(email= data['email'].lower()).exists():
            raise exceptions.ValidationError({
                'message': 'This email address has been occupied.'
            })
        return data

    def create(self, validated_data):
        username = validated_data['username'].lower()
        email = validated_data['email'].lower()
        password = validated_data['password']

        user = User.objects.create_user(
            username = username,
            email = email,
            password = password,
        )
        return user







