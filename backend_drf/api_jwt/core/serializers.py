from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ('uuid', 'name', 'email', 'password', 'password2')
        read_only_fields = ('uuid',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validate_data):
        return User.objects.create(
            email=validate_data['email'], name=validate_data['name'], password=validate_data['password']
        )

    def validate(self, data):
        password1 = data['password']
        password2 = data['password2']
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError(detail='The two password fields didn’t match.', code='password_mismatch')

        password_validation.validate_password(password1, self.instance)

        return data
