from django.contrib.auth.base_user import BaseUserManager


class UserProfileManager(BaseUserManager):
    def create_user(self, password, **extra_fields):
        # if not email or phone:
        #     raise ValueError(_('Email or Phone must be set.'))
        
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(password, **extra_fields)
