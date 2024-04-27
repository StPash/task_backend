from django.urls import path

from .views import *

urlpatterns = [
    path('', 'products/', ProductAPIView.as_view()),  # Список доступных для покупки продуктов
    path('product/<int:prod_id>',
         OneProductAPIView.as_view()),  # Спискок уроков по конкретному (prod_id) продукту
]
