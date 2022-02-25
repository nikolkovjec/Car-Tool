from django.shortcuts import render
from django.http import HttpResponse
from car_prices_tool.models import Car
from django.core import serializers
from django.db.models import Count
from car_prices_tool.forms import SearchCarForm
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy


def home(request):
    cars = Car.objects.filter()
    cars_below = Car.objects.filter(mileage__lte=150000)
    cars_below_2 = Car.objects.filter(price__lte=150000)
    context = {
        'cars': cars,
        'cars_below': cars_below,
        'cars_below_2': cars_below_2
    }

    return render(request, 'car_prices_tool/home.html', context)


def search(request):
    cars = Car.objects.all()
    makes = Car.objects.values('make').annotate(entries=Count('make'))
    models = Car.objects.values('model').annotate(entries=Count('model'))

    form = SearchCarForm
    form_class = SearchCarForm

    success_url = reverse_lazy('search')

    if request.method == 'POST':
        filled_form = SearchCarForm(request.POST)
        if filled_form.is_valid():
            context = {
                'make': filled_form.cleaned_data['make'],
                'state': filled_form.cleaned_data['state'],
                'model': filled_form.cleaned_data['model'],
                'offer_type': filled_form.cleaned_data['offer_type'],
                'mileage_less_more': filled_form.cleaned_data['mileage_less_more'],
                'mileage': filled_form.cleaned_data['mileage'],
                'production_year_less_more': filled_form.cleaned_data['production_year_less_more'],
                'production_year': filled_form.cleaned_data['production_year'],
                'price_less_more': filled_form.cleaned_data['price_less_more'],
                'price': filled_form.cleaned_data['price'],
                'price_currency': filled_form.cleaned_data['price_currency'],
                'engine_capacity_less_more': filled_form.cleaned_data['engine_capacity_less_more'],
                'engine_capacity': filled_form.cleaned_data['engine_capacity'],
                'engine_power_less_more': filled_form.cleaned_data['engine_power_less_more'],
                'engine_power': filled_form.cleaned_data['engine_power']
            }

            return results(request, context)
        else:
            return render(request, 'car_prices_tool/search.html', context={'form': filled_form})

    context = {
        'cars': cars,
        'makes': makes,
        'models': models,
        'form': form
    }

    return render(request, 'car_prices_tool/search.html', context)


def load_models(request):
    make = request.GET.get('make')
    models = Car.objects.values('model').distinct().filter(make=make).all()
    models_count = []
    for model in models:
        models_count.append(Car.objects.filter(model=model['model']).count())

    data = zip(models, models_count)

    return render(request, 'car_prices_tool/models_dropdown_list_options.html', {'data': data})


def results(request, context):
    make = context.get('make')
    state = context.get('state')
    model = context.get('model')
    offer_type = context.get('offer_type')
    mileage_less_more = context.get('mileage_less_more')
    mileage = context.get('mileage')
    production_year_less_more = context.get('production_year_less_more')
    production_year = context.get('production_year')
    price_less_more = context.get('price_less_more')
    price = context.get('price')
    price_currency = context.get('price_currency')
    engine_capacity_less_more = context.get('engine_capacity_less_more')
    engine_capacity = context.get('engine_capacity')
    engine_power_less_more = context.get('engine_power_less_more')
    engine_power = context.get('engine_power')

    cars = Car.objects.filter(make=make, model=model, state=state)

    if offer_type:
        cars = cars.filter(offer_type=offer_type)

    if mileage:
        if mileage_less_more == 'mileage_less_than':
            cars = cars.filter(price__lte=mileage)
        if mileage_less_more == 'mileage_more_than':
            cars = cars.filter(price__gte=mileage)

    if production_year:
        if production_year_less_more == 'production_year_less_than':
            cars = cars.filter(production_year__lte=production_year)
        if production_year_less_more == 'production_year_more_than':
            cars = cars.filter(production_year__gte=production_year)
        if production_year_less_more == 'production_year_exact':
            cars = cars.filter(production_year=production_year)

    if price:
        if price_currency != 'USD':
            if price_currency == 'PLN':
                price = price * 0.27
            if price_currency == 'EUR':
                price = price * 1.21

        if price_less_more == 'price_less_than':
            cars = cars.filter(price_dollars__lte=price)
        if price_less_more == 'price_more_than':
            cars = cars.filter(price_dollars__gte=price)

    if engine_capacity:
        if engine_capacity_less_more == 'engine_capacity_less_than':
            cars = cars.filter(engine_power__lte=engine_power)
        if engine_capacity_less_more == 'engine_capacity_more_than':
            cars = cars.filter(engine_power__gte=engine_power)
        if engine_capacity_less_more == 'engine_capacity_equal':
            cars = cars.filter(engine_power=engine_power)

    if engine_power:
        if engine_power_less_more == 'engine_power_less_than':
            cars = cars.filter(engine_capacity__lte=engine_capacity)
        if engine_power_less_more == 'engine_power_more_than':
            cars = cars.filter(engine_capacity__gte=engine_capacity)
        if engine_power_less_more == 'engine_power_equal':
            cars = cars.filter(engine_capacity=engine_capacity)

    context = {
        'make': context.get('make'),
        'state': context.get('state'),
        'model': context.get('model'),
        'offer_type': context.get('offer_type'),
        'mileage_less_more': context.get('mileage_less_more'),
        'mileage': context.get('mileage'),
        'production_year_less_more': context.get('production_year_less_more'),
        'production_year': context.get('production_year'),
        'price_less_more': context.get('price_less_more'),
        'price': context.get('price'),
        'price_currency': context.get('price_currency'),
        'engine_capacity_less_more': context.get('engine_capacity_less_more'),
        'engine_capacity': context.get('engine_capacity'),
        'engine_power_less_more': context.get('engine_power_less_more'),
        'engine_power': context.get('engine_power'),
    }

    return render(request, 'car_prices_tool/results.html', context)
