from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from account import forms
from  django.views.generic import FormView
from  . import models as user_models

class LoginView(FormView):
      template_name="login.html"
      form_class=forms.LoginForm

      def form_valid(self, form):
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user=authenticate(self.request,username=email, password=password)

            if user is not None:
                  login(self.request, user)
                  return redirect('testproject:post_list')
            return redirect('account:signup')


class SignUpView(FormView):
      template_name="signup.html"
      form_class=forms.SignUpform

      def form_valid(self,form):
            form.save()
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user=authenticate(self.request, username=email,password=password)
            if user is not None:
                  login(self.request, user)
            return redirect('account:signup')

# def signup_view(request):
#       if request.method == 'POST':
#             form = forms.SignUpform(request.POST) 
#             if form.is_valid():
#                   user = form.save()
#                   auth.login(request, user)
#                   return redirect('home')
#             return redirect('account:signup')
      
#       else:
#             form = forms.SignUpform
#             return render(request, 'signup.html', {'form' : form})