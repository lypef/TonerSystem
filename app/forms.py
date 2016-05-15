from django import forms

class LoginForm (forms.Forms):
	username = forms.charfield()
	password = charfield(widget=forms.passwordInput())
