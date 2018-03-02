from django import forms
from .models import Profile, Mensagem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

class EditProfileForm(UserChangeForm):
	password = ReadOnlyPasswordHashField()
	class Meta:
		model = User
		fields = (
		'first_name',
		'last_name',
		'email',
		'password'
		)	
	def clean_email(self):		
		email = self.cleaned_data['email']
		usuario	= User.objects.filter(email=email)
		usuario = usuario.exclude(pk=self.instance.pk)
		if usuario.exists() == True:
			raise ValidationError("A user with that email already exists.")			

		if email == '':
			raise ValidationError("Email field is required.")
		
		return email

	def clean_first_name(self):
		first_name = self.cleaned_data['first_name']
		if first_name == '':
			raise ValidationError("First name field is required.")

		return first_name

	def clean_last_name(self):
		last_name = self.cleaned_data['last_name']
		if last_name == '':
			raise ValidationError("Last name field is required.")

		return last_name


class RegisterProfileForm(UserCreationForm):
	email = forms.EmailField(required=True)	
	
	class Meta:
		model = User
		fields = (
		'username',
		'email',
		'first_name',
		'last_name',
		'password1',
		'password2'
		)		

	def save(self, commit=True):
		user = super(RegisterProfileForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']

		if commit:
			user.save()

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists() == True:
			raise ValidationError("A user with that email already exists.")			
		return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('descricao', 'cidade', 'estado')

class MensagemFormView(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ('remetente',
        		  'assunto', 
        		  'mensagem',
        		  'dt_mensagem' 		  
        		  )

class NewMessage(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ('destinatario',
        		  'assunto', 
        		  'mensagem',        		  
        		  )