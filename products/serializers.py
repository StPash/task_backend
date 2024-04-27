from rest_framework import serializers
from .models import Product, Lesson


class ProductSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'author', 'cost', 'num_lessons')

    def get_num_lessons(self, obj):
        return Lesson.objects.filter(product=obj.pk).count()

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('name',)
