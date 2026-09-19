from django.db import models
import uuid


class Member(models.Model):
    member_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    email = models.EmailField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    joining_date = models.DateField()

    monthly_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_due_date = models.DateField(
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        indexes = [
            models.Index(
                fields=["name"],
                name="member_name_idx"
            ),
            models.Index(
                fields=["is_active"],
                name="member_active_idx"
            ),
            models.Index(
                fields=["payment_due_date"],
                name="member_due_idx"
            ),
        ]

    def __str__(self):
        return self.name