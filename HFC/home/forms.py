from  django import forms
from .models import Reply, Member, Forum, Message, Post
from django.contrib.auth.models import User
from django.forms import ModelForm

class Comment(forms.Form):
	name = forms.CharField()
	message = forms.CharField(widget = forms.Textarea)

	def store_prayer_request(self):
		Reply.objects.create(name = self.name, reply = self.message, reply_type = 'Prayer Request')

	def store_suggestion(self):
		Reply.objects.create(name = self.name, reply = self.message, reply_type = 'Suggestion')

# I should have used modelform for this, but at the time of writting, i had to do it
# this way. It works but could have required less code and problem solving if i had
# used a model form.

class ResponseForm(forms.Form):
	name = forms.CharField(widget = forms.TextInput(attrs={'class':'validate', 'placeholder':'Optional'}), required = False)
	message = forms.CharField(widget = forms.Textarea(attrs={'class':'materialize-textarea'}))

	def store_prayer_request(self):
		Reply.objects.create(name = self.name, reply = self.message, reply_type = 'Prayer Request')

	def store_suggestion(self):
		Reply.objects.create(name = self.name, reply = self.message, reply_type = 'Suggestion')



class MembersForm(forms.Form):
	sex =(
		('null','Select Gender'),
		('male','Male'),
		('female','Female'))
	posts =(
		('null', 'Select Function'),
		('member','member'),
		('choir', 'choir'),
		('usher', 'usher'),
		('media','media'))
	firstname = forms.CharField(max_length = 50, widget = forms.TextInput(attrs={'class':'validate'}))
	lastname = forms.CharField(max_length = 50, widget = forms.TextInput(attrs={'class':'validate'}))
	email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'validate'}))
	phone = forms.CharField(max_length = 14, widget = forms.TextInput(attrs={'class':'validate'}))
	D_O_B = forms.DateField(widget = forms.TextInput(attrs={'class':'datepicker', 'placeholder':'Optional'}), required = False)
	gender = forms.CharField(max_length = 10, widget = forms.Select(attrs={'class':'validate'}, choices = sex))
	username = forms.CharField(max_length = 50, widget = forms.TextInput(attrs={'class':'validate'}))
	passwd = forms.CharField(max_length = 64, widget = forms.PasswordInput(attrs={'class':'validate','onfocus':'setInterval(validatePassword, 400)', 'id': 'confirm_passwd'}))
	function_held = forms.CharField(max_length = 15, widget = forms.Select(attrs = {'class': 'validate',}, choices = posts))
	path_to_pix = forms.ImageField(required = False)

	def register_member(self):
		Member.objects.create(firstname = self.firstname, lastname = self.lastname,\
		email = self.email, phone = self.phone, D_O_B = self.D_O_B, gender = self.gender,\
		username = self.username, passwd = self.passwd, \
		function_held = self.function_held, pix = self.path_to_pix)

		# creating their account
		#new_user = User.objects.create_user(self.email, self.email, self.passwd)

		# updating account details
		#new_user.first_name = self.firstname
		#new_user.last_name = self.lastname
		#new_user.acct_id = self.username
		#new_user.save()

class LoginForm(forms.Form):
	email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'validate'}))
	password = forms.CharField(max_length = 64, widget = forms.PasswordInput(attrs = {'class':'validate'}))

class PasswordRecoveryForm(forms.Form):
	password = forms.CharField(max_length = 64, widget = forms.PasswordInput(attrs = {'class':'validate', 'id':'confirm_passwd','onfocus':'setInterval(validatePassword, 400)',}))

class PasswordRecoveryMailForm(forms.Form):
	email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'validate'}))

class PasswordResetForm(forms.Form):
	email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'validate'}))
	password = forms.CharField(max_length = 64, widget = forms.PasswordInput(attrs = {'class':'validate', 'id':'confirm_passwd','onfocus':'setInterval(validatePassword, 400)',}))

class PasswordResetForm2(forms.Form):
	password = forms.CharField(max_length = 64, widget = forms.PasswordInput(attrs = {'class':'validate', 'id':'confirm_passwd','onfocus':'setInterval(validatePassword, 400)',}))

class SearchForm(forms.Form):
	search = forms.CharField(max_length = 200, widget = \
		forms.TextInput(attrs = {'class':'validate','type':'search',\
			'id':'search','placeholder':'Search here'}))

class UpdateProfileForm(forms.Form):
	posts =(
		('null', 'Select Function'),
		('member','member'),
		('choir', 'choir'),
		('usher', 'usher'),
		('media','media'))
	email = forms.EmailField(widget  = forms.EmailInput(attrs={'class':'validate'}))
	phone = forms.CharField(max_length = 14, widget = forms.TextInput(attrs={'class':'validate'}))
	username = forms.CharField(max_length = 50, widget = forms.TextInput(attrs={'class':'validate'}))
	function_held = forms.CharField(max_length = 15, widget = forms.Select(attrs = {'class': 'validate',}, choices = posts))
	path_to_pix = forms.ImageField(required = False)

class ForumForm(ModelForm):
	class Meta:
		forum_typ = (
		('null','Forum Type'),
		('PUBLIC','public'),
		('PRIVATE','private'))
		model = Forum
		fields = '__all__'
		widgets = {
		'forum_name': forms.TextInput(attrs = {'class': 'validate'}),
		'forum_typ': forms.Select(attrs = {'class':'validate'}, choices = forum_typ),
		'forum_description': forms.Textarea(attrs = {'class':'materialize-textarea'})
		}

class MessageForm(ModelForm):
	class Meta:
		model = Message
		fields = '__all__'
		widgets = {
		'posted_by': forms.TextInput(attrs = {'class': 'validate hide', 'id':'posted_by'}),
		'content': forms.Textarea(attrs = {'class':'materialize-textarea', 'placeholder':'Please type in your message here...','id':'content',\
			'autofocus':'autofocus'})
		}

class PostForm(ModelForm):
	class Meta:
		model = Post
		fields = '__all__'
		widgets = {
		'text': forms.TextInput(attrs = {'class': 'validate', 'id':'text', 'placeholder':'Write some post here', 'autofocus':'autofocus'})
		}
