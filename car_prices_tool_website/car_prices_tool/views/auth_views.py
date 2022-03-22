from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUpView, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return view

    def form_invalid(self, form):
        if User.objects.filter(username=self.request.POST['username']):
            context = {
                'form': UserCreationForm(),
                'error': 'This username is already taken.'
            }
        elif self.request.POST['password1'] != self.request.POST['password2']:
            context = {
                'form': UserCreationForm(),
                'error': 'Passwords do not match.'
            }
        else:
            context = {
                'form': UserCreationForm(),
                'error': 'Please make sure that your password have at least 8 characters and '
                         'that it is not too easy or too common. Your password also cannot be '
                         'entirely numeric and can not be too similar to your username.'
            }

        return render(self.request, 'registration/signup.html', context)
