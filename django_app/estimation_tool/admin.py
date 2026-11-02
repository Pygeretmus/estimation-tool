from django.contrib import admin

from .models import CategoryOptions, Estimation, OptionChoices, Platform, PlatformOptionsCategory


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]


@admin.register(PlatformOptionsCategory)
class PlatformOptionsCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "platform"]
    list_filter = ["platform"]


@admin.register(CategoryOptions)
class CategoryOptionsAdmin(admin.ModelAdmin):
    list_display = ["title", "category__platform", "category__title", "single_choice"]
    list_filter = ["category__platform", "category__title", "single_choice"]


@admin.register(OptionChoices)
class OptionChoices(admin.ModelAdmin):
    list_display = [
        "title",
        "option__category__platform",
        "option__category__title",
        "option__title",
        "designer_hours_amount",
        "developer_hours_amount",
    ]
    list_filter = ["option__category__platform", "option__category__title", "option__title"]


@admin.register(Estimation)
class EstimationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "designer_hours_amount",
        "developer_hours_amount",
        "total_hours",
        "hourly_rate",
        "budget",
    ]
