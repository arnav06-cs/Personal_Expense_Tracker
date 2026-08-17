from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.db.models import Sum

from .models import Expense
from .models import Category


class ExpenseAdminSite(AdminSite):

    site_header = "Personal Expense Tracker"

    site_title = "Expense Tracker"

    index_title = "Dashboard"

    def each_context(self, request):

        context = super().each_context(request)

        context["total_users"] = User.objects.count()

        context["total_expenses"] = Expense.objects.count()

        context["total_categories"] = Category.objects.count()

        context["total_amount"] = (
            Expense.objects.aggregate(
                total=Sum("amount")
            )["total"] or 0
        )

        return context


expense_admin_site = ExpenseAdminSite(name="expense_admin")

from .models import *

expense_admin_site.register(UserProfile, UserProfileAdmin)
expense_admin_site.register(Category, CategoryAdmin)
expense_admin_site.register(Expense, ExpenseAdmin)
expense_admin_site.register(Budget, BudgetAdmin)