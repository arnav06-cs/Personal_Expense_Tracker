from decimal import Decimal
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class UserProfile(models.Model):
    """
    Stores additional information for each user.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    monthly_budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    currency = models.CharField(
        max_length=10,
        default="₹",
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username


class Category(models.Model):
    """
    Expense Category
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="categories",
    )

    name = models.CharField(
        max_length=100,
    )

    color = models.CharField(
        max_length=20,
        default="#0d6efd",
    )

    class Meta:
        ordering = ["name"]
        unique_together = ("user", "name")
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Expense(models.Model):
    PAYMENT_CHOICES = [
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("Bank", "Bank"),
        ("Other", "Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expenses",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
    )

    title = models.CharField(
        max_length=200,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="Cash",
    )

    expense_date = models.DateField()

    notes = models.TextField(
        blank=True,
    )

    receipt = models.ImageField(
        upload_to="receipts/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-expense_date", "-created_at"]
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"

    def __str__(self):
        return f"{self.title} - {self.amount}"

    def get_absolute_url(self):
        return reverse(
            "expense_detail",
            kwargs={"pk": self.pk},
        )


class Budget(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    month = models.IntegerField()

    year = models.IntegerField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        unique_together = (
            "user",
            "month",
            "year",
            )
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"


    def __str__(self):
        return f"{self.month}/{self.year}"


class Income(models.Model):
    """
    Income / Earnings Log
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="incomes",
    )

    title = models.CharField(
        max_length=200,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    income_date = models.DateField(
        default=date.today,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-income_date", "-created_at"]
        verbose_name = "Income"
        verbose_name_plural = "Incomes"

    def __str__(self):
        return f"{self.title} - {self.amount}"