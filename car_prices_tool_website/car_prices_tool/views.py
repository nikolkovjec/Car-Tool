from django.shortcuts import render
from django.http import HttpResponse
from car_prices_tool.models import Car
from django.core import serializers
from django.db.models import Count


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

    context = {
        'cars': cars,
        'makes': makes,
        'models': models
    }

    return render(request, 'car_prices_tool/search.html', context)


def results(request):
    make = request.GET.get('make')
    state = request.GET.get('state')
    model = request.GET.get('model')
    offer_type = request.GET.get('offer_type')
    mileage_less_more = request.GET.get('mileage_less_more')
    mileage = request.GET.get('mileage')
    production_year_less_more = request.GET.get('production_year_less_more')
    production_year = request.GET.get('production_year')
    price_less_more = request.GET.get('price_less_more')
    price = request.GET.get('price')
    price_currency = request.GET.get('price_currency')
    engine_capacity_less_more = request.GET.get('engine_capacity_less_more')
    engine_capacity = request.GET.get('engine_capacity')
    engine_power_less_more = request.GET.get('engine_power_less_more')
    engine_power = request.GET.get('engine_power')

    context = {
        'make': make,
        'state': state,
        'model': model,
        'offer_type': offer_type,
        'mileage_less_more': mileage_less_more,
        'mileage': mileage,
        'production_year_less_more': production_year_less_more,
        'production_year': production_year,
        'price_less_more': price_less_more,
        'price': price,
        'price_currency': price_currency,
        'engine_capacity_less_more': engine_capacity_less_more,
        'engine_capacity': engine_capacity,
        'engine_power_less_more': engine_power_less_more,
        'engine_power': engine_power
    }

    return render(request, 'car_prices_tool/results.html', context)
