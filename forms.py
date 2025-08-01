from django import forms
from .models import Visitor
class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        exclude = ['visit_time']  # or use 'fields' if preferred
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
