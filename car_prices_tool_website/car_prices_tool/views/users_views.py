from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.authtoken.models import Token

from car_prices_tool.models import UserPremiumRank


@login_required(login_url='login')
def go_premium(request):
    if request.method == 'GET':
        try:
            user_rank_name = UserPremiumRank.objects.filter(user=request.user).values('rank').get()
        except UserPremiumRank.DoesNotExist:
            user_rank_name = {}

        if user_rank_name.get('rank') == 'Premium':
            context = {
                'message': 'You already have Premium account. Thank you!'
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


@login_required(login_url='login')
def go_api_pro(request):
    if request.method == 'GET':
        try:
            user_rank_name = UserPremiumRank.objects.filter(user=request.user).values('rank').get()
        except UserPremiumRank.DoesNotExist:
            user_rank_name = {}

        if user_rank_name.get('rank') == 'APIPRO':
            token = Token.objects.get(user=request.user)

            context = {
                'message': 'You already have API Pro account. Thank you!',
                'token': str(token)
            }

            return render(request, 'car_prices_tool/go_api_pro.html', context)
        else:
            return render(request, 'car_prices_tool/go_api_pro.html')
    else:
        UserPremiumRank.objects.filter(user=request.user).all().delete()
        get_api_pro = UserPremiumRank(user=request.user, rank='APIPRO')
        get_api_pro.save()

        token = Token.objects.create(user=request.user)

        context = {
            'message': 'Thank you very much for supporting our website! Enjoy your API Pro account!',
            'token': str(token)
        }

        return render(request, 'car_prices_tool/go_api_pro.html', context)
