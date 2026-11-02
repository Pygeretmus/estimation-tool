from rest_framework import serializers


def multiple_of_five_validator(value):
    """Checks if the given number is a multiple of 5."""

    if value < 5:
        raise serializers.ValidationError("The value must be at least 5.")

    if value % 5 != 0:
        raise serializers.ValidationError("The value must be a multiple of 5.")
