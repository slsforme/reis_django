from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import logging 

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('customer', 'Клиент'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"



class Category(models.Model):
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(default=0)
    categories = models.ManyToManyField(Category, related_name="products")
    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name="suppliers")
    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"Заказ #{self.id} от {self.customer.user.username}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"Отзыв от {self.customer.user.username} на {self.product.name}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Shipping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    shipped_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"Доставка для Заказа #{self.order.id}"

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Доставки"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"Оплата для Заказа #{self.order.id}"

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Promotion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percent = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"Акция на {self.product.name} ({self.discount_percent}%)"

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
        

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Order)
def send_order_email(sender, instance, created, **kwargs):
    if created:
        subject = "Спасибо за ваш заказ!"
        message = (
            f"Уважаемый {instance.customer.user.username},\n\n"
            f"Ваш заказ №{instance.id} успешно создан.\n"
            f"Общая сумма заказа: {instance.total_amount}.\n\n"
            "Спасибо за покупку!"
        )
        recipient_email = instance.customer.user.email
        sender_email = settings.EMAIL_HOST_USER

        if recipient_email and sender_email:
            try:
                send_mail(subject, message, sender_email, [recipient_email])
                logger.info("Письмо было отправлено")

            except Exception as e:
                logger.error(f"Failed to send order email: {e}")


@receiver(post_save, sender=Review)
def send_review_notification(sender, instance, created, **kwargs):
    if created:
        subject = f"Новый отзыв на продукт {instance.product.name}"
        message = (
            f"Уважаемый менеджер,\n\nНа продукт '{instance.product.name}' "
            f"поступил новый отзыв от {instance.customer.user.username}.\n\n"
            f"Рейтинг: {instance.rating}/5\nКомментарий: {instance.comment}\n\n"
            "Проверьте панель управления для получения более подробной информации."
        )
        manager_email = getattr(settings, 'MANAGER_EMAIL', None)
        sender_email = settings.EMAIL_HOST_USER

        if manager_email and sender_email:
            try:
                send_mail(subject, message, sender_email, [manager_email])
                logger.info("Письмо было отправлено")

            except Exception as e:
                logger.error(f"Failed to send review notification: {e}")


@receiver(post_save, sender=Shipping)
def send_shipping_update_notification(sender, instance, **kwargs):
    if instance.shipped_date:  # Проверяем, указана ли дата отправки
        subject = f"Ваш заказ №{instance.order.id} доставлен"
        message = (
            f"Уважаемый {instance.order.customer.user.username},\n\n"
            f"Ваш заказ №{instance.order.id} был успешно доставлен.\n\n"
            "Спасибо, что выбрали наш магазин. Желаем вам приятных покупок!"
        )
        customer_email = instance.order.customer.user.email
        sender_email = settings.EMAIL_HOST_USER

        if customer_email and sender_email:
            try:
                send_mail(subject, message, sender_email, [customer_email])
                logger.info("Письмо было отправлено")
            except Exception as e:
                logger.error(f"Failed to send shipping update notification: {e}")