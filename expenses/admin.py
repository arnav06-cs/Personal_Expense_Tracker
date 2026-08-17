from django.contrib import admin
from django.utils.html import format_html

from .models import UserProfile
from .models import Category
from .models import Expense
from .models import Income
from .models import Budget


# ==========================================
# USER PROFILE
# ==========================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "photo",
        "user",
        "monthly_budget",
        "currency",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "photo_preview",
    )

    fieldsets = (
        (
            "User",
            {
                "fields": (
                    "user",
                )
            }
        ),
        (
            "Profile",
            {
                "fields": (
                    "profile_picture",
                    "photo_preview",
                    "monthly_budget",
                    "currency",
                )
            }
        ),
    )

    def photo(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%;">',
                obj.profile_picture.url,
            )
        return "No Photo"

    photo.short_description = "Photo"

    def photo_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="200" style="border-radius:10px;">',
                obj.profile_picture.url,
            )
        return "No Photo Uploaded"

    photo_preview.short_description = "Preview"


# ==========================================
# CATEGORY
# ==========================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "user",
        "color_box",
    )

    search_fields = (
        "name",
        "user__username",
    )

    list_filter = (
        "user",
    )

    ordering = (
        "name",
    )

    def color_box(self, obj):
        return format_html(
            '<div style="width:25px;height:25px;background:{};border-radius:5px;"></div>',
            obj.color,
        )

    color_box.short_description = "Color"


# ==========================================
# EXPENSE
# ==========================================

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "user",
        "category",
        "amount",
        "payment_method",
        "expense_date",
        "receipt_image",
    )

    search_fields = (
        "title",
        "notes",
        "user__username",
    )

    list_filter = (
        "category",
        "payment_method",
        "expense_date",
    )

    ordering = (
        "-expense_date",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "receipt_preview",
    )

    fieldsets = (

        ("Expense", {
            "fields": (
                "user",
                "title",
                "category",
                "amount",
                "payment_method",
                "expense_date",
            )
        }),

        ("Receipt", {
            "fields": (
                "receipt",
                "receipt_preview",
            )
        }),

        ("Notes", {
            "fields": (
                "notes",
            )
        }),

        ("System", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    def receipt_image(self, obj):
        if obj.receipt:
            return format_html(
                '<img src="{}" width="60">',
                obj.receipt.url,
            )
        return "-"

    receipt_image.short_description = "Receipt"

    def receipt_preview(self, obj):
        if obj.receipt:
            return format_html(
                '<img src="{}" width="300">',
                obj.receipt.url,
            )
        return "No Receipt"

    receipt_preview.short_description = "Receipt Preview"


# ==========================================
# BUDGET
# ==========================================

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "month",
        "year",
        "amount",
    )

    search_fields = (
        "user__username",
    )

    list_filter = (
        "year",
        "month",
    )

    ordering = (
        "-year",
        "-month",
    )


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "amount", "income_date")
    search_fields = ("title", "notes", "user__username")
    list_filter = ("income_date",)
    ordering = ("-income_date",)


# ==========================================
# SITE BRANDING
# ==========================================

admin.site.site_header = "NovaSpend Executive Administration Console"

admin.site.site_title = "NovaSpend Executive Console"

admin.site.index_title = "System Management & Database Records"