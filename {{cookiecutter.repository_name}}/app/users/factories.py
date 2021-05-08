import factory
from django.contrib.auth import get_user_model
from faker import Factory

User = get_user_model()

faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'john{n}')
    email = factory.Sequence(lambda n: f'lennon{n}@dead.com')
    role = 1
    password = factory.PostGenerationMethodCall('set_password', 'john-doe')
    first_name = faker.name()
    last_name = faker.last_name()
    address = faker.address()
    phone = faker.phone_number()
