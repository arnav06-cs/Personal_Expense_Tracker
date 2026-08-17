from django import forms
from django.contrib.auth.models import User

from .models import Budget
from .models import Category
from .models import Expense
from .models import Income
from .models import UserProfile


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["title", "amount", "income_date", "notes"]
        widgets = {
            "income_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }


class ExpenseForm(forms.ModelForm):
    """
    Form for creating and updating expenses.
    """

    class Meta:

        model = Expense

        fields = [
            "title",
            "category",
            "amount",
            "payment_method",
            "expense_date",
            "notes",
            "receipt",
        ]

        widgets = {

            "expense_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control"
                }
            ),

        }


    def __init__(self, *args, user=None, **kwargs):

        super().__init__(*args, **kwargs)

        if user:

            self.fields["category"].queryset = Category.objects.filter(
                user=user
            )


class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category

        fields = [
            "name",
            "color",
        ]


class BudgetForm(forms.ModelForm):

    class Meta:
        model = Budget
        fields = [
            "amount",
        ]

class ProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        fields = [
            "profile_picture",
            "monthly_budget",
            "currency",
        ]


class UserUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
        ]