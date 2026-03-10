from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Category


class SkillFormTest(TestCase):
    """
    Test suite for the SkillForm.
    """

    def setUp(self):
        """
        Set up test data for the SkillForm.
        """
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(
            name="Test Category", description="This is a test category."
        )

    def test_valid_skill_form(self):
        """
        Test that a valid skill form is accepted.
        """
        from .forms import SkillForm

        form_data = {"name": "Valid Skill", "category": self.category.id}
        form = SkillForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_skill_form(self):
        """
        Test that an invalid skill form is rejected.
        """
        from .forms import SkillForm

        form_data = {"name": "", "category": self.category.id}
        form = SkillForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
