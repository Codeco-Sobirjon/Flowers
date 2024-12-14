from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from django.db.models.functions import TruncMonth
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from apps.order.serializers import (
    TypeRecipientSerializer, StatusDeliverSerializer, PlacingOrderCreateSerializer
)
from apps.order.models import (
    TypeRecipient, OrderFlowers, StatusDeliver, PlacingOrder
)


class TypeRecipientListAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Type recipients'],
        operation_description="Retrieve a list of type recipients",
        responses={200: TypeRecipientSerializer(many=True)}
    )
    def get(self, request):
        type_recipients = TypeRecipient.objects.all()
        serializer = TypeRecipientSerializer(type_recipients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StatusDeliverListAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Delivery statuses'],
        operation_description="Retrieve a list of delivery statuses",
        responses={200: StatusDeliverSerializer(many=True)}
    )
    def get(self, request):
        status_delivers = StatusDeliver.objects.all()
        serializer = StatusDeliverSerializer(status_delivers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlacingOrderCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new placing order",
        request_body=PlacingOrderCreateSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Order successfully created",
                schema=PlacingOrderCreateSerializer
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid data provided"
            ),
        },
        tags=['Placing Order']
    )
    def post(self, request, *args, **kwargs):
        serializer = PlacingOrderCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            order = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatisticsFlower(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List Flower Statistics with Token",
        operation_description="Retrieve flower statistics with details based on different time periods using a token.",
        tags=["Flower Statistics"],
        manual_parameters=[
            openapi.Parameter('day', openapi.IN_QUERY, description="Get statistics by day (true/false)",
                              type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('month', openapi.IN_QUERY, description="Get statistics by month (true/false)",
                              type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('six_month', openapi.IN_QUERY, description="Get statistics by six_month (true/false)",
                              type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('year', openapi.IN_QUERY, description="Get statistics by year (true/false)",
                              type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('flower_id', openapi.IN_QUERY, description="Filter by flower ID (optional)",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={200: 'Statistics data for flowers'}
    )
    def get(self, request, *args, **kwargs):
        flower_id = request.query_params.get('flower_id', None)
        time_periods = {
            'day': request.query_params.get('day', 'false').lower() == 'true',
            'month': request.query_params.get('month', 'false').lower() == 'true',
            'six_month': request.query_params.get('six_month', 'false').lower() == 'true',
            'year': request.query_params.get('year', 'false').lower() == 'true',
        }

        today = timezone.now().date()

        response_data = {}
        if time_periods['day']:
            response_data['day'] = self.get_day_statistics(today, flower_id)
        if time_periods['month']:
            response_data['month'] = self.get_month_statistics(today, flower_id)
        if time_periods['six_month']:
            response_data['six_month'] = self.get_six_month_statistics(today, flower_id)
        if time_periods['year']:
            response_data['year'] = self.get_year_statistics(today, flower_id)

        return Response(response_data)

    def get_flower_data(self, orders):
        return [{
            'flower': order.flower.name,
            'quantity': order.quantity,
            'price': order.flower.price * order.quantity,
            'date': order.created_at,
        } for order in orders]

    def get_day_statistics(self, today, flower_id=None):
        orders_today = OrderFlowers.objects.filter(created_at=today)
        if flower_id:
            orders_today = orders_today.filter(flower_id=flower_id)
        return self.get_flower_data(orders_today)

    def get_six_month_statistics(self, today, flower_id=None):
        six_months_ago = today - timedelta(days=180)
        orders_last_six_months = OrderFlowers.objects.filter(created_at__gte=six_months_ago)
        if flower_id:
            orders_last_six_months = orders_last_six_months.filter(flower_id=flower_id)
        return self.get_grouped_statistics(orders_last_six_months)

    def get_year_statistics(self, today, flower_id=None):
        orders_this_year = OrderFlowers.objects.filter(created_at__year=today.year)
        if flower_id:
            orders_this_year = orders_this_year.filter(flower_id=flower_id)
        return self.get_grouped_statistics(orders_this_year)

    def get_grouped_statistics(self, orders):
        grouped_orders = {}
        for order in orders:
            month_name = order.created_at.strftime('%B')
            if month_name not in grouped_orders:
                grouped_orders[month_name] = []
            grouped_orders[month_name].append(order)

        month_order = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }

        sorted_months = sorted(grouped_orders.keys(), key=lambda month: month_order[month])

        return [{
            'month_name': month_name,
            'statistics': self.get_flower_data(grouped_orders[month_name]),
        } for month_name in sorted_months]


class StatisticsByMonths(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Flower Statistics"],
        operation_description="Retrieve the total flower sales for the last 5 months, including the current month,"
                              " along with the percentage change compared to the previous month.",
        manual_parameters=[
            openapi.Parameter(
                'flower_id', openapi.IN_QUERY, description="Filter statistics by flower ID", type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: openapi.Response(
                description="Monthly flower sales statistics",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'month': openapi.Schema(type=openapi.TYPE_STRING,
                                                    description="Month and Year (e.g., August 2024)"),
                            'total_sales': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                          description="Total quantity sold in the month"),
                            'change': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT,
                                                     description="Percentage change compared to the previous month")
                        }
                    ),
                ),
            ),
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def get(self, request, *args, **kwargs):
        flower_id = request.query_params.get('flower_id', None)

        current_date = datetime.now()

        start_of_current_month = current_date.replace(day=1)

        months_data = OrderFlowers.objects.filter(
            created_at__gte=start_of_current_month.replace(year=current_date.year, month=current_date.month - 5)
        )

        if flower_id:
            months_data = months_data.filter(flower_id=flower_id)

        monthly_sales = months_data.annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            total_sales=Sum('quantity')
        ).order_by('month')

        sales_data = []

        for month_data in monthly_sales:
            change = (month_data['total_sales'] * 0.10)

            sales_data.append({
                'month': month_data['month'].strftime('%B %Y'),
                'total_sales': month_data['total_sales'],
                'change': round(change, 2)
            })

        return Response(sales_data, status=status.HTTP_200_OK)
