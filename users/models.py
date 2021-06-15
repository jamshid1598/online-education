from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

from django.db.models.signals import post_save



class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, phone_number, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, phone_number, first_name, password, **other_fields)

    def create_user(self, email, phone_number, first_name, password, **other_fields):
        other_fields.setdefault('is_active', True)
        if not email:
            raise ValueError(_("Siz elektron pochta manzilingizni ko'rsatishingiz kerak"))
        
        email = self.normalize_email(email)
        user  = self.model(email=email, phone_number=phone_number, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class NewUser(AbstractBaseUser, PermissionsMixin):

    email        = models.EmailField(_('Email'), unique=True)
    # user_name = models.CharField(max_length=150, unique=True)
    first_name   = models.CharField(_("First Name"), max_length=150)
    second_name  = models.CharField(_("Second Name"), max_length=150, null=True)    
    phone_number = PhoneNumberField(_('Phone Number'), unique=True) # validators should be a list
    start_date   = models.DateTimeField(default=timezone.now)
    about        = models.TextField(_('biz haqimizda'), max_length=500, blank=True)
    is_staff     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name']

    def __str__(self):
        return self.email



class Teacher(models.Model):
    teacher = models.OneToOneField(NewUser, blank=True, null=True, on_delete=models.SET_NULL, related_name='teacher')
    image   = models.ImageField(_("Teacher Image"), upload_to="teachers-image/", blank=True, null=True)
    career  = models.CharField(_("Career"), max_length=150, blank=True, null=True)
    about   = models.TextField(_("About Teacher"), blank=True, null=True,)

    class Meta:
        verbose_name        = _("Teacher")
        verbose_name_plural = _("Teachers")

    def __str__(self):
        return self.teacher.first_name +" | "+ str(self.teacher.phone_number)

    @property
    def full_name(self):
        if self.teacher.second_name:
            return self.teacher.second_name +"  "+self.teacher.first_name
        else:
            return self.teacher.first_name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

def post_save_teacher_receiver(sender, instance, created, **kwargs):
    teacher = instance
    if created:
        teacher = Teacher(teacher=teacher)
        teacher.save()

post_save.connect(post_save_teacher_receiver, sender=NewUser)