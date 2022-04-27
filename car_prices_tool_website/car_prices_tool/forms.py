from django import forms
from django.db.models import Count

from car_prices_tool.models import Car


class FreeSearchCarForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FreeSearchCarForm, self).__init__(*args, **kwargs)
        self.fields['make'].choices = self.generate_makes
        self.fields['model'].choices = self.generate_models

    def generate_makes(self):
        list_makes = [('', '--- select make ---')]
        for make in self.makes:
            list_makes.append((make["make"], f'{make["make"]} ({Car.objects.filter(make=make["make"]).count()})'))

        return list_makes

    def generate_models(self):
        list_models = [('', '<-- please select make <--')]
        for model in self.models:
            list_models.append((model["model"], f'{model["model"]} ({Car.objects.filter(model=model["model"]).count()})'))

        return list_models

    make_choices = [('', '--- select make ---')]
    makes = Car.objects.values('make').annotate(count=Count('make')).order_by('count').distinct().reverse()
    make = forms.ChoiceField(choices=make_choices)
    make.widget.attrs.update({'class': 'form-select'})

    state_choices = [('Used', 'Used'), ('New', 'New'), ('both', 'Both')]
    state = forms.ChoiceField(choices=state_choices, widget=forms.RadioSelect, initial='Used')
    state.widget.attrs.update({'class': 'form-horizontal', 'type': 'radio'})

    models = Car.objects.values('model').annotate(count=Count('model')).order_by('count').distinct().reverse()
    model_choices = [('', '<-- please select make <--')]
    model = forms.ChoiceField(choices=model_choices)
    model.widget.attrs.update({'class': 'form-select'})


class SearchCarForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SearchCarForm, self).__init__(*args, **kwargs)
        self.fields['make'].choices = self.generate_makes
        self.fields['model'].choices = self.generate_models

    def generate_makes(self):
        list_makes = [('', '--- select make ---')]
        for make in self.makes:
            list_makes.append((make["make"], f'{make["make"]} ({Car.objects.filter(make=make["make"]).count()})'))

        return list_makes

    def generate_models(self):
        list_models = [('', '<-- please select make <--')]
        for model in self.models:
            list_models.append((model["model"], f'{model["model"]} ({Car.objects.filter(model=model["model"]).count()})'))

        return list_models

    make_choices = [('', '--- select make ---')]
    makes = Car.objects.values('make').annotate(count=Count('make')).order_by('count').distinct().reverse()
    make = forms.ChoiceField(choices=make_choices)
    make.widget.attrs.update({'class': 'form-select'})

    state_choices = [('Used', 'Used'), ('New', 'New'), ('both', 'Both')]
    state = forms.ChoiceField(choices=state_choices, widget=forms.RadioSelect, initial='Used')
    state.widget.attrs.update({'class': 'form-horizontal', 'type': 'radio'})

    models = Car.objects.values('model').annotate(count=Count('model')).order_by('count').distinct().reverse()
    model_choices = [('', '<-- please select make <--')]
    model = forms.ChoiceField(choices=model_choices)
    model.widget.attrs.update({'class': 'form-select'})

    # Offer type:
    offer_type_choices = [('all', 'All'),
                          ('person', 'Person'),
                          ('company', 'Company')]
    offer_type = forms.ChoiceField(choices=offer_type_choices, required=False)
    offer_type.widget.attrs.update({'class': 'form-select'})

    # Mileage:
    mileage_less_more_choices = [('mileage_less_than', 'Mileage equal or less than:'),
                                 ('mileage_more_than', 'Mileage equal or more than:')]
    mileage_less_more = forms.ChoiceField(choices=mileage_less_more_choices, required=False)
    mileage_less_more.widget.attrs.update({'class': 'form-select'})
    mileage = forms.IntegerField(required=False)
    mileage.widget.attrs.update({'class': 'form-control', 'placeholder': '(e.q. 75000) in KMs'})

    # Production year:
    production_year_less_more_choices = [('production_year_less_than', 'Exact or older than:'),
                                         ('production_year_more_than', 'Exact or younger than:'),
                                         ('production_year_exact', 'Exact:')]
    production_year_less_more = forms.ChoiceField(choices=production_year_less_more_choices, required=False)
    production_year_less_more.widget.attrs.update({'class': 'form-select'})
    production_year = forms.IntegerField(required=False)
    production_year.widget.attrs.update({'class': 'form-control', 'placeholder': '(e.q. 2016)'})

    # Price:
    price_less_more_choices = [('price_less_than', 'Equal or cheaper than:'),
                               ('price_more_than', 'Equal or more expensive than:')]
    price_less_more = forms.ChoiceField(choices=price_less_more_choices, required=False)
    price_less_more.widget.attrs.update({'class': 'form-select'})
    price = forms.IntegerField(required=False)
    price.widget.attrs.update({'class': 'form-control', 'placeholder': '(e.q. 12500)'})

    # Price currency:
    price_currency_choices = [('pln', 'PLN'),
                              ('usd', 'USD'),
                              ('eur', 'EUR')]
    price_currency = forms.ChoiceField(widget=forms.RadioSelect, choices=price_currency_choices, required=False)
    price_currency.widget.attrs.update({'class': 'form-horizontal', 'type': 'radio'})

    # Engine capacity:
    engine_capacity_choices = [('engine_capacity_less_than', 'Equal or less than:'),
                               ('engine_capacity_more_than', 'Equal or more than:'),
                               ('engine_capacity_equal', 'Exact:')]
    engine_capacity_less_more = forms.ChoiceField(choices=engine_capacity_choices, required=False)
    engine_capacity_less_more.widget.attrs.update({'class': 'form-select'})
    engine_capacity = forms.FloatField(required=False)
    engine_capacity.widget.attrs.update({'class': 'form-control', 'placeholder': '(e.q. 1.4)'})

    # Engine power:
    engine_power_choices = [('engine_power_less_than', 'Equal or less than:'),
                            ('engine_power_more_than', 'Equal or more than:'),
                            ('engine_power_equal', 'Exact:')]
    engine_power_less_more = forms.ChoiceField(choices=engine_power_choices, required=False)
    engine_power_less_more.widget.attrs.update({'class': 'form-select'})
    engine_power = forms.IntegerField(required=False)
    engine_power.widget.attrs.update({'class': 'form-control', 'placeholder': '(e.q. 160)'})

    def clean(self):
        price = self.cleaned_data.get('price')

        if price:
            self.fields_below_required(['price_currency'])

        return self.cleaned_data

    def fields_below_required(self, fields):
        """Used for conditionally marking fields as required."""
        for field in fields:
            if not self.cleaned_data.get(field, ''):
                msg = forms.ValidationError("This option is required now!")
                self.add_error(field, msg)
