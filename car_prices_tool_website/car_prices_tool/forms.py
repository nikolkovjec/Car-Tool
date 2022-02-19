from django import forms
from car_prices_tool.models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('make', 'model')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = Car.objects.none()
