from django.contrib import admin
from parler.admin import TranslatableAdmin
from apps.flowers.models import (
    SizesofFlower, ImagesofFlower, QuantityofFlower,
    Flower, TopLevelCategory, Category, Review, CompoundyofFlower, PackageFlower,
    CountryFlower, LiketoFlower, ViewUsertoFlower, Balloon, ImagesofBalloon, LiketoBalloon,
    BannerCarousel
)


class SizesofFlowerInline(admin.TabularInline):
    model = SizesofFlower
    extra = 1
    verbose_name = "Размер букета"
    verbose_name_plural = "Размеры букета"


class QuantityofFlowerInline(admin.TabularInline):
    model = QuantityofFlower
    extra = 1
    verbose_name = "Количество букета"
    verbose_name_plural = "Количество букета"


class CompoundyofFlowerInline(admin.TabularInline):
    model = CompoundyofFlower
    extra = 1
    verbose_name = "Состав букета"
    verbose_name_plural = "Составы букета"


class ImagesofFlowerInline(admin.TabularInline):
    model = ImagesofFlower
    extra = 1
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения"


class LiketoFlowerInline(admin.TabularInline):
    model = LiketoFlower
    extra = 1


class LiketoBalloonInline(admin.TabularInline):
    model = LiketoBalloon
    extra = 1


class ViewUsertoFlowerInline(admin.TabularInline):
    model = ViewUsertoFlower
    extra = 1


class BalloonImageInline(admin.TabularInline):
    model = ImagesofBalloon
    extra = 1


@admin.register(Balloon)
class BalloonAdmin(TranslatableAdmin):
    list_display = ('name', 'price', 'discount_price', 'in_stock', 'category', 'author')
    list_filter = ('in_stock', 'category', 'author')
    search_fields = ('name', 'category__name', 'author__phone')
    inlines = [BalloonImageInline, LiketoBalloonInline]


@admin.register(Flower)
class FlowerAdmin(TranslatableAdmin):
    list_display = ('name', 'price', 'discount_price', 'in_stock', 'category', 'author')
    list_filter = ('in_stock', 'category', 'author')
    search_fields = ('name', 'category__name', 'author__phone')
    inlines = [SizesofFlowerInline, QuantityofFlowerInline,
               CompoundyofFlowerInline, ImagesofFlowerInline,
               LiketoFlowerInline, ViewUsertoFlowerInline]


@admin.register(TopLevelCategory)
class TopLevelCategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'created_at', 'id')
    search_fields = ('translations__name',)
    list_filter = ('created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(parent__isnull=True)

    def name(self, obj):
        return obj.safe_translation_getter('name', any_language=True) or 'Безымянный'

    name.short_description = 'Название категория'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is None or obj.parent is None:
            form.base_fields.pop('parent', None)
        return form


@admin.register(PackageFlower)
class PackageAdmin(TranslatableAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CountryFlower)
class CountryFlowerAdmin(TranslatableAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('flower', 'full_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('flower__name', 'full_name', 'content')


@admin.register(BannerCarousel)
class BannerCarouselAdmin(TranslatableAdmin):
    list_display = ['title']
    fields = ['title', 'text', 'image']

