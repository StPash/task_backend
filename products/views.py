from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product, ProductAccess, Lesson
from products.serializers import ProductSerializer, LessonSerializer


class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OneProductAPIView(APIView):
    def get(self, request, prod_id, stud_id):
        q = ProductAccess.objects.filter(product_id=prod_id, user=request.user).all()
        if q:
            queryset = Lesson.objects.filter(product=prod_id).all()
            serializer = LessonSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(f'Отсутсвует доступ к продукту')