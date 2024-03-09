import uuid
from django.db.models import Sum
from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    # user_profile = models.ForeignKey(
    #     "UserProfile",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="orders",
    # )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    consultation_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
    )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )

    # original_cart = models.TextField(null=False, blank=False, default='')
    # stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    class Meta:
        verbose_name_plural = "Orders"

    def _generate_order_number(self):
        """
        Generate a random & unique order number with UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total when a line item is added,
        accounting for consultation cost.
        """
        self.order_total = (
            self.lineitems.aggregate(Sum("lineitem_total"))["lineitem_total__sum"] or 0
        )
        # Check if order total is less than the free consultation threshold
        if self.order_total < settings.FREE_CONSULTATION_THRESHOLD:
            # If below threshold, fixed consultation cost applies
            self.consultation_cost = settings.FIXED_CONSULTATION_COST
        else:
            # If threshold is met or exceeded, consultation is free
            self.consultation_cost = 0
        self.grand_total = self.order_total + self.consultation_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="lineitems",
    )
    product = models.ForeignKey(
        Product,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="order_lineitems",
    )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=8, decimal_places=2, null=False, blank=False, editable=False
    )

    class Meta:
        verbose_name_plural = "Order Line Items"

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return (
            f"{self.quantity} x {self.product.name} on order {self.order.order_number}"
        )
