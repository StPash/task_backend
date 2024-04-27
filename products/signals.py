from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import ProductAccess, Group


@receiver(post_save, sender=ProductAccess)
def group_filling(sender, instance, created, **kwargs):
    product = instance.product
    user = instance.user
    if created:
        # Выбор групп учеников относящихся к конкретному продукту
        groups = Group.objects.filter(product=product).select_related('product').annotate(Count('users'))
        if groups:
            # Определение группы с минимальным количсетвом учеников
            group = min(groups, key=lambda x: x.users__count)
            # Создание новой группы, если все существующие заполнены. Добавление ученика
            if group.users__count == group.product.max_group:
                group_nums = Group.objects.all().count()
                new_group_name = f'Группа № {group_nums + 1} по курсу {product.name}'
                group = Group.objects.create(name=new_group_name, product=product)
                group.users.add(user)
            # Добавление пользователя в группы с минимальным количсетвом учеников
            else:
                group.users.add(user)
        # Создание группы, если по продукты не существет групп. Добавление ученика
        else:
            new_group_name = f'Группа № 1 по курсу {product.name}'
            group = Group.objects.create(name=new_group_name, product=product)
            group.users.add(user)
