from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager

from apps.flowers.models import Flower

user = settings.AUTH_USER_MODEL


class TypeRecipient(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_("Тип Получатель"), max_length=250, null=True, blank=True),
    )

    objects = TranslatableManager()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("2. Тип получателя")
        verbose_name_plural = _("2. Тип получателя")


class StatusDeliver(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_("Статус Доставить"), max_length=250, null=True, blank=True),
    )

    objects = TranslatableManager()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _("3. Статус Доставить")
        verbose_name_plural = _("3. Статус Доставить")


class PlacingOrder(models.Model):
    recipient = models.ForeignKey(TypeRecipient, on_delete=models.CASCADE, null=True, blank=True,
                                  verbose_name='Тип получателя')
    status_deliver = models.ForeignKey(StatusDeliver, on_delete=models.CASCADE, null=True, blank=True,
                                  verbose_name='Когда доставляем?')
    author = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Автор")
    full_name = models.CharField(_("ФИО"), max_length=250, null=True, blank=True)
    adress = models.CharField(_("Город"), max_length=250, null=True, blank=True)
    flat = models.CharField(_("Квартира/офис, подъезд, этаж"), max_length=250, null=True, blank=True)
    comment = models.TextField(_("Ваш комментарий"), max_length=250, null=True, blank=True)
    is_call = models.BooleanField(default=False, null=True, blank=True, verbose_name='Позвонить перед выездом курьера')
    total = models.FloatField(null=True, blank=True, default=0, verbose_name="ИТОГО к оплате")
    cashback = models.FloatField(null=True, blank=True, default=0, verbose_name="Ваш кешбэк 10%")
    deliver_price = models.FloatField(null=True, blank=True, default=0, verbose_name="Доставка")
    is_promo_code = models.BooleanField(default=False, null=True, blank=True, verbose_name='Применить кешбэк или нет')
    comment2 = models.TextField(_("Комментарий к заказу / текст записки"), max_length=250, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = models.Manager()

    def __str__(self):
        return f'{self.author}'

    class Meta:
        verbose_name = _("1. Заказанная продукция")
        verbose_name_plural = _("1. Заказанная продукция")


class OrderFlowers(models.Model):
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Выбрать цветок",
                               related_name='flower_order')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Количество')
    order = models.ForeignKey(PlacingOrder, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name="Выбрать цветок", related_name='flower_order')
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = models.Manager()
