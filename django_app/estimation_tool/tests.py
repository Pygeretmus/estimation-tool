import io

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CategoryOptions, OptionChoices, Platform, PlatformOptionsCategory


def create_temp_image():
    image = Image.new("RGB", (100, 100))
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)

    return SimpleUploadedFile("test_image.jpg", img_byte_arr.read(), content_type="image/jpeg")


def setup_database(cls):
    image = create_temp_image()
    for title in ["first", "second"]:
        platform = Platform.objects.create(title=title, description=f"{title} platform", icon=image)
        setattr(cls, f"{title}_platform", platform)
        options_category = PlatformOptionsCategory.objects.create(
            platform=platform, title=f"{title} platform options category"
        )
        category_option_single = CategoryOptions.objects.create(
            category=options_category, title="Single choice", single_choice=True
        )
        category_option_multiple = CategoryOptions.objects.create(
            category=options_category, title="Multiple choice", single_choice=False
        )
        for option_title, designer_hours_amount, developer_hours_amount in [
            ("first", 10, 20),
            ("second", 20, 40),
        ]:
            setattr(
                cls,
                f"{title}_{option_title}_single_choice",
                OptionChoices.objects.create(
                    option=category_option_single,
                    title=option_title,
                    description=f"{option_title} description",
                    icon=image,
                    designer_hours_amount=designer_hours_amount,
                    developer_hours_amount=developer_hours_amount,
                ),
            )

            setattr(
                cls,
                f"{title}_{option_title}_multiple_choice",
                OptionChoices.objects.create(
                    option=category_option_multiple,
                    title=option_title,
                    description=f"{option_title} description",
                    icon=image,
                    designer_hours_amount=designer_hours_amount,
                    developer_hours_amount=developer_hours_amount,
                ),
            )


class PlatformListView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("platform-list")
        setup_database(cls)

    def test_get_succesfull(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], self.first_platform.id)
        self.assertEqual(response.data[0]["title"], self.first_platform.title)
        self.assertEqual(response.data[0]["description"], self.first_platform.description)
        self.assertIn(self.first_platform.icon.url, response.data[0]["icon"])
        self.assertEqual(response.data[1]["id"], self.second_platform.id)
        self.assertEqual(response.data[1]["title"], self.second_platform.title)
        self.assertEqual(response.data[1]["description"], self.second_platform.description)
        self.assertIn(self.second_platform.icon.url, response.data[1]["icon"])


class PlatformRetrieveView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        setup_database(cls)

    def test_get_wrong_id(self):
        response = self.client.get(reverse("platform-detail", kwargs={"pk": 100000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "No Platform matches the given query.")

    def test_get_succesfull(self):
        response = self.client.get(
            reverse("platform-detail", kwargs={"pk": self.first_platform.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["title"], self.first_platform.title)
        self.assertEqual(data["description"], self.first_platform.description)
        self.assertIn(self.first_platform.icon.url, response.data["icon"])
        categories = data["categories"]
        category = categories[0]
        first_category = self.first_platform.categories.first()
        self.assertEqual(len(categories), 1)
        self.assertEqual(category["title"], first_category.title)
        options = category["options"]
        option = options[0]
        first_option = first_category.options.first()
        self.assertEqual(len(options), 2)
        self.assertEqual(option["title"], first_option.title)
        self.assertEqual(option["single_choice"], first_option.single_choice)
        choices = option["choices"]
        choice = choices[0]
        first_choice = first_option.choices.first()
        self.assertEqual(len(choices), 2)
        self.assertEqual(choice["id"], first_choice.id)
        self.assertEqual(choice["title"], first_choice.title)
        self.assertEqual(choice["description"], first_choice.description)
        self.assertIn(first_choice.icon.url, choice["icon"])


class EstimationCreationView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        setup_database(cls)
        cls.url = reverse("estimation-list")
        cls.data = {"option_choices": [1, 2], "hourly_rate": 40}

    def test_create_estimation_successful(self):
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.data
        self.assertEqual(response_data["designer_hours_amount"], 20)
        self.assertEqual(response_data["developer_hours_amount"], 40)
        self.assertEqual(response_data["total_hours"], 60)
        self.assertEqual(response_data["budget"], 2400)

    def test_create_estimation_hourly_rate_required(self):
        data = self.data
        del data["hourly_rate"]
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["message"], "Validation error")
        self.assertEqual(response_data["errors"]["hourly_rate"], "This field is required.")

    def test_create_estimation_option_choices_required(self):
        data = self.data
        del data["option_choices"]
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["message"], "Validation error")
        self.assertEqual(response_data["errors"]["option_choices"], "This field is required.")

    def test_create_estimation_hourly_rate_wrong_type(self):
        data = self.data
        data["hourly_rate"] = ""
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["message"], "Validation error")
        self.assertEqual(response_data["errors"]["hourly_rate"], "A valid integer is required.")

    def test_create_estimation_option_choices_wrong_type(self):
        data = self.data
        data["option_choices"] = ""
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["message"], "Validation error")
        self.assertEqual(
            response_data["errors"]["option_choices"],
            'Expected a list of items but got type "str".',
        )

    def test_create_estimation_hourly_rate_low(self):
        data = self.data
        data["hourly_rate"] = 0
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["message"], "Validation error")
        self.assertEqual(response_data["errors"]["hourly_rate"], "The value must be at least 5.")

    def test_create_estimation_option_choices_empty(self):
        data = self.data
        data["option_choices"] = []
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["message"], "Validation error")
        self.assertEqual(
            response_data["errors"]["option_choices"],
            "This list may not be empty.",
        )

    def test_create_estimation_hourly_rate_not_multiple_of_five(self):
        data = self.data
        data["hourly_rate"] = 6
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["message"], "Validation error")
        self.assertEqual(
            response_data["errors"]["hourly_rate"], "The value must be a multiple of 5."
        )

    def test_create_estimation_two_option_choices_from_single_choice(self):
        data = self.data
        data["option_choices"] = [
            self.first_first_single_choice.id,
            self.first_second_single_choice.id,
        ]
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["message"], "Validation error")
        self.assertEqual(
            response_data["errors"]["option_choices"], "Multiple answers in single choice category."
        )

    def test_create_estimation_two_option_choices_from_different_platforms(self):
        data = self.data
        data["option_choices"] = [
            self.first_first_single_choice.id,
            self.second_first_single_choice.id,
        ]
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["message"], "Validation error")
        self.assertEqual(
            response_data["errors"]["option_choices"], "Answers from different platforms."
        )
