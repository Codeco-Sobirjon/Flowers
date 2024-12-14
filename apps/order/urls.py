from django.urls import path

from apps.order.views import TypeRecipientListAPIView, StatusDeliverListAPIView, PlacingOrderCreateAPIView, \
    StatisticsFlower, StatisticsByMonths

urlpatterns = [
    path('type-recipients/', TypeRecipientListAPIView.as_view(), name='type-recipients-list'),
    path('status-delivers/', StatusDeliverListAPIView.as_view(), name='status-delivers-list'),
    path('place-order/', PlacingOrderCreateAPIView.as_view(), name='place_order'),
    path('statistics_flowers/', StatisticsFlower.as_view(), name='statistics_flowers'),
    path('statistics_flowers_by_months/', StatisticsByMonths.as_view(), name='statistics_flowers_by_months'),


]
