from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from multiselectfield import MultiSelectField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields['is_superuser'] = True
        extra_fields['role'] = 'admin'
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    PROJECT_TYPE_CHOICES = (
        ('proposal', "Proposal Factory"),
        ('supervisor', "Supervisor"),
        ('routes', "Routes"),
    )

    username = models.CharField(_('username'), max_length=20, unique=True)
    email = models.EmailField(_('email address'), unique=True, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    password = models.CharField(_('password'), max_length=100)
    role = models.CharField(_('role'), max_length=30, blank=True)

    description = models.CharField(
        _('description'), max_length=500, blank=True)

    profile_picture = models.ImageField(
        _('profile picture'), upload_to='profile_pictures/', default="default/profile_picture.png", null=True)
    capture_count = models.IntegerField(_('capture count'), default=0)
    followers_count = models.IntegerField(_('followers count'), default=0)
    following_count = models.IntegerField(_('following count'), default=0)
    followers = models.ManyToManyField(
        'self', verbose_name=_('followers'), symmetrical=False, blank=True, related_name='followers_set')
    following = models.ManyToManyField(
        'self', verbose_name=_('following'), symmetrical=False, blank=True, related_name='following_set')
    blocked = models.ManyToManyField(
        'self', verbose_name=_('blocked'), symmetrical=False, blank=True, related_name='blocked_set')
    level = models.ForeignKey(
        'level', verbose_name=_('level'), on_delete=models.CASCADE, null=True)
    private = models.BooleanField(_('private'), default=False)
    objects = UserManager()
    reports_count = models.IntegerField(_('reports count'), default=0)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class level(models.Model):
    name = models.CharField(_('name'), max_length=30, blank=True)
    image = models.ImageField(
        _('image'), upload_to='level_images/', blank=True, null=True)
    experience = models.IntegerField(_('experience'), default=0)
    experience_to_next_level = models.IntegerField(
        _('experience to next level'), default=0)

    class Meta:
        verbose_name = _('level')
        verbose_name_plural = _('levels')


class awards(models.Model):
    name = models.CharField(_('name'), max_length=100, blank=True)
    description = models.CharField(
        _('description'), max_length=200, blank=True)
    image = models.ImageField(
        _('image'), upload_to='awards_images/', blank=True, null=True)

    class Meta:
        verbose_name = _('awards')
        verbose_name_plural = _('awards')
