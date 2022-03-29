from datetime import date

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser

from car_prices_tool.models import UserPremiumRank, UserSearchQuery, Car
from .serializers import CarSerializer


class TokenAuthSupportQueryString(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support querystring authentication
    in the form of "http://www.example.com/?auth_token=<token_key>"
    """
    def authenticate(self, request):
        # Check if 'token_auth' is in the request query params.
        # Give precedence to 'Authorization' header.
        if 'auth_token' in request.query_params and 'HTTP_AUTHORIZATION' not in request.META:
            return self.authenticate_credentials(request.query_params.get('auth_token'))
        else:
            return super(TokenAuthSupportQueryString, self).authenticate(request)


@csrf_exempt
def sign_up_user(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(username=data['username'], password=data['password'])
            user.save()

            context = {
                'message': 'Thank you for registering!'
            }

            return JsonResponse(context, status=201)
        except IntegrityError:
            context = {
                'error': 'This username is already taken. Please choose another one.'
            }

            return JsonResponse(context, status=400)


@csrf_exempt
def get_token(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            context = {
                'error': 'Wrong password or user.'
            }

            return JsonResponse(context)
        else:
            # Make sure that user have correct rank to get token.
            try:
                user_rank = UserPremiumRank.objects.filter(user=user).values('rank').get()
            except UserPremiumRank.DoesNotExist:
                user_rank = {}

            if user_rank.get('rank') == 'APIPRO':
                try:
                    token = Token.objects.get(user=user)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)

                context = {
                    'token': str(token)
                }

                return JsonResponse(context, status=200)
            else:
                context = {
                    'error': 'You need rank API Pro to get your own API Key / Token!'
                }

                raise ValidationError(detail=context)


class CarsResults(generics.ListAPIView):
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthSupportQueryString,)

    def get_queryset(self):
        user = self.request.user

        make = self.request.query_params.get('make')
        state = self.request.query_params.get('state')
        model = self.request.query_params.get('model')
        offer_type = self.request.query_params.get('offer_type')
        mileage_less_more = self.request.query_params.get('mileage_less_more')
        mileage = self.request.query_params.get('mileage')
        production_year_less_more = self.request.query_params.get('production_year_less_more')
        production_year = self.request.query_params.get('production_year')
        price_less_more = self.request.query_params.get('price_less_more')
        price = self.request.query_params.get('price')
        price_currency = self.request.query_params.get('price_currency')
        engine_capacity_less_more = self.request.query_params.get('engine_capacity_less_more')
        engine_capacity = self.request.query_params.get('engine_capacity')
        engine_power_less_more = self.request.query_params.get('engine_power_less_more')
        engine_power = self.request.query_params.get('engine_power')

        try:
            user_rank = UserPremiumRank.objects.filter(user=user).values('rank').get()
        except UserPremiumRank.DoesNotExist:
            user_rank = {}

        today = date.today()
        last_user_searches = UserSearchQuery.objects.filter(user=user, date__year=today.year,
                                                            date__month=today.month, date__day=today.day).count()

        filters = {}

        if user_rank.get('rank') == 'APIPRO':
            if last_user_searches < 500:
                new_search = UserSearchQuery(user=user, search_parameters=filters)
                new_search.save()

                filters = {}

                if make:
                    filters['make'] = make

                if model:
                    filters['model'] = model

                if state:
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
                        filters['engine_capacity__lte'] = engine_capacity
                    if engine_capacity_less_more == 'engine_capacity_more_than':
                        filters['engine_capacity__gte'] = engine_capacity
                    if engine_capacity_less_more == 'engine_capacity_equal':
                        filters['engine_capacity'] = engine_capacity

                if engine_power:
                    if engine_power_less_more == 'engine_power_less_than':
                        filters['engine_power__lte'] = engine_power
                    if engine_power_less_more == 'engine_power_more_than':
                        filters['engine_power__gte'] = engine_power
                    if engine_power_less_more == 'engine_power_equal':
                        filters['engine_power'] = engine_power

                return Car.objects.filter(**filters)[:500]
            else:
                context = {
                    'error': 'No searches left for today!'
                }

                raise ValidationError(detail=context)
        else:
            context = {
                'error': 'Sorry, it looks like you do not have API Pro account.'
            }

            raise ValidationError(detail=context)


class CarCreate(generics.ListCreateAPIView):
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Car.objects.order_by('-date_scraped')[:10]

    def perform_create(self, serializer):
        serializer.save()


class CarRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Car.objects
