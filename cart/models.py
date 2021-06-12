from django.db import models
from django.urls import reverse

# from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

User = get_user_model()

from product.models import Lesson, SubCategory


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return str(self.user)



def post_save_user_receiver(sender, instance, created, **kwargs):
    user = instance
    if created:
        customer = Customer(user=user)
        customer.save()


post_save.connect(post_save_user_receiver, sender=User)


class OrderedItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_orders", verbose_name=_("Customer"))
    model = models.CharField(max_length=300, blank=True, null=True, verbose_name=_("Model"))
    image = models.ImageField(upload_to="ordered-product/%Y/%m/%d/", blank=True, null=True, verbose_name=_('Rasm'))
    model_quantity = models.IntegerField(default=0, verbose_name=_("Model miqdori"))
    single_price = models.FloatField(default=0, verbose_name=_("Narxi"))
    total_price = models.FloatField(default=0, verbose_name=_("Umumiy narx"))
    date_ordered = models.DateTimeField(auto_now_add=True, verbose_name=_("Yuklangan sanasi"))
    completed = models.BooleanField(default=False, verbose_name=_("Bajarildi"))

    def __str__(self):
        return str(self.customer) + " | " + str(self.completed)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    class Meta:
        ordering = ["-date_ordered"]
        verbose_name = _("Ordered Lesson")
        verbose_name_plural = _("Ordered Lessons")


def post_save_customer_receiver(sender, instance, created, **kwargs):
    customer = instance
    if created:
        ordered_item = OrderedItem(customer=customer)
        ordered_item.save()


post_save.connect(post_save_customer_receiver, sender=Customer)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)  # Customer returns user email
    complete = models.BooleanField(default=False, verbose_name=_('Bajarildi'))
    date_ordered = models.DateTimeField(auto_now_add=True, verbose_name=_('Buyurtma sanasi'))

    # transaction_id = models.CharField(max_length=100, null=True, verbose_name='Translation Id')

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return str(self.id)


class OrderLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name="ordered_lesson", null=True, verbose_name=_("Lesson"))
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name=_("Order"))
    # quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name=_("Miqdori"))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_("Order Date"))
    cart_field = models.BooleanField(default=False)  # This field is only changed through checkbox in cart page

    class Meta:
        verbose_name = _("Order Lesson")
        verbose_name_plural = _("Order Lesson")

    @property
    def get_total(self):
        price = 0
        if self.lesson.discount:
            price = self.lesson.discount
        else:
            price = self.lesson.price
        total = price * self.quantity
        return total


class OrderSingleItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='order_single_item')
    lesson = models.ForeignKey(Lesson, blank=True, null=True, on_delete=models.SET_NULL)
    completed = models.BooleanField(default=False)  # after download is completed this field value must be changed to True
