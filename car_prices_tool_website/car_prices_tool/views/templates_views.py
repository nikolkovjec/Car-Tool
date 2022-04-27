from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from car_prices_tool import all_jscharts
from car_prices_tool.forms import FreeSearchCarForm
from car_prices_tool.models import Car
from car_prices_tool.views.price_tools_views import results_demo


# Home is also a landing page.
def home(request):
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
            context = {
                'form': filled_form,
            }

            return render(request, 'car_prices_tool/home.html', context)
    else:
        context = {
            'form': form,
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


@login_required(login_url='login')
def api_documentation(request):
    return render(request, 'car_prices_tool/api_documentation.html')


# This view is for AJAX call.
def load_models(request):
    make = request.GET.get('make')
    models = Car.objects.filter(make=make).values('model').annotate(count=Count('make')).order_by('count').distinct().reverse()
    models_count = []
    for model in models:
        models_count.append(Car.objects.filter(model=model['model']).count())

    data = zip(models, models_count)

    return render(request, 'car_prices_tool/models_dropdown_list_options.html', {'data': data})
