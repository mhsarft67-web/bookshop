from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="کاربر")
    age = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="سن")
    bio = models.TextField(null=True, blank=True, verbose_name="بیوگرافی")


    class Meta:
        verbose_name="پروفایل کاربر"
        verbose_name_plural="پروفایل ها"

    def __str__(self):
        return f"{User.full_name} خوش اومدی"
        

# Create your models here.
