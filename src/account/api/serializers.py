from rest_framework import serializers

from account.models import Account


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['phone', 'username', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def save(self):
        account = Account(
            phone=self.validated_data['phone'],
            username=self.validated_data['username']
        )

        password = self.validated_data['password']

        account.set_password(password)
        account.save()

        return account
