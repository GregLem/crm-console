from django.db import models

class Lead(models.Model):
    # choices — это список кортежей (значение_в_БД, человекопонятное_название)
    STATUS_CHOICES = [
        ('new', '🆕 Новая заявка'),
        ('in_progress', '🔧 В работе'),
        ('proposal', '📄 КП отправлено'),
        ('negotiation', '💬 Переговоры'),
        ('won', '✅ Сделка выиграна'),
        ('lost', '❌ Сделка проиграна'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    service = models.CharField(max_length=200, verbose_name='Услуга')
    
    # Новые поля ↓
    source = models.CharField(
        max_length=100, 
        verbose_name='Источник', 
        blank=True  # необязательное поле
    )
    comment = models.TextField(
        verbose_name='Комментарий', 
        blank=True  # необязательное поле
    )
    
    # Статус — строка с выбором из STATUS_CHOICES
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',  # по умолчанию "Новая заявка"
        verbose_name='Статус'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Заявка'        # название в единственном числе
        verbose_name_plural = 'Заявки' # название во множественном числе
        ordering = ['-created_at']     # сортировка: новые сверху

    def __str__(self):
        return f"{self.name} - {self.phone}"