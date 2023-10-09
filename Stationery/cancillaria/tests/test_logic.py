from django.test import TestCase
from cancillaria.utils import *


class DefaultValueTestCase(TestCase, Default_value):
    def test_DefaultContext_pass(self):
        context = {}
        context = self.get_default_context()
        self.assertTrue(context == {'title': 'Страница'})

    def test_addDefaultContext_pass(self):
        context = {'1': 'test'}
        context = self.add_default_context(context)
        self.assertTrue(context == {'1': 'test', 'title': 'Страница по умолчанию'})

    def test_addTitleContext_pass(self):
        context = {'1': 'test'}
        context = self.add_title_context(context, 'Заголовок')
        self.assertTrue(context == {'1': 'test', 'title': 'Заголовок'})