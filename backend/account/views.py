from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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
            return super().form_vaild(form)

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
            super(SignUpView,self).form_valid(form)