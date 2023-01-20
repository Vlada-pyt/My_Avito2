from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from ads.models import Location, Ads, Categories, Users, Selection
from ads.validators import not_null, check_email, check_birth_date


class UserCreateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(required=False, many=True, slug_field='name',
                                            queryset=Location.objects.all())
    email = serializers.EmailField(required=True, validators=[check_email])
    birth_date = serializers.DateField(validators=[check_birth_date], required=True)

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop('locations', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        new_user = Users.objects.create(**validated_data)
        for loc in self._locations:
            locations, _ = Location.objects.get_or_create(name=loc)
            new_user.locations.add(locations)
        return new_user

    class Meta:
        model = Users
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(required=False, many=True, slug_field='name',
                                            queryset=Location.objects.all())

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop('locations', [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        for loc in self._locations:
            locations, _ = Location.objects.get_or_create(name=loc)
            user.locations.add(locations)
        return user

    class Meta:
        model = Users
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Location.objects.all())

    class Meta:
        model = Users
        exclude = ['password']
        # fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Location.objects.all())
    total_ads = serializers.IntegerField()

    class Meta:
        model = Users
        exclude = ['password']


class LocationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AdsSerializer(serializers.ModelSerializer):
    is_published = serializers.BooleanField(validators=[not_null])
    class Meta:
        model = Ads
        fields = '__all__'


class AdsDetailSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', queryset=Users.objects.all())
    category = SlugRelatedField(slug_field='name', queryset=Categories.objects.all())

    class Meta:
        model = Ads
        fields = '__all__'


class AdsListSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', queryset=Users.objects.all())
    category = SlugRelatedField(slug_field='name', queryset=Categories.objects.all())
    locations = serializers.SerializerMethodField()

    def get_locations(self, ads):
         return [loc.name for loc in ads.author.locations.all()]

    class Meta:
        model = Ads
        fields = '__all__'

class SelectionDetailSerializer(serializers.ModelSerializer):
    # ads = serializers.SlugRelatedField(required=False, many=True,
    #                                    slug_field='name',
    #                                    queryset=Ads.objects.all())
    user = SlugRelatedField(slug_field='username', queryset=Users.objects.all())
    items = AdsListSerializer(many=True)
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionListSerializer(serializers.ModelSerializer):
    # ads = serializers.SlugRelatedField(required=False, many=True,
    #                                    slug_field='name',
    #                                    queryset=Ads.objects.all())

    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = '__all__'