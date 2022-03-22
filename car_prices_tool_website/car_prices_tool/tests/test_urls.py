from django.urls import reverse, resolve


class TestUrls:
    def test_home_url(self):
        path = reverse('home')
        assert resolve(path).view_name == 'home'

    def test_about_url(self):
        path = reverse('about')
        assert resolve(path).view_name == 'about'

    def test_features_url(self):
        path = reverse('features')
        assert resolve(path).view_name == 'features'

    def test_pricing_url(self):
        path = reverse('pricing')
        assert resolve(path).view_name == 'pricing'

    def test_search_url(self):
        path = reverse('search')
        assert resolve(path).view_name == 'search'

    def test_results_url(self):
        path = reverse('results')
        assert resolve(path).view_name == 'results'

    def test_no_results_url(self):
        path = reverse('no_results')
        assert resolve(path).view_name == 'no_results'

    def test_go_premium_url(self):
        path = reverse('go_premium')
        assert resolve(path).view_name == 'go_premium'

    def test_go_api_pro_url(self):
        path = reverse('go_api_pro')
        assert resolve(path).view_name == 'go_api_pro'

    def test_signup_url(self):
        path = reverse('signup')
        assert resolve(path).view_name == 'signup'

    def test_login_url(self):
        path = reverse('login')
        assert resolve(path).view_name == 'login'

    def test_logout_url(self):
        path = reverse('logout')
        assert resolve(path).view_name == 'logout'

    def test_ajax_load_models_url(self):
        path = reverse('ajax_load_models')
        assert resolve(path).view_name == 'ajax_load_models'
