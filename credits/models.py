from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone


class Credit(models.Model):
    FUEL_CHOICES = [
        ('metan', 'Метан'),
        ('propan', 'Пропан'),
    ]

    debtor_name = models.CharField(max_length=255, verbose_name="ИФО должника")
    car_number = models.CharField(max_length=6, verbose_name="Номер авто", validators=[
        RegexValidator(regex=r'^N\d{3}[A-Z]{2}$', message="Номер авто должен быть в формате N123VA")])
    debtor_phone = models.CharField(
        max_length=13,
        verbose_name="Телефон должника",
        validators=[RegexValidator(regex=r'^\+998\d{9}$', message="Телефон должен быть в формате +998XXXXXXXXX")]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    initial_payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Первоначальная предоплата")
    fuel_type = models.CharField(max_length=6, choices=FUEL_CHOICES, verbose_name="Тип топлива")
    credit_term = models.PositiveIntegerField(verbose_name="Срок кредита (месяцы)",
                                              validators=[MinValueValidator(1), MaxValueValidator(36)])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    is_closed = models.BooleanField(default=False, verbose_name="Закрыт")
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата закрытия")

    def save(self, *args, **kwargs):
        if self.is_closed and self.closed_at is None:
            self.closed_at = timezone.now()
        elif not self.is_closed:
            self.closed_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Кредит для {self.debtor_name}, авто {self.car_number}, топливо {self.get_fuel_type_display()}"

    class Meta:
        verbose_name = 'Кредит'
        verbose_name_plural = 'Кредиты'
