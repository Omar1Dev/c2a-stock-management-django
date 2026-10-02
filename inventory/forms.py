from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "description",
            "initial_quantity",
            "current_quantity",
            "unit_price",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "e.g. Barre Acier Rond 12mm",
                "autocomplete": "off",
            }),
            "category": forms.TextInput(attrs={
                "placeholder": "e.g. Barres",
                "autocomplete": "off",
            }),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Optional product description...",
            }),
            "initial_quantity": forms.NumberInput(attrs={
                "min": "0",
                "placeholder": "0",
            }),
            "current_quantity": forms.NumberInput(attrs={
                "min": "0",
                "placeholder": "0",
            }),
            "unit_price": forms.NumberInput(attrs={
                "min": "0",
                "step": "0.01",
                "placeholder": "0.00",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        initial_qty = cleaned_data.get("initial_quantity")
        current_qty = cleaned_data.get("current_quantity")

        if initial_qty is not None and current_qty is not None:
            if current_qty > initial_qty:
                self.add_error(
                    "current_quantity",
                    "Current quantity cannot exceed initial quantity."
                )
        return cleaned_data
