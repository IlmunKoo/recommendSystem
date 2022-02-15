from django import forms
from . import models

class LoginForm(forms.Form):
  email=forms.EmailField(widget=forms.EmailInput({'placeholder': 'Email'}))
  password=forms.CharField(widget=forms.PasswordInput({'placeholder':'Password'}))

  def clean(self):
    email=self.cleaned_data.get('email')
    password=self.cleaned_data.get('password')

    try:
      user=models.User.objects.get(email=email)
      if user.check_password(password):
        return self.cleaned_data
      else:
        self.add_error('password', forms.ValidationError('password is wrong'))

    except models.User.DoesNotExist:
      self.add_error('email', forms.ValidationError('User does not exist'))

class SignUpform(forms.ModelForm):
  class Meta:
    model=models.User
    fields=('email','password')
    widgets={
      'email':forms.EmailInput(attrs={'placeholder':'Email'}),
      'password':forms.PasswordInput(attrs={'placeholder':'Password'})
    }

    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))

  def clean_email(self):
    email=self.cleaned_data.get('email')
    try:
      models.User.objects.get(email=email)
      raise forms.ValidationError(
        'this email is already exist'
      )
    except models.User.DoesNotExist:
      return email

  def clean_password(self):
        password=self.cleaned_data.get('password')
        return password

  def save(self, *args, **kwargs):
        user=super().save(commit=False)
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        user.username=email
        user.set_password(password)
        user.save()




        
