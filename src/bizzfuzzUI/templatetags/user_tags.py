from django import template

register = template.Library()


class ValidAgeNode(template.Node):
    def __init__(self, age):
        self.age = template.Variable(age)

    def render(self, context):
        real_age = self.age.resolve(context)
        if real_age <= 13:
            return "blocked"
        return "allowed"


@register.tag(name="valid_age")
def do_valid_age(parser, token):
    age = token.split_contents()
    # print age
    return ValidAgeNode(age[1])


class BizzFuzzNode(template.Node):
    def __init__(self, random_number):
        self.random_number = template.Variable(random_number)

    def render(self,context):
        real_random_number = self.random_number.resolve(context)
        # multiples of both 3 and 5 get the full bizzfuzz
        if real_random_number % 3 == 0 and real_random_number % 5 == 0:
            return "BizzFuzz"
        # multiples of 3 are just Bizzed
        elif real_random_number % 3 == 0:
            return "Bizz"
        # multiples of 5 are Fuzzed
        elif real_random_number % 5 == 0:
            return "Fuzz"
        # anything that's not a multiple of either just has the value returned as a string
        return str(real_random_number)


@register.tag(name="bizzfuzz")
def do_bizzfuzz(parser, token):
    random_number = token.split_contents()
    return BizzFuzzNode(random_number[1])
