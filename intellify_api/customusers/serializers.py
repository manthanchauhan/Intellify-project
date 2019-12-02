from rest_framework import serializers
from customusers.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ['created_on']

        # passwords are stored in Hashed format and are meaningless to human eye.
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.save(new_password=True)
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.user_name = validated_data.get('user_name', instance.user_name)

        if 'password' in validated_data.keys():
            instance.password = validated_data['password']
            instance.save(new_password=True)
        else:
            instance.save()
        return instance
