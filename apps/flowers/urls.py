from django.urls import path
from apps.flowers.views import *

urlpatterns = [
    path('categories/', TopLevelCategoryListAPIView.as_view(), name='category-list'),
    path('flowers/', FlowerListCreateAPIView.as_view(), name='flower-list-create'),
    path('flowers/all/', FlowerListAPIView.as_view(), name='flower-list-public'),
    path('flowers/<int:pk>/', FlowerRetrieveUpdateAPIView.as_view(), name='flower-detail-update'),
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-create'),
    path('package-flowers/', PackageFlowerAPIView.as_view(), name='package-flowers'),
    path('country-flowers/', CountryFlowerAPIView.as_view(), name='country-flowers'),
    path('size-flowers/', SizesofFlowerAPIView.as_view(), name='size-flowers'),
    path('banner-carousel/', BannerCarouselAPIView.as_view(), name='banner-carousel'),
    path('like/', LiketoFlowerCreateAPIView.as_view(), name='like-flower'),
    path('like/<int:flower_id>/', LiketoFlowerDeleteAPIView.as_view(), name='unlike-flower'),
    path('flower-seen/', ViewUsertoFlowerListView.as_view(), name='flower-seer'),
    path('deploy-/', ViewUsertosFlowerListView.as_view(), name='flower-seer'),

    path('distinct-product-attributes/', DistinctProductAttributesView.as_view(),
         name='distinct-product-attributes'),

]
