from datetime import date
from django.db.models import Sum


def current_month_total(user):
    today = date.today()

    total = user.expenses.filter(
        expense_date__month=today.month,
        expense_date__year=today.year,
    ).aggregate(
        Sum("amount")
    )["amount__sum"]

    return total or 0


def yearly_total(user):
    today = date.today()

    total = user.expenses.filter(
        expense_date__year=today.year
    ).aggregate(
        Sum("amount")
    )["amount__sum"]

    return total or 0


def category_summary(user):

    return (
        user.expenses.values(
            "category__name"
        )
        .annotate(
            total=Sum("amount")
        )
        .order_by("-total")
    )