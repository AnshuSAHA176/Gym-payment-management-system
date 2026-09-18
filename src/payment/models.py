from django.db import models
import uuid

from members.models import Member


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ("CASH", "Cash"),
        ("UPI", "UPI"),
        ("BANK", "Bank Transfer"),
    ]

    STATUS_CHOICES = [
        ("PAID", "Paid"),
        ("PENDING", "Pending"),
        ("OVERDUE", "Overdue"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField(null=True)

    due_date = models.DateField(null= True)

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PAID"
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.member.name} - {self.amount} - {self.status}"