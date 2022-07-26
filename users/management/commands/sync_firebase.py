import firebase_admin
from firebase_admin import credentials, auth
from django.core.management.base import BaseCommand
from users.models import UserProfile, Profile

# python manage.py seed --mode=refresh

""" Clear all data and creates collectiones """
MODE_REFRESH = "refresh"

""" Clear all data and do not create any object """
MODE_CLEAR = "clear"


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument("--mode", type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write("seeding data...")
        run_seed(self, options["mode"])
        self.stdout.write("done.")



def cloning_users():
    """Creates an user object combining different elements from the list"""
    print("Creating Users")
    page = auth.list_users()

    while page:
        for user in page.users:
            user_instance,created = UserProfile.objects.get_or_create(email=user.email,username=user.uid)
            if created:
                user.is_active=not user.disabled,
                user_instance.set_password("defaultpassword")
                user_instance.save()
                print("{} user created.".format(user_instance))

                profile = Profile(
                user=user_instance,
                name=user.display_name,
                avatar=user.photo_url,)
                
                profile.save()
                print("{} profile created.".format(Profile))
            else:
                print("{} user exists.".format(user_instance))
            
        page = page.get_next_page()


def run_seed(self, mode):
    """Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    cloning_users()
