from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from apps.account.serializers import CustomUserDeatilSerializer
from apps.flowers.models import Flower
from apps.order.models import (
    TypeRecipient, OrderFlowers, StatusDeliver, PlacingOrder
)
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from django.db import transaction


class TypeRecipientSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=TypeRecipient)

    class Meta:
        model = TypeRecipient
        fields = ['id', 'translations']

    def get_text(self, instance):
        return {
            "en": instance.name_en,
            "ru": instance.name_ru,
        }


class StatusDeliverSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=StatusDeliver)

    class Meta:
        model = StatusDeliver
        fields = ['id', 'translations']

    def get_text(self, instance):
        return {
            "en": instance.name_en,
            "ru": instance.name_ru,
        }


class OrderFlowersSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderFlowers
        fields = ['id', 'flower', 'quantity']


class PlacingOrderCreateSerializer(serializers.ModelSerializer):
    order_flower = OrderFlowersSerializer(read_only=True, many=True)
    type_recipient = TypeRecipientSerializer(read_only=True)
    status_deliver = StatusDeliverSerializer(read_only=True)
    total = serializers.FloatField(read_only=True)
    cashback = serializers.FloatField(read_only=True)
    deliver_price = serializers.FloatField(read_only=True)
    is_promo_code = serializers.BooleanField(default=False)
    order_flower_data = serializers.JSONField()

    class Meta:
        model = PlacingOrder
        fields = [
            'id', 'recipient', 'status_deliver', 'author', 'full_name', 'adress', 'flat',
            'comment', 'is_call', 'total', 'cashback', 'deliver_price', 'is_promo_code',
            'comment2', 'created_at', 'order_flower', 'type_recipient', 'status_deliver',
            'order_flower_data'
        ]

    def create(self, validated_data):
        order_flower_data = validated_data.pop('order_flower_data', [])
        author = self.context.get('request').user
        order = PlacingOrder.objects.create(**validated_data, author=author)

        with transaction.atomic():
            for item in order_flower_data:
                flower = get_object_or_404(Flower, id=item['flower'])
                OrderFlowers.objects.create(
                    flower=flower,
                    quantity=item['quantity'],
                    order=order
                )
        return order
