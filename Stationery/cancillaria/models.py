from django.db import models
from django.urls import reverse, reverse_lazy


class Cancillaria(models.Model):
    name = models.CharField(max_length=120, default='cancillaria', verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    price = models.FloatField(default=10, verbose_name='Цена')
    date_add = models.DateField(auto_now_add=True, verbose_name='Дата добавления')
    date_update = models.DateField(auto_now=True, null=True, verbose_name='Дата обновления')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, verbose_name='Картинка')
    exist = models.BooleanField(default=True, verbose_name='В каталоге ?')

    supplier = models.ForeignKey('Supplier', on_delete=models.PROTECT, null=True, verbose_name='Поставщик')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'канцтовар'
        verbose_name_plural = 'Канцтовары'
        ordering = ['name']


class Supplier(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название поставщика')
    agent_name = models.CharField(max_length=100, verbose_name='Имя агента поставщика')
    agent_firstname = models.CharField(max_length=100, verbose_name='Фамилия агента поставщика')
    agent_patronymic = models.CharField(max_length=100, verbose_name='Отчество агента поставщика')
    exist = models.BooleanField(default=True, verbose_name='Сотрудничаем?')

    def get_absolute_url(self):
        return reverse('info_supp_view', kwargs={'supplier_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'поставщика'
        verbose_name_plural = 'Поставщики'
        ordering = ['title']


class Order(models.Model):
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    date_finish = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения заказа')
    price = models.FloatField(null=True, verbose_name='Стоимость заказа')
    address_delivery = models.CharField(max_length=150, verbose_name='Адрес доставки')
    status = models.CharField(max_length=150, verbose_name='Статус',
                              choices=[
                                  ('1', 'Создан'),
                                  ('2', 'Отменён'),
                                  ('3', 'Согласован'),
                                  ('4', 'В пути'),
                                  ('5', 'Завершён')
                              ]
                              )

    cancillarias = models.ManyToManyField(Cancillaria, through='Pos_order')

    def __str__(self):
        return f"{self.date_create} {self.status} {self.price}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['date_create']


class Pos_order(models.Model):
    cancillaria = models.ForeignKey(Cancillaria, on_delete=models.PROTECT, verbose_name='Канцтовар')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Заказ')
    count_cancillaria = models.IntegerField(verbose_name='Количество кантовара')
    price = models.FloatField(verbose_name='Общая цена канцтовара')

    def __str__(self):
        return self.cancillaria.name + " " + self.order.address_delivery + " " + self.order.status

    class Meta:
        verbose_name = 'позицию'
        verbose_name_plural = 'Позиции заказа'
        ordering = ['cancillaria', 'order', 'price']


class Chegue(models.Model):
    date_print = models.DateTimeField(auto_now_add=True, verbose_name='Дата распечатки')
    address_print = models.CharField(max_length=150, verbose_name='Место создания чека')
    terminal = models.CharField(max_length=10, verbose_name='Код терминала')
    order = models.OneToOneField(Order, on_delete=models.PROTECT, primary_key=True, verbose_name='Заказ')

    def __str__(self):
        return str(self.date_print) + " " + self.terminal

    class Meta:
        verbose_name = 'чек'
        verbose_name_plural = 'Чек'
        ordering = ['terminal', 'date_print']
