from car_prices_tool import all_jscharts
from django.shortcuts import render, redirect
from car_prices_tool.models import Car, UserSearchQuery, UserPremiumRank, CarMake
from django.db.models import Count
from car_prices_tool.forms import SearchCarForm, FreeSearchCarForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django import template
import pendulum

register = template.Library()

usd_pln = 3.73
usd_eur = 0.82


def home(request):
    cars = Car.objects.all()
    makes = Car.objects.values('make').annotate(entries=Count('make'))
    models = Car.objects.values('model').annotate(entries=Count('model'))

    form = FreeSearchCarForm

    if request.method == 'POST':
        filled_form = FreeSearchCarForm(request.POST)
        if filled_form.is_valid():
            context = {
                'make': filled_form.cleaned_data['make'],
                'state': filled_form.cleaned_data['state'],
                'model': filled_form.cleaned_data['model'],
            }

            return results_demo(request, context)
    else:
        cars = Car.objects.filter()
        cars_below = Car.objects.filter(mileage__lte=150000)
        cars_below_2 = Car.objects.filter(price__lte=150000)

        context = {
            'form': form,
            'cars': cars,
            'cars_below': cars_below,
            'cars_below_2': cars_below_2,
            'home_popularmakes_barchart': all_jscharts.home_popularmakes_barchart(),
            'home_popularproductionyears_piechart': all_jscharts.home_popularproductionyears_piechart(),
            'home_average_cars_used_info_radarchart': all_jscharts.home_average_cars_used_info_radarchart()
        }

        return render(request, 'car_prices_tool/home.html', context)


def about(request):
    return render(request, 'car_prices_tool/about.html')


def features(request):
    context = {
        'home_popularmakes_barchart': all_jscharts.home_popularmakes_barchart(),
        'home_popularproductionyears_piechart': all_jscharts.home_popularproductionyears_piechart(),
        'home_average_cars_used_info_radarchart': all_jscharts.home_average_cars_used_info_radarchart()
    }

    return render(request, 'car_prices_tool/features.html', context)


def pricing(request):
    return render(request, 'car_prices_tool/pricing.html')


def no_results(request):
    return render(request, 'car_prices_tool/no_results.html')


def go_premium(request):
    if request.method == 'GET':
        try:
            user_rank_name = UserPremiumRank.objects.filter(user=request.user).values('rank').get()
        except UserPremiumRank.DoesNotExist:
            user_rank_name = {}

        if user_rank_name.get('rank') == 'Premium':
            context = {
                'message': 'It seems that you already have Premium account. Thank you!'
            }

            return render(request, 'car_prices_tool/go_premium.html', context)
        else:
            return render(request, 'car_prices_tool/go_premium.html')
    else:
        get_premium = UserPremiumRank(user=request.user, rank='Premium')
        get_premium.save()

        context = {
            'message': 'Thank you very much for supporting our website! Enjoy your premium account!'
        }

        return render(request, 'car_prices_tool/go_premium.html', context)


def sign_up_user(request):
    if request.method == 'GET':
        context = {
            'form': UserCreationForm()
        }

        return render(request, 'car_prices_tool/signup.html', context)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)

                return redirect('search')
            except IntegrityError:
                context = {
                    'form': UserCreationForm(),
                    'error': 'This username is already taken. Please choose another one.'
                }

                return render(request, 'car_prices_tool/signup.html', context)
        else:
            context = {
                'form': UserCreationForm(),
                'error': 'Password did not match!'
            }

            return render(request, 'car_prices_tool/signup.html', context)


def log_in_user(request):
    if request.method == 'GET':
        context = {
            'form': AuthenticationForm()
        }

        return render(request, 'car_prices_tool/login.html', context)
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)

            return redirect('search')
        else:
            context = {
                'form': AuthenticationForm(),
                'error': 'Wrong password or username.'
            }

            return render(request, 'car_prices_tool/login.html', context)


def log_out_user(request):
    if request.method == 'POST':
        logout(request)

        return render(request, 'car_prices_tool/home.html')


@login_required
def search(request):
    cars = Car.objects.all()
    makes = Car.objects.values('make').annotate(entries=Count('make'))
    models = Car.objects.values('model').annotate(entries=Count('model'))

    form = SearchCarForm
    form_class = SearchCarForm

    success_url = reverse_lazy('search')
    try:
        user_rank = UserPremiumRank.objects.filter(user=request.user).values('rank').get()
    except UserPremiumRank.DoesNotExist:
        user_rank = {}

    today = date.today()
    last_user_searches = UserSearchQuery.objects.filter(user=request.user, date__year=today.year, date__month=today.month, date__day=today.day).count()

    if user_rank.get('rank') == 'Premium':
        available_searches = 100 - last_user_searches
    else:
        available_searches = 10 - last_user_searches

    available_searches_multiplied = available_searches * 10
    searches_multiplied = last_user_searches * 10

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
            if user_rank.get('rank') == 'Premium':
                if last_user_searches < 100:
                    new_search = UserSearchQuery(user=request.user, search_parameters=context)
                    new_search.save()

                    return results(request, context)
                else:
                    context = {
                        'quota_error': 'No searches left for today!'
                    }

                    return render(request, 'car_prices_tool/search.html', context)
            else:
                if last_user_searches < 10:
                    new_search = UserSearchQuery(user=request.user, search_parameters=context)
                    new_search.save()

                    return results(request, context)
                else:
                    context = {
                        'quota_error': 'No searches left for today!'
                    }

                    return render(request, 'car_prices_tool/search.html', context)
        else:
            context = {
                'form': filled_form,
                'last_user_searches': last_user_searches,
                'user_rank': user_rank,
                'searches_multiplied': searches_multiplied,
                'available_searches': available_searches,
                'available_searches_multiplied': available_searches_multiplied
            }

            return render(request, 'car_prices_tool/search.html', context)

    context = {
        'cars': cars,
        'makes': makes,
        'models': models,
        'form': form,
        'last_user_searches': last_user_searches,
        'searches_multiplied': searches_multiplied,
        'available_searches': available_searches,
        'available_searches_multiplied': available_searches_multiplied,
        'user_rank': user_rank
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
    mileage = None if context.get('mileage') == '' else context.get('mileage')
    production_year_less_more = context.get('production_year_less_more')
    production_year = None if context.get('production_year') == '' else context.get('production_year')
    price_less_more = context.get('price_less_more')
    price = None if context.get('price') == '' else context.get('price')
    price_currency = context.get('price_currency')
    engine_capacity_less_more = context.get('engine_capacity_less_more')
    engine_capacity = None if context.get('engine_capacity') == '' else context.get('engine_capacity')
    engine_power_less_more = context.get('engine_power_less_more')
    engine_power = None if context.get('engine_power') == '' else context.get('engine_power')

    filters = {}

    filters['make'] = make
    filters['model'] = model
    filters['state'] = state

    if offer_type:
        filters['offer_type'] = offer_type

    if mileage:
        if mileage_less_more == 'mileage_less_than':
            filters['mileage__lte'] = mileage
        if mileage_less_more == 'mileage_more_than':
            filters['mileage__gte'] = mileage

    if production_year:
        if production_year_less_more == 'production_year_less_than':
            filters['production_year__lte'] = production_year
        if production_year_less_more == 'production_year_more_than':
            filters['production_year__gte'] = production_year
        if production_year_less_more == 'production_year_exact':
            filters['production_year'] = production_year

    if price:
        if price_currency != 'USD':
            if price_currency == 'PLN':
                price = price * 0.27
            if price_currency == 'EUR':
                price = price * 1.21

        if price_less_more == 'price_less_than':
            filters['price_dollars__lte'] = price
        if price_less_more == 'price_more_than':
            filters['price_dollars__gte'] = price

    if engine_capacity:
        if engine_capacity_less_more == 'engine_capacity_less_than':
            filters['engine_power__lte'] = engine_power
        if engine_capacity_less_more == 'engine_capacity_more_than':
            filters['engine_power__gte'] = engine_power
        if engine_capacity_less_more == 'engine_capacity_equal':
            filters['engine_power'] = engine_power

    if engine_power:
        if engine_power_less_more == 'engine_power_less_than':
            filters['engine_capacity__lte'] = engine_capacity
        if engine_power_less_more == 'engine_power_more_than':
            filters['engine_capacity__gte'] = engine_capacity
        if engine_power_less_more == 'engine_power_equal':
            filters['engine_capacity'] = engine_capacity

    cars = Car.objects.filter(**filters)

    cars_amount = len(cars)
    print(len(cars))

    if len(cars) == 0:
        return render(request, 'car_prices_tool/no_results.html')

    average_price_usd = '{:.2f}'.format(cars.aggregate(Avg('price_dollars'))['price_dollars__avg'])
    average_price_pln = '{:.2f}'.format(cars.aggregate(Avg('price_dollars'))['price_dollars__avg'] * usd_pln)
    average_price_eur = '{:.2f}'.format(cars.aggregate(Avg('price_dollars'))['price_dollars__avg'] * usd_eur)
    average_mileage = '{:.2f}'.format(cars.aggregate(Avg('mileage'))['mileage__avg'])
    average_production_year = int(cars.aggregate(Avg('production_year'))['production_year__avg'])
    average_engine_power = int(cars.aggregate(Avg('engine_power'))['engine_power__avg'])
    average_engine_capacity = '{:.2f}'.format(cars.aggregate(Avg('engine_capacity'))['engine_capacity__avg'])

    popular_model_variants = cars.filter(model_variant__isnull=False).values('model_variant').annotate(count=Count('model_variant')).order_by('count').reverse()[:10]

    pmv_dict = {}

    for pmv in popular_model_variants:
        pmv_dict[f'{pmv["model_variant"]}'] = []
        pmv_dict[f'{pmv["model_variant"]}'].append('{:.2f}'.format(cars.filter(model_variant=pmv["model_variant"]).aggregate(Avg('price_dollars'))['price_dollars__avg'] * usd_pln))
        pmv_dict[f'{pmv["model_variant"]}'].append('{:.2f}'.format(cars.filter(model_variant=pmv["model_variant"]).aggregate(Avg('price_dollars'))['price_dollars__avg']))
        pmv_dict[f'{pmv["model_variant"]}'].append('{:.2f}'.format(cars.filter(model_variant=pmv["model_variant"]).aggregate(Avg('price_dollars'))['price_dollars__avg'] * usd_eur))
        pmv_dict[f'{pmv["model_variant"]}'].append(int(cars.filter(model_variant=pmv["model_variant"]).aggregate(Avg('mileage'))['mileage__avg']))
        pmv_dict[f'{pmv["model_variant"]}'].append(int(cars.filter(model_variant=pmv["model_variant"]).aggregate(Avg('production_year'))['production_year__avg']))
        pmv_dict[f'{pmv["model_variant"]}'].append(int(cars.filter(model_variant=pmv["model_variant"]).aggregate(Avg('engine_power'))['engine_power__avg']))
        pmv_dict[f'{pmv["model_variant"]}'].append('{:.2f}'.format(cars.filter(model_variant=pmv["model_variant"]).aggregate(Avg('engine_capacity'))['engine_capacity__avg']))

    pmv_info_dict = {}

    pmv_info_dict_price = {}
    pmv_info_dict_mileage = {}

    current_year = pendulum.now('UTC')
    period = pendulum.period(current_year.subtract(years=10), current_year)
    years_list = []

    for year in period.range('years'):
        years_list.append(year.year)

    for pmv in popular_model_variants:
        pmv_info_dict_price[f'{pmv["model_variant"]}'] = []
        pmv_info_dict_mileage[f'{pmv["model_variant"]}'] = []
        for year in period.range('years'):
            price = cars.filter(model_variant=pmv["model_variant"], production_year=year.year).aggregate(Avg('price_dollars'))['price_dollars__avg']
            if price:
                pmv_info_dict_price[f'{pmv["model_variant"]}'].append(price)
            else:
                pmv_info_dict_price[f'{pmv["model_variant"]}'].append(0)

            mileage = cars.filter(model_variant=pmv["model_variant"], production_year=year.year).aggregate(Avg('mileage'))['mileage__avg']
            if mileage:
                pmv_info_dict_mileage[f'{pmv["model_variant"]}'].append(mileage)
            else:
                pmv_info_dict_mileage[f'{pmv["model_variant"]}'].append(0)

    context = {
        'years_list': years_list,
        'pmv_info_dict': pmv_info_dict,
        'pmv_info_dict_price': pmv_info_dict_price,
        'pmv_info_dict_mileage': pmv_info_dict_mileage,
        'cars_amount': cars_amount,
        'average_price_usd': average_price_usd,
        'average_price_pln': average_price_pln,
        'average_price_eur': average_price_eur,
        'average_mileage': average_mileage,
        'average_production_year': average_production_year,
        'average_engine_power': average_engine_power,
        'average_engine_capacity': average_engine_capacity,
        'popular_model_variants': popular_model_variants,
        'pmv_dict': pmv_dict,
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


def results_demo(request, context):
    make = context.get('make')
    state = context.get('state')
    model = context.get('model')

    cars = Car.objects.filter(make=make, model=model, state=state)

    cars_amount = cars.count()

    average_price = '{:.2f}'.format(cars.aggregate(Avg('price'))['price__avg'])
    average_mileage = '{:.2f}'.format(cars.aggregate(Avg('mileage'))['mileage__avg'])
    average_production_year = int(cars.aggregate(Avg('production_year'))['production_year__avg'])
    average_engine_power = int(cars.aggregate(Avg('engine_power'))['engine_power__avg'])
    average_engine_capacity = '{:.2f}'.format(cars.aggregate(Avg('engine_capacity'))['engine_capacity__avg'])

    popular_model_variants = cars.values('model_variant').annotate(count=Count('model_variant')).order_by('count').reverse()[:3]
    pmv_dict = {}

    for pmv in popular_model_variants:
        pmv_dict[f'{pmv["model_variant"]}'] = []
        pmv_dict[f'{pmv["model_variant"]}'].append('{:.2f}'.format(cars.filter(model_variant=pmv["model_variant"]).aggregate(Avg('price_dollars'))['price_dollars__avg'] * usd_pln))
        pmv_dict[f'{pmv["model_variant"]}'].append('{:.2f}'.format(cars.filter(model_variant=pmv["model_variant"]).aggregate(Avg('price_dollars'))['price_dollars__avg']))
        pmv_dict[f'{pmv["model_variant"]}'].append('{:.2f}'.format(cars.filter(model_variant=pmv["model_variant"]).aggregate(Avg('price_dollars'))['price_dollars__avg'] * usd_eur))
        pmv_dict[f'{pmv["model_variant"]}'].append(int(cars.filter(model_variant=pmv["model_variant"]).aggregate(Avg('mileage'))['mileage__avg']))
        pmv_dict[f'{pmv["model_variant"]}'].append(int(cars.filter(model_variant=pmv["model_variant"]).aggregate(Avg('production_year'))['production_year__avg']))
        pmv_dict[f'{pmv["model_variant"]}'].append(int(cars.filter(model_variant=pmv["model_variant"]).aggregate(Avg('engine_power'))['engine_power__avg']))
        pmv_dict[f'{pmv["model_variant"]}'].append('{:.2f}'.format(cars.filter(model_variant=pmv["model_variant"]).aggregate(Avg('engine_capacity'))['engine_capacity__avg']))

    context = {
        'cars_amount': cars_amount,
        'average_price': average_price,
        'average_mileage': average_mileage,
        'average_production_year': average_production_year,
        'average_engine_power': average_engine_power,
        'average_engine_capacity': average_engine_capacity,
        'popular_model_variants': popular_model_variants,
        'pmv_dict': pmv_dict,
    }

    return render(request, 'car_prices_tool/results_demo.html', context)
