from rest_framework import serializers
from occurrences.models import Occurrence


class OccurrenceSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = serializers.CharField(source='category.type')

    class Meta:
        model = Occurrence
        fields = ('url', 'id', 'author', 'geo_location', 'description',
                  'created', 'updated', 'status', 'category')

    # def get_owner(self, obj):
    #     return obj.owner.username

    def create(self, validated_data):
        return Occurrence.objects.create(**validated_data)


from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model

UserModel = get_user_model()


class CreateAuthorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = ('url', 'id', 'username', 'password')


class AuthorSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='username')
    occurrences = serializers.PrimaryKeyRelatedField(many=True, queryset=Occurrence.objects.all())

    class Meta:
        model = UserModel
        fields = ('url', 'id', 'author', 'occurrences')

    def get_author(self, obj):
        return obj.author.username

