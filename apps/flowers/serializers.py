
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from apps.account.serializers import CustomUserDeatilSerializer
from apps.flowers.models import (
    SizesofFlower, ImagesofFlower, QuantityofFlower,
    Flower, TopLevelCategory, Category, Review, CompoundyofFlower, PackageFlower, CountryFlower,
    BannerCarousel, LiketoFlower, ViewUsertoFlower, Balloon, ImagesofBalloon
)
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField


class TopLevelCategoryWithSubCategoriesSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=TopLevelCategory)

    class Meta:
        model = TopLevelCategory
        fields = ['id', 'translations', 'image']

    def get_text(self, instance):
        return {
            "en": instance.name_en,
            "ru": instance.name_ru,
        }


class ReviewSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Review
        fields = ['id', 'full_name', 'rating', 'content', 'image', 'created_at']

    def create(self, validated_data):
        review = Review.objects.create(
            **validated_data, image=validated_data.get('image', None)
        )
        return review


class ReviewListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'full_name', 'rating', 'content', 'image', 'created_at']


class LiketoFlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiketoFlower
        fields = ['id', 'flower']

    def create(self, validated_data):
        user = self.context.get('request').user
        flower = validated_data.get('flower')

        if LiketoFlower.objects.filter(flower=flower, author=user).exists():
            raise serializers.ValidationError({'error': "You have already liked this flower"})

        like_create = LiketoFlower.objects.create(
            **validated_data, author=user
        )
        return like_create


class PackageFlowerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=PackageFlower)

    class Meta:
        model = PackageFlower
        fields = ['id', 'translations']

    def get_text(self, instance):
        return {
            "en": instance.name_en,
            "ru": instance.name_ru,
        }


class BannerCarouselSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=BannerCarousel)

    class Meta:
        model = BannerCarousel
        fields = ['id', 'translations', 'image']

    def get_text(self, instance):
        return {
            "en": instance.name_en,
            "ru": instance.name_ru,
        }


class CountryFlowerSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=CountryFlower)

    class Meta:
        model = CountryFlower
        fields = ['id', 'translations', 'image']

    def get_text(self, instance):
        return {
            "en": instance.name_en,
            "ru": instance.name_ru,
        }


class SizesofFlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizesofFlower
        fields = ['id', 'name']


class QuantityofFlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuantityofFlower
        fields = ['id', 'name']


class CompoundyofFlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryFlower
        fields = ['id', 'name']


class ImagesofFlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagesofFlower
        fields = ['id', 'image']


class FlowerListSerializer(serializers.ModelSerializer):
    images = ImagesofFlowerSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    size = SizesofFlowerSerializer(many=True, read_only=True)
    quantity_of_flower = QuantityofFlowerSerializer(many=True, read_only=True)
    compound = CompoundyofFlowerSerializer(many=True, read_only=True)
    country = CountryFlowerSerializer(read_only=True)

    class Meta:
        model = Flower
        fields = [
            'id', 'name', 'plantation', 'sort', 'plant_length', 'price_per_box',
            'head_outer_diameter', 'price', 'discount_price', 'cashback', 'description',
            'images', 'uploaded_images', 'size', 'category', 'author', 'in_stock',
            'package', 'quantity', 'quantity_of_flower', 'compound',
            'is_popular', 'showcase_online', 'stock_number', 'is_new',
            'country', 'uploaded_images', 'volume', 'stem_height'
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        user = self.context.get('request').user
        flower = Flower.objects.create(
            **validated_data, author=user
        )
        for image in uploaded_images:
            ImagesofFlower.objects.create(image=image, flower=flower)

        return flower

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class FlowerDetailSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Flower)
    images = ImagesofFlowerSerializer(many=True, read_only=True)
    size = serializers.SerializerMethodField()
    quantity_of_flower = serializers.SerializerMethodField()
    compound = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()
    country = CountryFlowerSerializer(read_only=True)
    author = CustomUserDeatilSerializer(read_only=True)
    like = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Flower
        fields = [
            'id', 'translations', 'plant_length', 'price_per_box',
            'head_outer_diameter', 'price', 'discount_price', 'cashback',
            'images', 'size', 'category', 'author', 'in_stock',
            'package', 'quantity', 'quantity_of_flower', 'compound', 'average_rating',
            'review', 'is_popular', 'showcase_online', 'stock_number', 'is_new',
            'country', 'volume', 'stem_height', 'like', 'review_count'
        ]

    def get_average_rating(self, obj):
        reviews = obj.flower_review.all()
        if reviews.exists():
            return reviews.aggregate(Avg('rating'))['rating__avg']
        return None

    def get_size(self, obj):
        queryset = SizesofFlower.objects.select_related('flower').filter(
            flower=obj.id
        )
        serializer = SizesofFlowerSerializer(queryset, many=True, context={"request": self.context.get('request')})
        return serializer.data

    def get_quantity_of_flower(self, obj):
        queryset = QuantityofFlower.objects.select_related('flower').filter(
            flower=obj.id
        )
        serializer = QuantityofFlowerSerializer(queryset, many=True, context={"request": self.context.get('request')})
        return serializer.data

    def get_compound(self, obj):
        queryset = CompoundyofFlower.objects.select_related('flower').filter(
            flower=obj.id
        )
        serializer = CompoundyofFlowerSerializer(queryset, many=True, context={"request": self.context.get('request')})
        return serializer.data

    def get_review(self, obj):
        queryset = Review.objects.select_related('flower').filter(
            flower=obj.id
        )
        serializer = ReviewListSerializer(queryset, many=True, context={"request": self.context.get('request')})
        return serializer.data

    def get_like(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return LiketoFlower.objects.filter(flower=obj.id, author=user).exists()
        return False

    def get_review_count(self, obj):
        queryset = Review.objects.select_related('flower').filter(
            flower=obj.id
        )
        return queryset.count()


class ViewUsertoFlowerSerializer(serializers.ModelSerializer):
    flower = FlowerDetailSerializer(read_only=True, many=True)

    class Meta:
        model = ViewUsertoFlower
        fields = ['id', 'flower']


class ImagesofBalloonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagesofFlower
        fields = ['id', 'image']


class BalloonSerializer(TranslatableModelSerializer):
    images_balloon = ImagesofBalloonSerializer(read_only=True, many=True)
    translations = TranslatedFieldsField(shared_model=Balloon)

    class Meta:
        model = Balloon
        fields = ['id', 'translations', 'images_balloon', 'price', 'discount_price',
                  'category', 'author', 'in_stock', 'quantity', 'showcase_online',
                  'is_popular', 'is_new', 'stock_number']

    def get_text(self, instance):
        return {
            "en": instance.name_en,
            "ru": instance.name_ru,
        }
