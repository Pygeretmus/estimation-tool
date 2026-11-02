from rest_framework import serializers

from .models import CategoryOptions, Estimation, OptionChoices, Platform, PlatformOptionsCategory
from .validators import multiple_of_five_validator


class OptionChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionChoices
        fields = ["id", "title", "description", "icon"]


class CategoryOptionsSerializer(serializers.ModelSerializer):
    choices = OptionChoicesSerializer(many=True, read_only=True)

    class Meta:
        model = CategoryOptions
        fields = ["title", "single_choice", "choices"]


class PlatformOptionsCategorySerializer(serializers.ModelSerializer):
    options = CategoryOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = PlatformOptionsCategory
        fields = ["title", "options"]


class RetrievePlatformSerializer(serializers.ModelSerializer):
    categories = PlatformOptionsCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Platform
        fields = ["title", "description", "icon", "categories"]


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ["id", "title", "description", "icon"]


class EstimationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimation
        fields = [
            "option_choices",
            "designer_hours_amount",
            "developer_hours_amount",
            "total_hours",
            "hourly_rate",
            "budget",
        ]
        extra_kwargs = {
            "option_choices": {"write_only": True},
            "hourly_rate": {
                "write_only": True,
                "required": True,
                "validators": [multiple_of_five_validator],
            },
            "designer_hours_amount": {"read_only": True},
            "developer_hours_amount": {"read_only": True},
            "total_hours": {"read_only": True},
            "budget": {"read_only": True},
        }

    def create(self, validated_data):
        option_choices = validated_data.get("option_choices", [])

        platform_id = option_choices[0].option.category.platform.id
        existing_options = []

        designer_hours_amount, developer_hours_amount = 0, 0

        for choice in option_choices:
            choice_option = choice.option

            if platform_id != choice_option.category.platform.id:
                raise serializers.ValidationError(
                    {"option_choices": "Answers from different platforms."}
                )

            if choice_option.single_choice:
                choice_option_id = choice_option.id
                if choice_option_id in existing_options:
                    raise serializers.ValidationError(
                        {"option_choices": "Multiple answers in single choice category."}
                    )
                existing_options.append(choice_option_id)

            designer_hours_amount += choice.designer_hours_amount
            developer_hours_amount += choice.developer_hours_amount

        total_hours = designer_hours_amount + developer_hours_amount
        hourly_rate = validated_data["hourly_rate"]
        budget = total_hours * hourly_rate

        estimation_object = Estimation.objects.create(
            designer_hours_amount=designer_hours_amount,
            developer_hours_amount=developer_hours_amount,
            total_hours=total_hours,
            budget=budget,
            hourly_rate=hourly_rate,
        )
        estimation_object.option_choices.set(option_choices)

        return estimation_object
