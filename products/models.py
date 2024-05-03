from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Sum


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
    def groups_rebuild(self):
        # Проверка, что курс ещё не начался
        if self.start > timezone.now():
            groups = (Group.objects.filter(product=self).annotate(Count('users')).
                      prefetch_related('users').order_by('users__count'))
            # Проверка: группы существуют и разница в количестве участников больше 1
            if groups.count() > 1 and (groups.last().users__count - groups.first().users__count > 1):
                users_number = groups.aggregate(Sum('users__count'))['users__count__sum']  # Всего участников
                shortage = users_number // groups.count() - groups.first().users__count  # Недобор в наименьшей группе
                list_transfer_users = []
                    # Выборка необходимого количества пользователей из максимально заполненных групп
                for _ in range(shortage):
                    group = max(groups, key=lambda x: x.users__count)
                    transfer_user = group.users.first()
                    list_transfer_users.append(transfer_user)
                    group.users.remove(transfer_user)
                groups.first().users.add(*list_transfer_users)
                return 'Группы перукомплектованы'
            else:
                return "Группы же укомплектованы корректно"
        else:
            return "Невозможно переукомплектовать группы, курс уже начался"








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


