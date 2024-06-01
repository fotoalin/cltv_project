from django import forms

from .models import CustomerData


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = CustomerData
        fields = ["upload"]
