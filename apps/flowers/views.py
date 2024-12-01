from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from apps.flowers.filters import FlowerFilter
from apps.flowers.models import (
    Flower, TopLevelCategory, CountryFlower, PackageFlower, SizesofFlower, BannerCarousel, LiketoFlower,
    ViewUsertoFlower,
)
from apps.flowers.pagination import FlowerPagination
from apps.flowers.serializers import (
    FlowerListSerializer, ReviewSerializer, TopLevelCategoryWithSubCategoriesSerializer,
    FlowerDetailSerializer, CountryFlowerSerializer, PackageFlowerSerializer, SizesofFlowerSerializer,
    BannerCarouselSerializer, LiketoFlowerSerializer, ViewUsertoFlowerSerializer
)
from apps.flowers.utils import get_distinct_product_attributes


class TopLevelCategoryListAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Retrieve All Top-Level Categories",
        operation_description="Get a list of all top-level categories with their details.",
        tags=["Categories"]
    )
    def get(self, request):
        categories = TopLevelCategory.objects.all()
        serializer = TopLevelCategoryWithSubCategoriesSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FlowerListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = FlowerFilter

    @swagger_auto_schema(
        operation_summary="List All Flowers with token",
        operation_description="Retrieve a list of all flowers with their details with token.",
        tags=["Flowers"],
        manual_parameters=[
            openapi.Parameter(
                'name', openapi.IN_QUERY, description="Filter by flower name (partial match)", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'category', openapi.IN_QUERY, description="Filter by category ID", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'package', openapi.IN_QUERY, description="Filter by package ID", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'size', openapi.IN_QUERY, description="Filter by size name (partial match)", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'compound', openapi.IN_QUERY, description="Filter by compound name (partial match)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'quantity', openapi.IN_QUERY, description="Filter by flower quantity (exact match)",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'in_stock', openapi.IN_QUERY, description="Filter by stock availability (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'is_popular', openapi.IN_QUERY, description="Filter by popular availability (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'showcase_online', openapi.IN_QUERY, description="Filter by showcase online availability (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'is_new', openapi.IN_QUERY, description="Filter by new availability (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'plantation', openapi.IN_QUERY, description="Filter by plantation name (partial match)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'stem_height', openapi.IN_QUERY, description="Filter by stem height (exact match)",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'min_price', openapi.IN_QUERY, description="Filter by minimum price", type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'max_price', openapi.IN_QUERY, description="Filter by maximum price", type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'volume', openapi.IN_QUERY, description="Filter by volume (exact match)", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'head_outer_diameter', openapi.IN_QUERY, description="Filter by head outer diameter (exact match)",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'ordering', openapi.IN_QUERY,
                description=(
                        "Specify ordering of results. Use fields like 'price', '-price' for descending order, "
                        "'name', '-name', etc."
                ),
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'page', openapi.IN_QUERY, description="Page number for pagination", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'page_size', openapi.IN_QUERY, description="Number of results per page (default: 10)",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: FlowerDetailSerializer(many=True)}
    )
    def get(self, request):
        flowers = Flower.objects.select_related('author').filter(author=request.user)
        filtered_queryset = self.filterset_class(request.GET, queryset=flowers)
        paginator = FlowerPagination()
        paginated_flowers = paginator.paginate_queryset(filtered_queryset.qs, request)
        serializer = FlowerDetailSerializer(paginated_flowers, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a New Flower",
        operation_description="Create a new flower with its details, including uploaded images.",
        tags=["Flowers"],
        request_body=FlowerListSerializer,
        responses={201: FlowerListSerializer}
    )
    def post(self, request):
        serializer = FlowerListSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            flower = serializer.save()
            return Response(FlowerListSerializer(flower).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlowerListAPIView(APIView):
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = FlowerFilter

    @swagger_auto_schema(
        operation_summary="List All Flowers without Token",
        operation_description="Retrieve a list of all flowers with their details and without token.",
        tags=["Flowers"],
        manual_parameters=[
            openapi.Parameter(
                'name', openapi.IN_QUERY, description="Filter by flower name (partial match)", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'category', openapi.IN_QUERY,
                description="Filter by category IDs (comma-separated list of category IDs)",
                type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)
            ),
            openapi.Parameter(
                'package', openapi.IN_QUERY, description="Filter by package ID", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'size', openapi.IN_QUERY, description="Filter by size name (partial match)", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'compound', openapi.IN_QUERY, description="Filter by compound name (partial match)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'quantity', openapi.IN_QUERY, description="Filter by flower quantity (exact match)",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'in_stock', openapi.IN_QUERY, description="Filter by stock availability (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'is_popular', openapi.IN_QUERY, description="Filter by popular availability (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'showcase_online', openapi.IN_QUERY, description="Filter by showcase online availability (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'is_new', openapi.IN_QUERY, description="Filter by new availability (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'plantation', openapi.IN_QUERY, description="Filter by plantation name (partial match)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'stem_height', openapi.IN_QUERY, description="Filter by stem height (exact match)",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'volume', openapi.IN_QUERY, description="Filter by volume (exact match)", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'min_price', openapi.IN_QUERY, description="Filter by minimum price", type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'max_price', openapi.IN_QUERY, description="Filter by maximum price", type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'head_outer_diameter', openapi.IN_QUERY, description="Filter by head outer diameter (exact match)",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'ordering', openapi.IN_QUERY,
                description=(
                        "Specify ordering of results. Use fields like 'price', '-price' for descending order, "
                        "'name', '-name', etc."
                ),
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'page', openapi.IN_QUERY, description="Page number for pagination", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'page_size', openapi.IN_QUERY, description="Number of results per page (default: 10)",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={200: FlowerDetailSerializer(many=True)}
    )
    def get(self, request):
        flowers = Flower.objects.all()
        filtered_queryset = self.filterset_class(request.GET, queryset=flowers)
        paginator = FlowerPagination()
        paginated_flowers = paginator.paginate_queryset(filtered_queryset.qs, request)
        serializer = FlowerDetailSerializer(paginated_flowers, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class FlowerRetrieveUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve a Flower",
        operation_description="Retrieve the details of a specific flower by its ID.",
        tags=["Flowers"],
        responses={200: FlowerDetailSerializer}
    )
    def get(self, request, pk):

        if request.user.is_authenticated:
            flower = get_object_or_404(Flower, id=pk)
            user = request.user
            if not ViewUsertoFlower.objects.filter(flower=flower, author=user).exists():
                ViewUsertoFlower.objects.create(flower=flower, author=user)
                serializer = FlowerDetailSerializer(flower)
                return Response(serializer.data, status=status.HTTP_200_OK)
        flower = get_object_or_404(Flower, id=pk)
        serializer = FlowerDetailSerializer(flower)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a Flower",
        operation_description="Update the details of a specific flower, including replacing uploaded images.",
        tags=["Flowers"],
        request_body=FlowerListSerializer,
        responses={200: FlowerListSerializer}
    )
    def put(self, request, pk):
        flower = get_object_or_404(Flower, id=pk)
        serializer = FlowerListSerializer(flower, data=request.data, context={"request": request})
        if serializer.is_valid():
            flower = serializer.save()
            return Response(FlowerListSerializer(flower).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a New Review",
        operation_description="Add a new review for a specific flower.",
        tags=["Reviews"],
        request_body=ReviewSerializer,
        responses={201: ReviewSerializer}
    )
    def post(self, request):
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            review = serializer.save()
            return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackageFlowerAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['Package Flowers'])
    def get(self, request):
        reviews = PackageFlower.objects.all()
        serializer = PackageFlowerSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CountryFlowerAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(tags=['Country Flowers'])
    def get(self, request):
        countries = CountryFlower.objects.all()
        serializer = CountryFlowerSerializer(countries, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SizesofFlowerAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(tags=['Sizes of Flowers'])
    def get(self, request):
        countries = SizesofFlower.objects.all()
        serializer = SizesofFlowerSerializer(countries, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class BannerCarouselAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(tags=['Banner Carousel'])
    def get(self, request):
        countries = BannerCarousel.objects.all()
        serializer = BannerCarouselSerializer(countries, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DistinctProductAttributesView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Get distinct product attributes",
        tags=["Flower attributes"],
        responses={
            200: openapi.Response(
                description="Distinct product attributes retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'plantation': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                     items=openapi.Items(type=openapi.TYPE_STRING)),
                        'head_outer_diameter': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                              items=openapi.Items(type=openapi.TYPE_INTEGER)),
                        'volume': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                 items=openapi.Items(type=openapi.TYPE_INTEGER)),
                        'stem_height': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                      items=openapi.Items(type=openapi.TYPE_INTEGER)),
                    }
                )
            )
        }
    )
    def get(self, request):
        distinct_attributes = get_distinct_product_attributes()
        return Response(distinct_attributes)


class LiketoFlowerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Like'],
        operation_description="Like a flower. This will create a new like for the user.",
        request_body=LiketoFlowerSerializer,
        responses={
            201: LiketoFlowerSerializer,
            400: "Bad Request",
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = LiketoFlowerSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LiketoFlowerDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Like'],
        operation_description="Unlike a flower. This will delete the like of a user.",
        responses={
            204: "Like removed successfully",
            404: "You haven't liked this flower",
        }
    )
    def delete(self, request, *args, **kwargs):
        flower_id = kwargs.get('flower_id')
        try:
            like = LiketoFlower.objects.get(flower_id=flower_id, author=request.user)
        except LiketoFlower.DoesNotExist:
            return Response({"error": "You haven't liked this flower"}, status=status.HTTP_404_NOT_FOUND)

        like.delete()
        return Response({"message": "Like removed successfully"}, status=status.HTTP_204_NO_CONTENT)


class ViewUsertoFlowerListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve a list of flowers viewed by the user",
        operation_description="Fetch a list of all the flowers that the authenticated user has viewed.",
        tags=["Flowers seen by user"],
        responses={
            200: ViewUsertoFlowerSerializer(many=True),
            401: "Unauthorized - User is not authenticated"
        }
    )
    def get(self, request):
        queryset = ViewUsertoFlower.objects.select_related('author').filter(
            author=request.user
        )

        serializer = ViewUsertoFlowerSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)