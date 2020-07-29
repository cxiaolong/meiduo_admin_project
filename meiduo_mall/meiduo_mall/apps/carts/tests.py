from django.test import TestCase

# Create your tests here.
if __name__ == '__main__':
    def haha(*args, **kwargs):

        print(args)

        print(*args)

        print(kwargs)

        print(kwargs.items())


    haha(1, 2, 3, 4, 5, a=10, b=20, c=30)


