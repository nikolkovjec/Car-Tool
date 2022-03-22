from datetime import date

from .models import UserPremiumRank, UserSearchQuery


# Used for navbar.
def add_variable_to_context(request):
    if request.user.is_authenticated:
        try:
            user_rank_name = UserPremiumRank.objects.filter(user=request.user).values('rank').get()
        except UserPremiumRank.DoesNotExist:
            user_rank_name = {}

        if user_rank_name.get('rank') == 'Premium':
            user_rank_name = 'Premium'
        elif user_rank_name.get('rank') == 'APIPRO':
            user_rank_name = 'API Pro'
        if not user_rank_name:
            user_rank_name = 'Free'

        today = date.today()
        last_user_searches = UserSearchQuery.objects.filter(user=request.user, date__year=today.year, date__month=today.month, date__day=today.day).count()

        context = {
            'user_rank_name': user_rank_name,
            'last_user_searches': last_user_searches
        }

        return context
    else:
        return {}
