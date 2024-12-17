from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from parler.models import TranslatableModel, TranslatedFields, TranslatableManager

user = settings.AUTH_USER_MODEL


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Название категория"), max_length=250, null=True, blank=True),
    )
    image = models.ImageField(upload_to='category_images/', null=True, blank=True, verbose_name="Изображение")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Родитель категории",
        related_name='subcategories'
    )
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = TranslatableManager()

    def __str__(self):
        return str(self.safe_translation_getter('name', any_language=True))


class TopLevelCategory(Category):
    objects = TranslatableManager()

    class Meta:
        proxy = True
        verbose_name = "1. Основная категория"
        verbose_name_plural = "1. Основная категория"


class PackageFlower(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Название упаковка"), max_length=250, null=True, blank=True)
    )

    objects = TranslatableManager()

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or 'Безымянный'

    class Meta:
        verbose_name = "2. Упаковка"
        verbose_name_plural = "2. Упаковка"


class CountryFlower(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Название страна"), max_length=250, null=True, blank=True)
    )
    image = models.ImageField(upload_to='country_images/', null=True, blank=True, verbose_name="Изображение")

    objects = TranslatableManager()

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or 'Безымянный'

    class Meta:
        verbose_name = "3. Страна"
        verbose_name_plural = "3. Страна"


class Flower(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Название цвета"), max_length=250, null=True, blank=True),
        description=models.TextField(null=True, blank=True, verbose_name="Краткое описание"),
        plantation=models.CharField(_("Плантация"), max_length=250, null=True, blank=True),
        sort=models.CharField(_("Cорт"), max_length=250, null=True, blank=True),
    )
    stem_height = models.IntegerField(default=0, null=True, blank=True, verbose_name='Высота стебля')
    volume = models.IntegerField(default=0, null=True, blank=True, verbose_name='Объём')
    plant_length = models.IntegerField(default=0, null=True, blank=True, verbose_name='Длина растения')
    price_per_box = models.IntegerField(default=0,  null=True, blank=True, verbose_name='Цена за коробку')
    head_outer_diameter = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2,
                                              verbose_name="Внешний диаметр головки (мм)")
    price = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2, verbose_name="Цена")
    discount_price = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2,
                                         verbose_name="Цена со скидкой")
    cashback = models.IntegerField(default=10, null=True, blank=True, verbose_name="Кешбак")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Категория")
    author = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Автор")
    package = models.ForeignKey(PackageFlower, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Упаковка")
    country = models.ForeignKey(CountryFlower, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Страна")
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name="Количество цветов")
    in_stock = models.BooleanField(default=True, null=True, blank=True, verbose_name="В наличи или нет")
    showcase_online = models.BooleanField(default=False, null=True, blank=True, verbose_name='Витрина Онлайн')
    is_popular = models.BooleanField(default=False, null=True, blank=True, verbose_name='Популярное')
    is_new = models.BooleanField(default=False, null=True, blank=True, verbose_name='Новинки')
    stock_number = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Процент акции")

    objects = TranslatableManager()

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or 'Безымянный'

    class Meta:
        verbose_name = "4. Цветы"
        verbose_name_plural = "4. Цветы"


class SizesofFlower(models.Model):
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Выбрать цветок",
                               related_name='flower_size')
    name = models.CharField(_("Название размер букета"), max_length=250, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class QuantityofFlower(models.Model):
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Выбрать цветок",
                               related_name='flower_quantity')
    name = models.CharField(_("Количество букета"), max_length=250, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class CompoundyofFlower(models.Model):
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Выбрать цветок",
                               related_name='flower_compound')
    name = models.CharField(_("Состав букета"), max_length=250, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class ImagesofFlower(models.Model):
    image = models.ImageField(upload_to='flower_images/', null=True, blank=True, verbose_name="Изображение")
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Выбрать цветок",
                               related_name='images')

    objects = models.Manager()

    def __str__(self):
        return self.flower.name


class Review(models.Model):
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Выбрать цветок",
                               related_name='flower_review')
    full_name = models.CharField(_("ФИО"), max_length=250, null=True, blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рейтинг"
    )
    content = models.TextField(verbose_name="Отзыв", null=True, blank=True)
    image = models.ImageField(upload_to='flower_images/', null=True, blank=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")

    objects = models.Manager()

    def __str__(self):
        return f"Отзыв от {self.full_name} на {self.flower.name}"

    class Meta:
        verbose_name = _("5. Отзыв")
        verbose_name_plural = _("5. Отзывы")


class BannerCarousel(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_("Название баннера"), max_length=250, null=True, blank=True),
        text=models.TextField(null=True, blank=True, verbose_name="Краткое описание"),
    )
    image = models.ImageField(upload_to='banner/', null=False, blank=False, verbose_name="Изображение")

    objects = TranslatableManager()

    class Meta:
        ordering = ["id"]
        verbose_name = _("5. Карусели баннеров")
        verbose_name_plural = _("5. Карусели баннеров")


class LiketoFlower(models.Model):
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Выбрать цветок",
                               related_name='flower_like')
    author = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Автор")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = models.Manager()

    class Meta:
        ordering = ["id"]
        verbose_name = _("Лайк за цветы ")
        verbose_name_plural = _("Лайк за цветы")


class ViewUsertoFlower(models.Model):
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Выбрать цветок",
                               related_name='flower_views')
    author = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Автор")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = models.Manager()

    class Meta:
        ordering = ["id"]
        verbose_name = _("Увиденные цветы ")
        verbose_name_plural = _("Увиденные цветы")


class Balloon(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Название цвета"), max_length=250, null=True, blank=True),
        description=models.TextField(null=True, blank=True, verbose_name="Краткое описание"),
    )
    price = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2, verbose_name="Цена")
    discount_price = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2,
                                         verbose_name="Цена со скидкой")
    cashback = models.IntegerField(default=10, null=True, blank=True, verbose_name="Кешбак")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Категория")
    author = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Автор")
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name="Количество цветов")
    in_stock = models.BooleanField(default=True, null=True, blank=True, verbose_name="В наличи или нет")
    showcase_online = models.BooleanField(default=False, null=True, blank=True, verbose_name='Витрина Онлайн')
    is_popular = models.BooleanField(default=False, null=True, blank=True, verbose_name='Популярное')
    is_new = models.BooleanField(default=False, null=True, blank=True, verbose_name='Новинки')
    stock_number = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                       verbose_name="Процент акции")

    objects = TranslatableManager()

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or 'Безымянный'

    class Meta:
        verbose_name = "6. Воздушные шары"
        verbose_name_plural = "6. Воздушные шары"


class ImagesofBalloon(models.Model):
    image = models.ImageField(upload_to='balloon_images/', null=True, blank=True, verbose_name="Изображение")
    balloon = models.ForeignKey(Balloon, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Выбрать",
                               related_name='images_balloon')

    objects = models.Manager()

    def __str__(self):
        return self.balloon.name


class LiketoBalloon(models.Model):
    balloon = models.ForeignKey(Balloon, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Выбрать",
                               related_name='balloon_like')
    author = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Автор")
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = models.Manager()

    class Meta:
        ordering = ["id"]
        verbose_name = _("Лайк за воздушный шар ")
        verbose_name_plural = _("Лайк за воздушный шар")
