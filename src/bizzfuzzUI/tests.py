from django.test import TestCase

# Test whether the tag will return false for ages 13 AND under, whilte true for all others
class ValidAgeTagTest(TestCase):
    def test_valid_ages(self):
        from django.template import Template, Context
        for test_age in range(10,15):
            #print test_age
            #if test_age == 13:
            #    self.assertEquals(test_age, 13 )
            TEMPLATE = Template("{% load user_tags %} {% valid_age " + str(test_age) + " %}")
            rendered = TEMPLATE.render(Context({}))

            if test_age < 13:
                self.assertIn("blocked", rendered)
            if test_age == 13:
                self.assertIn("blocked", rendered)
            if test_age > 13:
                self.assertIn("allowed", rendered)