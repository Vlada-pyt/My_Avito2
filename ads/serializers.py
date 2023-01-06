from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from ads.models import Location, Ads, Categories, Users, Selection


class UserCreateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(required=False, many=True, slug_field='name',
                                            queryset=Location.objects.all())

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop('location', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        new_user = Users.objects.create(**validated_data)
        for loc in self._location:
            location, _ = Location.objects.get_or_create(name=loc)
            new_user.locations.add(location)
        return new_user

    class Meta:
        model = Users
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(required=False, many=True, slug_field='name',
                                            queryset=Location.objects.all())

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop('location', [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        for loc in self._location:
            location, _ = Location.objects.get_or_create(name=loc)
            user.locations.add(location)
        return user

    class Meta:
        model = Users
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Location.objects.all())

    class Meta:
        model = Users
        exclude = ['password']
        # fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Location.objects.all())
    total_ads = serializers.IntegerField()

    class Meta:
        model = Users
        exclude = ['password']


class LocationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ads
        fields = '__all__'


class AdsDetailSerializer(serializers.ModelSerializer):
    author_id = SlugRelatedField(slug_field='username', queryset=Users.objects.all())
    category = SlugRelatedField(slug_field='name', queryset=Categories.objects.all())

    class Meta:
        model = Ads
        fields = '__all__'


class AdsListSerializer(serializers.ModelSerializer):
    author_id = SlugRelatedField(slug_field='username', queryset=Users.objects.all())
    category = SlugRelatedField(slug_field='name', queryset=Categories.objects.all())
    location = serializers.SerializerMethodField()

    def get_location(self, ads):
        return [loc.name for loc in ads.author_id.location.all()]

    class Meta:
        model = Ads
        fields = '__all__'


# class SelectionCreateSerializer(serializers.ModelSerializer):
#     ads = serializers.SlugRelatedField(required=False, many=True,
#                                             slug_field='name',
#                                             queryset=Ads.objects.all())
#     items = AdsSerializer(many=True)
#
#     def is_valid(self, *, raise_exception=False):
#         self.ads = self.initial_data.pop('ads', [])
#         return super().is_valid(raise_exception=raise_exception)
#
#     def create(self, validated_data):
#         new_selection = Selection.objects.create(**validated_data)
#         for ad in self.ads:
#             ad, _ = Ads.objects.get_or_create(name=ad)
#             new_selection.ads.add(ad)
#         return new_selection
#
#     class Meta:
#         model = Selection
#         fields = '__all__'


# class SelectionUpdateSerializer(serializers.ModelSerializer):
#     ads = serializers.SlugRelatedField(required=False, many=True,
#                                        slug_field='name',
#                                        queryset=Ads.objects.all())
#
#     def is_valid(self, *, raise_exception=False):
#         self.ads = self.initial_data.pop('ads', [])
#         return super().is_valid(raise_exception=raise_exception)
#     def save(self, **kwargs):
#         selection = super().save(**kwargs)
#         for ad in self._ads:
#             ad, _ = Ads.objects.get_or_create(name=ad)
#             selection.ads.add(ad)
#         return selection

    # class Meta:
    #     model = Selection
    #     fields = '__all__'


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