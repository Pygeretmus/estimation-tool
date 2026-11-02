from django.db import models


class Platform(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="platforms/")

    def __str__(self):
        return f"{self.title} platform"


class PlatformOptionsCategory(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name="categories")
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.platform} | {self.title}"


class CategoryOptions(models.Model):
    category = models.ForeignKey(
        PlatformOptionsCategory, on_delete=models.CASCADE, related_name="options"
    )
    title = models.CharField(max_length=100)
    single_choice = models.BooleanField()

    def __str__(self):
        return f"{self.category} | {self.title}"


class OptionChoices(models.Model):
    option = models.ForeignKey(CategoryOptions, on_delete=models.CASCADE, related_name="choices")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    icon = models.ImageField(upload_to="option_choices/")
    designer_hours_amount = models.IntegerField(default=0)
    developer_hours_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.option} | {self.title}"


class Estimation(models.Model):
    option_choices = models.ManyToManyField(OptionChoices)
    designer_hours_amount = models.IntegerField(default=0)
    developer_hours_amount = models.IntegerField(default=0)
    total_hours = models.IntegerField(default=0)
    hourly_rate = models.IntegerField(default=0)
    budget = models.IntegerField(default=0)
