from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('The phone number must be set')

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(phone_number, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=13, unique=True, verbose_name=_('Номер телефона'))
    code = models.CharField(max_length=4, blank=True, null=True, verbose_name=_('Код'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Работник'))
    full_name = models.CharField(max_length=255, blank=True, verbose_name=_('Полное имя'))
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=_('Дата рождения'))
    email = models.EmailField(blank=True, verbose_name=_('Имейл'))
    first_visit = models.BooleanField(default=True, verbose_name=_('Дата первого визита'))
    fcm_token = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Токен'))
    receive_notifications = models.BooleanField(default=False, verbose_name=_('Получать уведомления'), null=True, blank=True)
    is_retiree = models.BooleanField(default=False, verbose_name=_('Пенсионер'))
    retiree_card_front = models.ImageField(upload_to='retiree_cards/', blank=True, null=True,
                                           verbose_name=_('Лицевая сторона карточки пенсионера'))
    retiree_card_back = models.ImageField(upload_to='retiree_cards/', blank=True, null=True,
                                          verbose_name=_('Оборотная сторона карточки пенсионера'))
    is_retiree_approved = models.BooleanField(default=False, verbose_name=_('Прошел модерацию'))

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _("Пользователи")


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name=_("Пользователь"))
    address = models.CharField(max_length=255, verbose_name=_("Адрес"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    is_primary = models.BooleanField(default=False, verbose_name=_("Главный"))

    class Meta:
        verbose_name = _("Адрес пользователя")
        verbose_name_plural = _("Адреса пользователей")
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.address}'
