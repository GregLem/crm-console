from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        # Добавляем все поля, которые теперь есть в модели
        fields = ['name', 'phone', 'service', 'source', 'comment', 'status']
        
        # Подписи на русском
        labels = {
            'name': 'Имя клиента',
            'phone': 'Телефон',
            'service': 'Услуга',
            'source': 'Источник заявки',
            'comment': 'Комментарий',
            'status': 'Статус',
        }
        
        # Красивые поля с подсказками
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иван Петров'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'service': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ремонт телефона'
            }),
            'source': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Instagram, рекомендация, сайт...'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Дополнительная информация...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }