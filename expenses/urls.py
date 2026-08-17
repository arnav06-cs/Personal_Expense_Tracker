from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard",
    ),

    path(
    "register/",
    views.register,
    name="register",
    ),

    path(
        "expenses/",
        views.expense_list,
        name="expense_list",
    ),

    path(
        "expenses/add/",
        views.expense_create,
        name="expense_add",
    ),

    path(
        "expenses/<int:pk>/",
        views.expense_detail,
        name="expense_detail",
    ),

    path(
        "expenses/<int:pk>/edit/",
        views.expense_update,
        name="expense_edit",
    ),

    path(
        "expenses/<int:pk>/delete/",
        views.expense_delete,
        name="expense_delete",
    ),

    path(
        "categories/",
        views.category_list,
        name="category_list",
    ),

    path(
        "categories/add/",
        views.category_create,
        name="category_add",
    ),

    path(
    "categories/<int:pk>/edit/",
    views.category_update,
    name="category_edit",
    ),

path(
    "categories/<int:pk>/delete/",
    views.category_delete,
    name="category_delete",
    ),

    path(
        "profile/",
        views.profile,
        name="profile",
    ),

    path(
        "reports/",
        views.reports,
        name="reports",
    ),

    path(
        "reports/pdf/",
        views.export_pdf,
        name="export_pdf",
    ),

    path(
        "reports/excel/",
        views.export_excel,
        name="export_excel",
    ),

    path(
        "budget/",
        views.budget,
        name="budget",
    ),

    path(
        "ai-advisor/",
        views.ai_advisor,
        name="ai_advisor",
    ),

    path(
        "api/ai-advisor/chat/",
        views.api_ai_advisor_chat,
        name="api_ai_advisor_chat",
    ),

    path(
        "bill-splitter/",
        views.bill_splitter,
        name="bill_splitter",
    ),

    path(
        "incomes/",
        views.income_list,
        name="income_list",
    ),

    path(
        "incomes/<int:pk>/delete/",
        views.income_delete,
        name="income_delete",
    ),

    path(
        "change-currency/",
        views.change_currency,
        name="change_currency",
    ),

    path(
        "arcade/",
        views.arcade_view,
        name="arcade",
    ),
]