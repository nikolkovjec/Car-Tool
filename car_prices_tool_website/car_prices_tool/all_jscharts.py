from car_prices_tool.models import Car, CarMake
from django.db.models import Count, Avg

charts_base_colors = ["#25CCF7", "#FD7272", "#54a0ff", "#00d2d3", "#01a3a4"
                                                                  "#1abc9c", "#2ecc71", "#3498db", "#9b59b6", "#34495e",
                      "#16a085", "#27ae60", "#2980b9", "#8e44ad", "#2c3e50",
                      "#f1c40f", "#e67e22", "#e74c3c", "#ecf0f1", "#95a5a6",
                      "#f39c12", "#d35400", "#c0392b", "#bdc3c7", "#7f8c8d",
                      "#55efc4", "#81ecec", "#74b9ff", "#a29bfe", "#dfe6e9",
                      "#00b894", "#00cec9", "#0984e3", "#6c5ce7", "#ffeaa7",
                      "#fab1a0", "#ff7675", "#fd79a8", "#fdcb6e", "#e17055",
                      "#d63031", "#feca57", "#5f27cd", "#54a0ff"]

charts_backgroung_colors = ["rgba(255, 99, 132, 0.5)", "rgba(255, 159, 64, 0.5)", "rgba(255, 205, 86, 0.5)",
                            "rgba(75, 192, 192, 0.5)", "rgba(54, 162, 235, 0.5)", "rgba(153, 102, 255, 0.5)",
                            "rgba(201, 203, 207, 0.5)", "rgba(255, 99, 132, 0.5)", "rgba(255, 159, 64, 0.5)",
                            "rgba(255, 205, 86, 0.5)",
                            "rgba(75, 192, 192, 0.5)", "rgba(54, 162, 235, 0.5)", "rgba(153, 102, 255, 0.5)",
                            "rgba(201, 203, 207, 0.5)"]

charts_border_colors = ["rgb(255, 99, 132)", "rgb(255,159,64)", "rgb(255, 205, 86)", "rgb(75, 192, 192)",
                        "rgb(54, 162, 235)", "rgb(153, 102, 255)", "rgb(201, 203, 207)", "rgb(255, 99, 132)",
                        "rgb(255,159,64)", "rgb(255, 205, 86)", "rgb(75, 192, 192)",
                        "rgb(54, 162, 235)", "rgb(153, 102, 255)", "rgb(201, 203, 207)"]


def home_popularmakes_barchart():
    make_choices = []
    makes = Car.objects.values('make').annotate(count=Count('make')).order_by('count').reverse()[:15]

    for make in makes:
        make_choices.append((make["make"]))

    make_amount = []
    for make in makes:
        make_amount.append(Car.objects.filter(make=make["make"]).count())

    context = {
        'labels': make_choices,
        'data': make_amount,
        'charts_backgroung_colors': charts_backgroung_colors,
        'charts_border_colors': charts_border_colors,
        'charts_base_colors': charts_base_colors
    }

    return context


def home_popularproductionyears_piechart():
    popular_years = []
    years = Car.objects.values('production_year').annotate(count=Count('production_year')).order_by('count').reverse()[
            :10]

    for year in years:
        popular_years.append((year["production_year"]))

    popular_years_amount = []
    for year in years:
        popular_years_amount.append(Car.objects.filter(production_year=year["production_year"]).count())

    context = {
        'labels': popular_years,
        'data': popular_years_amount,
        'charts_backgroung_colors': charts_backgroung_colors,
        'charts_border_colors': charts_border_colors,
        'charts_base_colors': charts_base_colors
    }

    return context


def home_average_cars_used_info_radarchart():
    makes = Car.objects.values('make').annotate(count=Count('make')).order_by('count').reverse()[:8]

    average_cars_used_labels = []
    average_cars_used_price_list = []
    average_cars_used_mileage_list = []
    average_cars_used_enginepower_list = []
    average_cars_used_enginecapacity_list = []

    for make in makes:
        average_cars_used_labels.append(make["make"])
        average_price = Car.objects.filter(make=make["make"]).filter(state='Used').aggregate(Avg('price'))
        average_cars_used_price_list.append(int(average_price['price__avg']))
        average_mileage = Car.objects.filter(make=make["make"]).filter(state='Used').aggregate(Avg('mileage'))
        average_cars_used_mileage_list.append(int(average_mileage['mileage__avg']))
        average_engine_power = Car.objects.filter(make=make["make"]).filter(state='Used').aggregate(Avg('engine_power'))
        average_cars_used_enginepower_list.append(int(average_engine_power['engine_power__avg']))
        average_engine_capacity = Car.objects.filter(make=make["make"]).filter(state='Used').aggregate(Avg('engine_capacity'))
        average_cars_used_enginecapacity_list.append('{:.2f}'.format(average_engine_capacity['engine_capacity__avg']))

    context = {
        'data_price': average_cars_used_price_list,
        'data_mileage': average_cars_used_mileage_list,
        'data_enginepower': average_cars_used_enginepower_list,
        'data_enginecapacity': average_cars_used_enginecapacity_list,
        'labels': average_cars_used_labels,
        'charts_backgroung_colors': charts_backgroung_colors,
        'charts_border_colors': charts_border_colors,
        'charts_base_colors': charts_base_colors
    }

    return context
