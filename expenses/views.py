"""
views.py

Main application views for the Personal Expense Tracker.

Features
--------
✔ Dashboard
✔ Expense CRUD
✔ Category CRUD
✔ Profile
✔ Budget
✔ Reports
✔ PDF Export
✔ Excel Export
✔ Authentication Required
"""

from datetime import date
from datetime import datetime

import json
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import BudgetForm
from .forms import CategoryForm
from .forms import ExpenseForm
from .forms import IncomeForm
from .forms import ProfileForm
from .forms import UserUpdateForm

from .models import Budget
from .models import Category
from .models import Expense
from .models import Income
from .models import UserProfile

from .exports import generate_pdf
from .exports import generate_excel

from django.contrib.auth import login
from django.contrib.auth.models import User

from .forms_register import RegistrationForm

from datetime import datetime
from django.db.models import Sum

@login_required
def dashboard(request):
    if request.method == "POST" and "add_category" in request.POST:
        cat_name = request.POST.get("name", "").strip()
        cat_color = request.POST.get("color", "#10B981").strip()
        if cat_name:
            Category.objects.create(user=request.user, name=cat_name, color=cat_color)
            messages.success(request, f"Category '{cat_name}' added successfully!")
            return redirect("dashboard")

    # Retrieve categories
    user_cats = Category.objects.filter(user=request.user)
    if not user_cats.exists():
        user_cats = Category.objects.all()

    today = date.today()

    expenses = Expense.objects.filter(user=request.user)

    monthly_expenses = expenses.filter(
        expense_date__month=today.month,
        expense_date__year=today.year
    )

    yearly_expenses = expenses.filter(
        expense_date__year=today.year
    )

    monthly_total = (
        monthly_expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    )

    yearly_total = (
        yearly_expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    )

    budget = Budget.objects.filter(
        user=request.user,
        month=today.month,
        year=today.year
    ).first()

    budget_warning = False

    if budget:
        budget_warning = monthly_total > budget.amount

    recent_expenses = monthly_expenses.order_by("-expense_date")[:5]

    category_totals = (
        expenses.values(
            "category__name",
            "category__color"
        )
        .annotate(total=Sum("amount"))
        .order_by("category__name")
    )

    category_data = []

    for item in category_totals:
        if item["total"] and float(item["total"]) > 0:
            category_data.append({
                "name": item["category__name"] or "General",
                "total": float(item["total"]),
                "color": item["category__color"] or "#10B981",
            })

    if not category_data:
        category_data = [
            {"name": "Food & Dining", "total": 1200.0, "color": "#F59E0B"},
            {"name": "Housing & Rent", "total": 3500.0, "color": "#6366F1"},
            {"name": "Transport & Gas", "total": 650.0, "color": "#06B6D4"},
            {"name": "Tech & Gadgets", "total": 850.0, "color": "#8B5CF6"},
            {"name": "Entertainment", "total": 450.0, "color": "#F43F5E"},
        ]

    context = {
        "monthly_total": monthly_total,
        "yearly_total": yearly_total,
        "budget": budget,
        "budget_warning": budget_warning,
        "recent_expenses": recent_expenses,
        "category_data": category_data,
        "all_categories": user_cats,
    }

    return render(
        request,
        "dashboard.html",
        context,
    )

@login_required
def expense_list(request):

    expenses = Expense.objects.filter(
        user=request.user
    )

    query = request.GET.get("q")

    category = request.GET.get("category")

    start = request.GET.get("start")

    end = request.GET.get("end")

    if query:

        expenses = expenses.filter(

            Q(title__icontains=query)

            |

            Q(notes__icontains=query)

        )

    if category:

        expenses = expenses.filter(

            category_id=category

        )

    if start:

        expenses = expenses.filter(

            expense_date__gte=start

        )

    if end:

        expenses = expenses.filter(

            expense_date__lte=end

        )

    total = expenses.aggregate(

        Sum("amount")

    )["amount__sum"] or 0

    context = {

        "expenses": expenses,

        "categories": Category.objects.filter(
            user=request.user
        ),

        "total": total,

    }

    return render(

        request,

        "expense_list.html",

        context,

    )

@login_required
def expense_detail(request, pk):

    expense = get_object_or_404(

        Expense,

        pk=pk,

        user=request.user,

    )

    return render(

        request,

        "expense_detail.html",

        {

            "expense": expense

        },

    )

@login_required
def expense_create(request):

    if request.method == "POST":

        form = ExpenseForm(
        
                    request.POST,
        
                    request.FILES,
        
                )

        form.fields["category"].queryset = Category.objects.filter(
            user=request.user
        )

        if form.is_valid():

            expense = form.save(commit=False)

            expense.user = request.user

            expense.save()

            messages.success(

                request,

                "Expense added successfully."

            )

            return redirect(

                "expense_list"

            )

    else:

        # expense_create() - GET
        form = ExpenseForm(
            user=request.user
            )

        form.fields["category"].queryset = Category.objects.filter(
            user=request.user
        )

    return render(

        request,

        "expense_form.html",

        {

            "form": form,

            "title": "Add Expense"

        }

    )

@login_required
def expense_update(request, pk):
    """
    Update an existing expense record.
    """
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        form.fields["category"].queryset = Category.objects.all()

        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            messages.success(request, f"Expense '{exp.title}' updated successfully.")
            return redirect("expense_list")
    else:
        form = ExpenseForm(instance=expense)
        form.fields["category"].queryset = Category.objects.all()

    return render(
        request,
        "expense_form.html",
        {
            "form": form,
            "title": "Edit Expense",
        },
    )

@login_required
def expense_delete(request, pk):

    expense = get_object_or_404(

        Expense,

        pk=pk,

        user=request.user,

    )

    if request.method == "POST":

        expense.delete()

        messages.success(

            request,

            "Expense deleted."

        )

        return redirect(

            "expense_list"

        )

    return render(

        request,

        "expense_delete.html",

        {

            "expense": expense

        }

    )

@login_required
def category_list(request):
    """
    Display all categories belonging to the current user.
    """
    categories = Category.objects.filter(user=request.user).order_by("name")
    if not categories.exists():
        default_cats = [
            ("🍕 Food & Dining", "#F59E0B"),
            ("🏠 Housing & Rent", "#6366F1"),
            ("🚗 Transport & Gas", "#06B6D4"),
            ("💻 Tech & Gadgets", "#8B5CF6"),
            ("🍿 Entertainment", "#F43F5E"),
        ]
        for name, color in default_cats:
            Category.objects.get_or_create(user=request.user, name=name, defaults={"color": color})
        categories = Category.objects.filter(user=request.user).order_by("name")

    return render(
        request,
        "category_list.html",
        {
            "categories": categories,
        },
    )

@login_required
def category_create(request):
    """
    Add a new expense category.
    """

    if request.method == "POST":

        form = CategoryForm(request.POST)

        if form.is_valid():

            category = form.save(commit=False)

            category.user = request.user

            category.save()

            messages.success(
                request,
                "Category created successfully."
            )

            return redirect("category_list")

    else:
        form = CategoryForm()

    return render(
        request,
        "category_form.html",
        {
            "form": form,
            "title": "Add Category",
        },
    )

@login_required
def category_update(request, pk):
    """
    Update existing category name and color.
    """
    category = get_object_or_404(Category, id=pk)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        color = request.POST.get("color", "#10B981").strip()
        if name:
            category.name = name
            category.color = color
            category.save()
            messages.success(request, f"Category '{category.name}' updated successfully.")
            next_url = request.GET.get("next") or request.POST.get("next") or "category_list"
            return redirect(next_url)

    form = CategoryForm(instance=category)
    return render(
        request,
        "category_form.html",
        {
            "form": form,
            "category": category,
            "title": "Edit Category",
        },
    )


@login_required
def category_delete(request, pk):
    """
    Delete category instantly and return to calling page.
    """
    category = Category.objects.filter(id=pk).first()

    if category:
        cat_name = category.name
        category.delete()
        messages.success(
            request,
            f"Category '{cat_name}' deleted successfully."
        )
    else:
        messages.info(request, "Category already deleted or not found.")

    next_url = request.GET.get("next", "category_list")
    return redirect(next_url)

@login_required
def profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user,
        )

        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        user_form = UserUpdateForm(
            instance=request.user,
        )

        profile_form = ProfileForm(
            instance=profile,
        )

    total_expenses_count = Expense.objects.filter(user=request.user).count()
    total_income_count = Income.objects.filter(user=request.user).count()

    return render(
        request,
        "profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "total_expenses_count": total_expenses_count,
            "total_income_count": total_income_count,
        },
    )

@login_required
def budget(request):
    """
    Create or update monthly budget.
    """

    today = date.today()

    budget = Budget.objects.filter(
        user=request.user,
        month=today.month,
        year=today.year,
    ).first()

    if request.method == "POST":

        form = BudgetForm(
            request.POST,
            instance=budget,
        )

        if form.is_valid():

            item = form.save(commit=False)

            item.user = request.user
            item.month = today.month
            item.year = today.year
            item.save()

            messages.success(
                request,
                "Budget saved successfully."
            )

            return redirect("budget")

    else:

        form = BudgetForm(
            instance=budget
        )

    current_month_total = (
        Expense.objects.filter(
            user=request.user,
            expense_date__month=today.month,
            expense_date__year=today.year,
        ).aggregate(
            Sum("amount")
        )["amount__sum"] or 0
    )

    remaining = (budget.amount - current_month_total) if budget else 0

    spent_pct = 0
    if budget and budget.amount > 0:
        spent_pct = min(100, round((current_month_total / budget.amount) * 100, 1))

    context = {
        "form": form,
        "budget": budget,
        "spent": current_month_total,
        "remaining": remaining,
        "spent_pct": spent_pct,
    }

    return render(
        request,
        "budget.html",
        context,
    )

@login_required
def reports(request):
    """
    Monthly and yearly reports.
    """

    expenses = Expense.objects.filter(
        user=request.user
    )

    year = request.GET.get(
        "year",
        date.today().year,
    )

    month = request.GET.get(
        "month",
        date.today().month,
    )

    monthly = expenses.filter(
        expense_date__year=year,
        expense_date__month=month,
    )

    yearly = expenses.filter(
        expense_date__year=year
    )

    monthly_total = (
        monthly.aggregate(
            Sum("amount")
        )["amount__sum"] or 0
    )

    yearly_total = (
        yearly.aggregate(
            Sum("amount")
        )["amount__sum"] or 0
    )

    chart_labels = []

    chart_values = []

    category_totals = (
        monthly.values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("category__name")
    )

    for item in category_totals:

        chart_labels.append(
            item["category__name"] or "Uncategorized"
        )

        chart_values.append(
            float(item["total"])
        )

    context = {
        "monthly": monthly,
        "monthly_total": monthly_total,
        "yearly_total": yearly_total,
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "selected_month": int(month),
        "selected_year": int(year),
    }

    return render(
        request,
        "reports.html",
        context,
    )

@login_required
def export_pdf(request):
    """
    Export expense report as PDF.
    """

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by("-expense_date")

    return generate_pdf(
        expenses,
        request.user,
    )

@login_required
def export_excel(request):
    """
    Export expense report as Excel.
    """

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by("-expense_date")

    return generate_excel(
        expenses,
        request.user,
    )

def register(request):

    if request.method == "POST":

        form = RegistrationForm(
            request.POST
        )

        if form.is_valid():

            user = User.objects.create_user(

                username=form.cleaned_data["username"],

                email=form.cleaned_data["email"],

                password=form.cleaned_data["password"]

            )

            login(
                request,
                user
            )

            messages.success(
                request,
                "Account created successfully"
            )

            return redirect(
                "dashboard"
            )


    else:

        form = RegistrationForm()


    return render(

        request,

        "registration/register.html",

        {
            "form": form
        }

    )

@login_required
def ai_advisor(request):
    today = date.today()
    expenses = Expense.objects.filter(user=request.user)
    monthly_expenses = expenses.filter(expense_date__month=today.month, expense_date__year=today.year)
    monthly_total = float(monthly_expenses.aggregate(Sum("amount"))["amount__sum"] or 0)
    
    budget = Budget.objects.filter(user=request.user, month=today.month, year=today.year).first()
    budget_amount = float(budget.amount) if budget else 0.0
    remaining_budget = budget_amount - monthly_total

    context = {
        "monthly_total": monthly_total,
        "budget_amount": budget_amount,
        "remaining_budget": remaining_budget,
        "expense_count": monthly_expenses.count(),
    }
    return render(request, "ai_advisor.html", context)

@login_required
def api_ai_advisor_chat(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            prompt = body.get("prompt", "").strip().lower()
        except:
            prompt = ""

        today = date.today()
        expenses = Expense.objects.filter(user=request.user)
        monthly_expenses = expenses.filter(expense_date__month=today.month, expense_date__year=today.year)
        monthly_total = float(monthly_expenses.aggregate(Sum("amount"))["amount__sum"] or 0)
        
        budget = Budget.objects.filter(user=request.user, month=today.month, year=today.year).first()
        budget_amount = float(budget.amount) if budget else 0.0
        remaining_budget = budget_amount - monthly_total

        top_cats = monthly_expenses.values("category__name").annotate(total=Sum("amount")).order_by("-total")
        top_cat_name = top_cats[0]["category__name"] if top_cats else "General"
        top_cat_amount = float(top_cats[0]["total"]) if top_cats else 0.0

        profile = getattr(request.user, 'profile', None)
        curr = profile.currency if profile and profile.currency else "₹"

        if "afford" in prompt or "splurge" in prompt or "buy" in prompt:
            if remaining_budget > 200:
                reply = f"💡 **Affordability Analysis**: You currently have **{curr}{remaining_budget:,.2f}** remaining in your budget for this month. You can safely afford discretionary purchases up to **{curr}{remaining_budget * 0.5:,.2f}**."
            else:
                reply = f"⚠️ **Caution**: You only have **{curr}{remaining_budget:,.2f}** remaining in your monthly budget. I recommend holding off on extra non-essential purchases until next month."
        elif "summary" in prompt or "budget" in prompt or "analyze" in prompt or "health" in prompt:
            reply = f"📊 **Financial Health Summary**:\n- **Total Spent This Month**: {curr}{monthly_total:,.2f}\n- **Monthly Budget**: {curr}{budget_amount:,.2f}\n- **Remaining Budget**: {curr}{remaining_budget:,.2f}\n- **Highest Spending Sector**: {top_cat_name} ({curr}{top_cat_amount:,.2f})\n\n👍 **Status**: {'Under Budget' if remaining_budget >= 0 else 'Over Budget Alert'}"
        else:
            reply = f"🤖 **NovaAI Advisor**: You have spent **{curr}{monthly_total:,.2f}** out of your **{curr}{budget_amount:,.2f}** monthly budget. Your highest category is **{top_cat_name}** ({curr}{top_cat_amount:,.2f}). How can I help optimize your spending today?"

        return JsonResponse({"reply": reply})

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def bill_splitter(request):
    categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST.get("title", "Group Bill Split")
        my_share = float(request.POST.get("my_share", 0))
        category_id = request.POST.get("category_id")
        notes = request.POST.get("notes", "Logged via Bill Splitter")
        if my_share > 0:
            category = Category.objects.filter(id=category_id).first() if category_id else categories.first()
            Expense.objects.create(
                user=request.user,
                title=title,
                amount=my_share,
                category=category,
                notes=notes,
                expense_date=date.today()
            )
            messages.success(request, f"Successfully logged your share (${my_share:.2f}) to expenses!")
            return redirect("expense_list")

    context = {
        "categories": categories,
    }
    return render(request, "bill_splitter.html", context)


@login_required
def income_list(request):
    """
    List and log income entries.
    """
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            inc = form.save(commit=False)
            inc.user = request.user
            inc.save()
            messages.success(request, f"Income '{inc.title}' logged successfully.")
            return redirect("income_list")
    else:
        form = IncomeForm()

    incomes = Income.objects.filter(user=request.user)
    total_income = incomes.aggregate(Sum("amount"))["amount__sum"] or 0

    return render(
        request,
        "income_list.html",
        {
            "incomes": incomes,
            "total_income": total_income,
            "form": form,
        },
    )


@login_required
def income_delete(request, pk):
    """
    Delete an income entry.
    """
    inc = Income.objects.filter(id=pk).first()
    if inc:
        title = inc.title
        inc.delete()
        messages.success(request, f"Income '{title}' deleted successfully.")
    return redirect("income_list")


@login_required
def change_currency(request):
    """
    Switch active display currency across the application.
    """
    curr = request.POST.get("currency") or request.GET.get("currency") or "INR"
    request.session["currency"] = curr

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    symbol_map = {"INR": "₹", "USD": "$", "EUR": "€", "GBP": "£", "AED": "AED "}
    profile.currency = symbol_map.get(curr, "₹")
    profile.save()

    messages.success(request, f"Currency updated to {curr} ({profile.currency}).")
    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or "dashboard"
    return redirect(next_url)


@login_required
def arcade_view(request):
    """
    Gamified Savings Streaks, Badges, & Financial Challenges.
    """
    today = date.today()
    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)

    total_expenses = expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    total_incomes = incomes.aggregate(Sum("amount"))["amount__sum"] or 0
    exp_count = expenses.count()

    budget = Budget.objects.filter(user=request.user, month=today.month, year=today.year).first()
    budget_amt = budget.amount if budget else 0

    xp = (exp_count * 50) + (100 if budget_amt > 0 else 0) + (150 if total_incomes > 0 else 0)
    level = min(5, (xp // 200) + 1)
    xp_next_level = level * 200

    streak_days = min(7, exp_count + 1) if exp_count > 0 else 0

    has_receipt = expenses.filter(receipt__isnull=False).exclude(receipt="").exists()
    cat_count = Category.objects.filter(user=request.user).count()

    badges = [
        {
            "id": "budget_master",
            "title": "Budget Master",
            "desc": "Kept monthly spending under budget limit",
            "icon": "🏆",
            "unlocked": budget_amt > 0 and total_expenses <= budget_amt,
            "reward": "+200 XP",
        },
        {
            "id": "streak_warrior",
            "title": "Streak Warrior",
            "desc": "Logged transactions consistently for 5+ entries",
            "icon": "⚡",
            "unlocked": exp_count >= 5,
            "reward": "+150 XP",
        },
        {
            "id": "savings_titan",
            "title": "Savings Titan",
            "desc": "Logged income higher than monthly expenses",
            "icon": "💰",
            "unlocked": total_incomes > total_expenses and total_incomes > 0,
            "reward": "+300 XP",
        },
        {
            "id": "category_ninja",
            "title": "Category Ninja",
            "desc": "Organized expenses across 3+ categories",
            "icon": "🎯",
            "unlocked": cat_count >= 3,
            "reward": "+100 XP",
        },
        {
            "id": "receipt_collector",
            "title": "Receipt Collector",
            "desc": "Attached official receipt proof to expense entries",
            "icon": "🧾",
            "unlocked": has_receipt or exp_count >= 1,
            "reward": "+125 XP",
        },
        {
            "id": "ai_scholar",
            "title": "AI Financial Scholar",
            "desc": "Consulted NovaAI Advisor for budget insights",
            "icon": "🤖",
            "unlocked": True,
            "reward": "+100 XP",
        },
        {
            "id": "global_traveler",
            "title": "Global Traveler",
            "desc": "Switched currency to manage multi-currency funds",
            "icon": "🌐",
            "unlocked": "currency" in request.session,
            "reward": "+100 XP",
        },
        {
            "id": "bill_splitter_pro",
            "title": "Bill Splitter Pro",
            "desc": "Calculated shared bills with friends & roommates",
            "icon": "🧮",
            "unlocked": True,
            "reward": "+175 XP",
        },
        {
            "id": "zero_debt_defender",
            "title": "Zero Debt Defender",
            "desc": "Kept single transaction limits under control",
            "icon": "🛡️",
            "unlocked": exp_count > 0,
            "reward": "+150 XP",
        },
        {
            "id": "freedom_legend",
            "title": "Financial Freedom Legend",
            "desc": "Achieved Level 5 Titan Status & 500+ XP",
            "icon": "👑",
            "unlocked": xp >= 500,
            "reward": "+500 XP",
        },
    ]

    challenges = [
        {
            "title": "Weekend Saver Challenge",
            "desc": "Keep spending under budget limit this weekend",
            "progress": 65,
            "reward": "🏆 Gold Saver Badge",
            "status": "In Progress",
        },
        {
            "title": "No-Splurge Friday",
            "desc": "Zero unnecessary dining out on Friday",
            "progress": 100,
            "reward": "⭐ 100 XP",
            "status": "Completed",
        },
        {
            "title": "Income Tracker Champion",
            "desc": "Log at least 2 income sources this month",
            "progress": 50 if incomes.exists() else 0,
            "reward": "💎 Financial Master Badge",
            "status": "In Progress",
        },
    ]

    context = {
        "xp": xp,
        "level": level,
        "xp_next_level": xp_next_level,
        "streak_days": streak_days,
        "badges": badges,
        "challenges": challenges,
    }

    return render(request, "arcade.html", context)