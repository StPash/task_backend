from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count


# Create your models here.


# Сущность продукта
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    author = models.CharField(max_length=255, verbose_name='Автор')
    start = models.DateTimeField(verbose_name='Дата и время старата')
    cost = models.PositiveIntegerField(verbose_name='Стоимость')
    min_group = models.PositiveIntegerField(verbose_name='Макс. кол-во человек в группе')
    max_group = models.PositiveIntegerField(verbose_name='Мин. кол-во человек в группе')

    def __str__(self):
        return self.name

    # # Функция переформирования групп, чтобы количество учеников не отличалось больше, чем на 1
    # def groups_rebuild(self):
    #     # Проверка, что курс ещё не начался
    #     if True:
    #         groups = Group.objects.filter(product=self).annotate(Count('users')).prefetch_related('users')
    #         # Проверка, что группы существуют
    #         if groups:
    #             smallest_group = min(groups, key=lambda x: x.users__count)
    #             shortage = self.max_group - smallest_group.users__count
    #             # Проверка, что есть разница в количестве учеников больше 1
    #             if shortage > 1:
    #                 list_transfer_users = []
    #                 nums_group = len(groups)
    #                 # Выборка необходимого количества пользователей из максимально заполненных групп
    #                 for _ in range(self.max_group - shortage):
    #                     group = max(groups, key=lambda x: x.users__count)
    #                     transfer_user = group.users.first()
    #                     list_transfer_users.append(transfer_user)
    #                     group.users.remove(transfer_user)
    #                 smallest_group.users.add(*list_transfer_users)







# Таблица определяющая доступ пользователей к продуктам
class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='product_user_access_unique')
        ]


# Сущность группы
class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    users = models.ManyToManyField(User)
    # is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'Группа "{self.name}" продукта {self.product}'


# Сущность урока
class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    link = models.CharField(max_length=255, blank=True, verbose_name='Ссылка')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


