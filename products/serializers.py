from rest_framework import serializers
from .models import CustomUser, Product

# CustomUser Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is not exposed in read operations
        }

    def create(self, validated_data):
        # Use the set_password method to properly hash the password
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # Proper password hashing
        user.save()
        return user

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
