from django import template

register = template.Library()

@register.filter(name='join')
def join(collection, seperator):
    joined_string = ""
    last_index = len(collection) -1
    for index, element in enumerate(collection):
        joined_string += str(element)
        if index < last_index:
            joined_string += seperator
    return joined_string

if __name__ == "__main__":
    print(join(["Hara", "John", "Mary"], ":"))