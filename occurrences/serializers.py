from django.contrib.auth import get_user_model  # If used custom user model
from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from occurrences.models import Occurrence, Category, Pizza

UserModel = get_user_model()


class OccurrenceSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = serializers.SlugRelatedField(
        read_only=False,
        queryset=Category.objects.all(),
        slug_field='type'
    )
    geo_location = PointField()

    class Meta:
        model = Occurrence
        fields = ('url', 'id', 'author', 'geo_location', 'description',
                  'created', 'updated', 'status', 'category')

    def create(self, validated_data):
        return Occurrence.objects.create(**validated_data)


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


class PizzaListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        # Perform creations and updates.
        ret = []

        for data in validated_data:
            if "id" in data and data['id'] not in ['', None]:
                Pizza.objects.filter(id=data['id']).update(**data)
                ret.append(data)
            else:
                ret.append(Pizza.objects.create(**data))
        return ret


class PizzaDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ('id', 'name', 'description', 'price')

        list_serializer_class = PizzaListSerializer
        extra_kwargs = {
            # We need to identify elements in the list using their primary key,
            # so use a writable field here, rather than the default which would be read-only.
            'id': {
                'read_only': False,
                'allow_null': True,
            },
            'name': {
                'required': True,
            },
            'description': {
                'required': True,
            },
            'price': {
                'required': False,
            }
        }

