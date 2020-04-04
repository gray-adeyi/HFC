from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import View, generic
from django.views.generic.edit import  FormView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Page, Download, Article, Member, ForumDetail, Forum,\
Message, Post, Notification, Tool, Developer, ChurchOfficial, Contributor,\
ChurchDetail
from .forms import MembersForm, ResponseForm, Comment,\
LoginForm, PasswordRecoveryMailForm, SearchForm, PasswordRecoveryForm\
, PasswordResetForm, PasswordResetForm2, UpdateProfileForm, ForumForm,\
MessageForm, PostForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import math, random, os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import datetime as dt

# Create your views here.
class Index(View):
	def get(self, request):
		temp = 'home/index.html'
		# I'm a bit nervous i have to something differnt
		# below i had to read some content of the page
		# which i had already stored in text format,
		# xml would have been better, but i still have
		# limted knowledge on how to use python for that
		# and there is little time on my side 'cus' i ought
		# to have submitted this project in a long time.
		# enough of the story for now. the big question is why
		# i had to do this because at my development phase,
		# the database i used to start the project was sqlite
		# and i'm hoping to switch to mysql database at pro-
		# duction phase. these files are essential for the
		# proper projection of the index pageg of this site.

		# Important notice, all the .open, .read and .close
		# could have been simplified
		welcome_header = open('./home/Notes/welcome_title.txt', 'r+')
		welcome_body = open('./home/Notes/welcome_body.txt', 'r+')
		mission_header = open('./home/Notes/mission_title.txt', 'r+')
		mission_body = open('./home/Notes/mission_body.txt', 'r+')
		vision_header = open('./home/Notes/vision_title.txt', 'r+')
		vision_body = open('./home/Notes/vision_body.txt', 'r+')
		core_values_header = open('./home/Notes/core_values_title.txt', 'r+')
		core_values_preamble = open('./home/Notes/core_values_preamble.txt', 'r+')
		core_values_l1 = open('./home/Notes/core_values_l1.txt', 'r+')
		core_values_l2 = open('./home/Notes/core_values_l2.txt', 'r+')
		core_values_l3 = open('./home/Notes/core_values_l3.txt', 'r+')
		core_values_l4 = open('./home/Notes/core_values_l4.txt', 'r+')
		core_values_l5 = open('./home/Notes/core_values_l5.txt', 'r+')

		# the content of the text files opened above are stored
		# in the same variable that opened them.
		a = welcome_header.read()
		b = welcome_body.read()
		c = mission_header.read()
		d = mission_body.read()
		e = vision_header.read()
		f = vision_body.read()
		g  = core_values_header.read()
		h = core_values_preamble.read()
		i = core_values_l1.read()
		j = core_values_l2.read()
		k = core_values_l3.read()
		l = core_values_l4.read()
		m = core_values_l5.read()

		# all the retrieved content are stored in a dictionary
		content = {'welcome_header':a, 'welcome_body':b,\
		'mission_header':c, 'mission_body':d,\
		'vision_header':e, 'vision_body':f,\
		'core_values_header':g, 'core_values_preamble':\
		h, 'core_values_l1':i,\
		'core_values_l2':j, 'core_values_l3':k,\
		'core_values_l4':l, 'core_values_l5': m}

		# all the opened text files are closed
		welcome_header.close(); welcome_body.close()
		mission_header.close(); mission_body.close()
		vision_header.close(); vision_body.close()
		core_values_header.close(); core_values_preamble.close()
		core_values_l1.close(); core_values_l2.close()
		core_values_l3.close(); core_values_l4.close()
		core_values_l5.close()

		content['tools'] = Tool.objects.all()
		content['developers'] = Developer.objects.all()
		content['contributors'] = Contributor.objects.all()
		print("here are the contents")
		print(content)

		return render(request, temp, content) # i removed this  {"picture" : picture}

class AltIndex(View):
	'''This is an alternative view to the
	index page. it has better css'''
	def get(self,request):
		'''this method handles get requsts for
		the website'''
		news_list = Article.objects.filter(pub_type = 'N').order_by('-pub_date_et_time')[:4]
		church_detail = ChurchDetail.objects.get()
		template = 'home/imperial/index.html'
		context = {
		"church_detail": church_detail,
		"news_list": news_list,
		}
		context['tools'] = Tool.objects.all()
		context['developers'] = Developer.objects.all()
		context['contributors'] = Contributor.objects.all()
		return render(request,template, context)



class Suggestions(View):
	def post(self, request):
		form = Comment(request.POST)

	def get(self, request):
		form = Comment()
		return render(request, 'home/suggestions.html', {'form':form})

def forms_view(request, form_type):
	template = "home/forms.html"
	if(request.method == "POST"):
		if(form_type == "members_account"):
			membersform = MembersForm(request.POST, request.FILES)
			if(membersform.is_valid()):
				membersform.firstname = membersform.cleaned_data['firstname']
				membersform.lastname = membersform.cleaned_data['lastname']
				membersform.email = membersform.cleaned_data['email']
				membersform.phone = membersform.cleaned_data['phone']
				membersform.D_O_B = membersform.cleaned_data['D_O_B']
				membersform.gender = membersform.cleaned_data['gender']
				membersform.username = membersform.cleaned_data['username']
				membersform.passwd = membersform.cleaned_data['passwd']
				membersform.function_held = membersform.cleaned_data['function_held']
				if(request.FILES):
					membersform.path_to_pix = request.FILES['path_to_pix']
				else:
					members_avatar = '/home/static/home/images/members_image/gbenga.jpg'
					membersform.path_to_pix = members_avatar
				membersform.register_member()

				# code to send email link to new user
				mail_type = 'new_signup'
				to_email = [membersform.cleaned_data['email']]
				from_email = '<signup@happyfamilychurch.com>'
				recipients_email = membersform.cleaned_data['email']
				recipients_name = membersform.cleaned_data['firstname']
				template = 'home/email.html'
				subject = 'Activate my HFC account'
				html_content = render_to_string(template,{'mail_type':mail_type,'recipients_name':\
				recipients_name,'recipients_email':recipients_email})
				new_signup_msg = EmailMessage(subject, html_content, from_email, to_email)
				new_signup_msg.content_subtype = "html"  # Main content is now text/html
				new_signup_msg.send()
				return HttpResponseRedirect(reverse('home:success',args = ('members_account',)))
			else:
				membersform = MembersForm()
			return render(request, template,{'membersform': membersform})
		elif(form_type == "suggestions"):
			suggestionform = ResponseForm(request.POST)
			if(suggestionform.is_valid()): #validate and store in members database
				suggestionform.name = suggestionform.cleaned_data['name']
				if(suggestionform.name == ''): suggestionform.name = 'Anonymous'
				suggestionform.message = suggestionform.cleaned_data['message']
				suggestionform.store_suggestion()
				return HttpResponseRedirect(reverse('home:success',args = ('suggestions',))) # modifiy to success url
			else:
				suggestionform = ResponseForm()
			return render(request, template,{'suggestionform': suggestionform})
		elif(form_type == "prayer_requests"):
			prayerform = ResponseForm(request.POST)
			if(prayerform.is_valid()): #validate and store in members database
				prayerform.name = prayerform.cleaned_data['name']
				if(prayerform.name == ''): prayerform.name = 'Anonymous'
				prayerform.message = prayerform.cleaned_data['message']
				prayerform.store_prayer_request()
				return HttpResponseRedirect(reverse('home:success',args = ('prayer_requests',))) # modifiy to success url
			else:
				membersform = ResponseForm()
			return render(request, template,{'prayerform': prayerform})
		else:
			pass
	elif(request.method == "GET"):
		first_value = {'key': 'value'}
		if(form_type == "members_account"):
			membersform = MembersForm(initial = first_value)
			return render(request, template, {'membersform': membersform})
		elif(form_type == 'suggestions'):
			suggestionform = ResponseForm(initial = first_value)
			return render(request, template, {'suggestionform': suggestionform})
		elif(form_type == 'prayer_requests'):
			prayerform = ResponseForm(initial = first_value)
			return render(request, template, {'prayerform': prayerform})
		else:
			pass
	else:
		return HttpResponseRedirect(reverse('home:index'))

class ActivateAccount(View):
	'''This is the view that activates
	the account after sign up'''
	def get(self,request, *args, **kwargs):
		self.store = kwargs
		## activation of account.
		add_user = Member.objects.get(email=self.store['mail'])
		## add the the new member to the User model
		# creating their account
		new_user = User.objects.create_user(username = add_user.email,\
		email = add_user.email, password = add_user.passwd)

		# updating account details
		new_user.first_name = add_user.firstname
		new_user.last_name = add_user.lastname
		new_user.acct_id = add_user.username
		new_user.save()

		render_type = 'success_account_activation'
		template = 'home/success.html'
		return render(request,template,{'render_type':render_type})

def get_random_number(max_range):
	'''This function helps to create random
	numbers that are used for the random
	gif images displayed in the Success view'''

	a = math.ceil(random.random()*max_range)
	return a

class Success(View):
	'''This view provides all the pages for
	display on successfully completing an action
	on the site'''

	template = 'home/success.html'
	def get(self, request, *args, **kwargs):
		store = kwargs
		if(store['type'] == 'members_account'):
			title = 'Sucessful Member Registration'
			gif = self.random_gifs()
			render_type = 'members_account'
			return render(request, self.template, {'title':title, 'gif':gif, 'render_type': render_type})
		elif(store['type'] == 'prayer_requests'):
			title = 'Prayer Request Sucessfully Sent'
			gif = self.random_gifs()
			render_type = 'prayer_requests'
			return render(request, self.template, {'title':title, 'gif':gif, 'render_type': render_type})
		elif(store['type'] == 'suggestions'):
			title = 'Prayer Request Sucessfully Sent'
			gif = self.random_gifs()
			render_type = 'suggestions'
			return render(request, self.template, {'title':title, 'gif':gif, 'render_type': render_type})

	def random_gifs(self):
		random_gif_no = get_random_number(3)
		if(random_gif_no == 1):
			return 'home/images/raw.gif'
		elif(random_gif_no == 2):
			return 'home/images/giphy.webp'
		elif(random_gif_no == 3):
			return 'home/images/giphy1.webp'
		else:
			return

class Login(View):
	'''This view provides the user logging in
	facility to the site'''

	def get(self, request):
		template = 'home/sign_in.html'
		first_value = {'key':'value'}
		sign_in = LoginForm(initial = first_value)
		return render(request, template,{'sign_in':sign_in})

	def post(self,request):
		login_details = LoginForm(request.POST)
		if(login_details.is_valid()):
			login_username = login_details.cleaned_data['email']
			login_passwd = login_details.cleaned_data['password']
			verify_user = authenticate(request,username = login_username,\
				password = login_passwd)
			if verify_user is not None:
				login(request, verify_user)
				return HttpResponseRedirect(reverse("home:member_account",\
					kwargs = {"mail":login_username}))

			else:
				template = 'home/sign_in.html'
				error_msg = '''Invalid Email or password, please log in with a valid
				account detail or reset your password if you\'ve forgotten it.'''
				first_value = {'email':login_username}
				sign_in = LoginForm(initial = first_value)
				return render(request, template,{'sign_in':sign_in,'error_msg':error_msg})

class PasswordRecovery(View):
	'''This view is responsible for user password
	recovery as the name implies'''

	def get(self, request):
		template = 'home/forgotten_passwd_email.html'
		first_value = {'key':'value'}
		password_recovery_email = PasswordRecoveryMailForm(initial = first_value)
		return render(request, template, {'password_recovery_email':password_recovery_email})

	def post(self, request):
		password_recovery_email = PasswordRecoveryMailForm(request.POST)
		if(password_recovery_email.is_valid()):
			password_recovery_email.email = password_recovery_email.cleaned_data['email']
			a = password_recovery_email.email
			members_details = Member.objects.get(email=a)
		# code to send email link to new user
		mail_type = 'password_reset'
		to_email = [a]
		from_email = '<passwordrecovery@happyfamilychurch.com>'
		templateE = 'home/forgotten_passwd.html'
		subject = 'Reset HFC account password'
		first_value = {'key':'value'}
		new_password = PasswordRecoveryForm(initial = first_value)
		html_content = render_to_string(templateE,{'members_details':\
		members_details,'mail_type':mail_type})
		passwd_recovery_msg = EmailMessage(subject, html_content, from_email, to_email)
		passwd_recovery_msg.content_subtype = "html"  # Main content is now text/html
		passwd_recovery_msg.send()
		template = 'home/email.html'
		return render(request,template,{'members_details':\
		members_details})

class ResetPassword(View):
	def get(self, request,*args,**kwargs):
		self.kwargs = kwargs
		theMail = self.kwargs['mail']
		members_details = Member.objects.get(email = theMail)
		template = 'home/forgotten_passwd.html'
		first_value = {'key':'value'}
		password_reset = PasswordResetForm(initial = first_value)
		return render(request,template,{'password_reset':password_reset,\
		'theMail':theMail,'members_details':members_details})

	def post(self, request,*args,**kwargs):
		if(request.POST):
			self.kwargs = kwargs
			new_passwd = PasswordResetForm2(request.POST)
			if(new_passwd.is_valid()):
				store_passwd_email = self.kwargs['mail']
				store_passwd = new_passwd.cleaned_data['password']

				Query_member = Member.objects.get(email=store_passwd_email)
				Query_member.passwd = store_passwd
				Query_member.save()

				Query_member_s = User.objects.get(username = store_passwd_email)
				Query_member_s.set_password(store_passwd)
				Query_member_s.save()
				# i am to update the password for the User model
				# for the Query member linked to the User model
				render_type = 'success_password_reset'
				template = 'home/success.html'
				return render(request,template,{'render_type':render_type})
			else:
				self.mail = self.kwargs['mail']
				return HttpResponseRedirect(reverse('home:change_passwd',mail=self.mail))

class DownloadsView(View):
	def get(self, request, *args, **kwargs):
		if(kwargs['type'] == 'music'):
			template = 'home/articles_et_downloads_main.html'
			search = SearchForm()
			music_list = Download.objects.filter(filetype = 'M').order_by('-upload_date')
			paginator = Paginator(music_list,10)
			page = request.GET.get('page')
			music_l = paginator.get_page(page)
			return render(request, template, {'music_list':music_l,'search':search})
		elif(kwargs['type'] == 'videos'):
			template = 'home/articles_et_downloads_main.html'
			search = SearchForm()
			video_list = Download.objects.filter(filetype = 'V').order_by('-upload_date')
			paginator = Paginator(video_list,10)
			page = request.GET.get('page')
			video_l = paginator.get_page(page)
			return render(request, template, {'video_list':video_l,'search':search})
		elif(kwargs['type'] == 'picture'):
			template = 'home/articles_et_downloads_main.html'
			search = SearchForm()
			picture_list = Download.objects.filter(filetype = 'Pic').order_by('-upload_date')
			paginator = Paginator(picture_list,10)
			page = request.GET.get('page')
			picture_l = paginator.get_page(page)
			return render(request, template, {'picture_list':picture_l,'search':search})
		elif(kwargs['type'] == 'pdf'):
			template = 'home/articles_et_downloads_main.html'
			search = SearchForm()
			pdf_list = Download.objects.filter(filetype = 'Pdf').order_by('-upload_date')
			paginator = Paginator(pdf_list,10)
			page = request.GET.get('page')
			pdf_l = paginator.get_page(page)
			return render(request, template, {'pdf_list':pdf_l,'search':search})
		elif(kwargs['type'] == 'others'):
			template = 'home/articles_et_downloads_main.html'
			search = SearchForm()
			other_list = Download.objects.filter(filetype = 'O').order_by('-upload_date')
			paginator = Paginator(other_list,10)
			page = request.GET.get('page')
			other_l = paginator.get_page(page)
			return render(request, template, {'other_list':other_l,'search':search})
		elif(kwargs['type'] == ''):
			return HttpResponseRedirect(reverse('home:index'))
		else:
			return HttpResponseRedirect(reverse('home:index'))
		return HttpResponseRedirect(reverse('home:index'))

	def post(self, request, *args, **kwargs):
		if(kwargs['type'] == 'music'):
			searchquery = SearchForm(request.POST)
			if(searchquery.is_valid()):
				query = searchquery.cleaned_data['search']
				result =  Download.objects.filter(filename__icontains = query).filter(filetype = 'M')
				result_count = result.count()
				if (result_count == 0):
					error_msg = 'Sorry no results were found!'
				music_list = result
				template = 'home/articles_et_downloads_main.html'
				search = SearchForm()
				return render(request, template, {'music_list':music_list,'search':search,'error_msg':error_msg})
		elif(kwargs['type'] == 'videos'):
			searchquery = SearchForm(request.POST)
			if(searchquery.is_valid()):
				query = searchquery.cleaned_data['search']
				result =  Download.objects.filter(filename__icontains = query).filter(filetype = 'V')
				result_count = result.count()
				if (result_count == 0):
					error_msg = 'Sorry no results were found!'
				video_list = result
				template = 'home/articles_et_downloads_main.html'
				search = SearchForm()
				return render(request, template, {'video_list':video_list,'search':search,'error_msg':error_msg})
		elif(kwargs['type'] == 'picture'):
			searchquery = SearchForm(request.POST)
			if(searchquery.is_valid()):
				query = searchquery.cleaned_data['search']
				result =  Download.objects.filter(filename__icontains = query).filter(filetype = 'Pic')
				result_count = result.count()
				if (result_count == 0):
					error_msg = 'Sorry no results were found!'
				picture_list = result
				template = 'home/articles_et_downloads_main.html'
				search = SearchForm()
				return render(request, template, {'picture_list':picture_list,'search':search,'error_msg':error_msg})
		elif(kwargs['type'] == 'pdf'):
			searchquery = SearchForm(request.POST)
			if(searchquery.is_valid()):
				query = searchquery.cleaned_data['search']
				result =  Download.objects.filter(filename__icontains = query).filter(filetype = 'Pdf')
				result_count = result.count()
				if (result_count == 0):
					error_msg = 'Sorry no results were found!'
				pdf_list = result
				template = 'home/articles_et_downloads_main.html'
				search = SearchForm()
				return render(request, template, {'pdf_list':pdf_list,'search':search,'error_msg':error_msg})
		elif(kwargs['type'] == 'others'):
			searchquery = SearchForm(request.POST)
			if(searchquery.is_valid()):
				query = searchquery.cleaned_data['search']
				result =  Download.objects.filter(filename__icontains = query).filter(filetype = 'O')
				result_count = result.count()
				if (result_count == 0):
					error_msg = 'Sorry no results were found!'
				other_list = result
				template = 'home/articles_et_downloads_main.html'
				search = SearchForm()
				return render(request, template, {'other_list':other_list,'search':search,'error_msg':error_msg})
		else:
			return HttpResponseRedirect(reverse('home:index'))

class OfficialDownloadsView(View):
	def get(self, request, *args, **kwargs):
		if(kwargs['type'] == 'music'):
			music_file = get_object_or_404(Download,filetype = 'M',filename = kwargs['filename'])
			search = SearchForm()
			template = 'home/downloads.html'
			return render(request, template, {'music_file':music_file,'search':search})
		elif(kwargs['type'] == 'videos'):
			video_file = get_object_or_404(Download,filetype = 'V',filename = kwargs['filename'])
			search = SearchForm()
			template = 'home/downloads.html'
			return render(request, template, {'video_file':video_file,'search':search})
		elif(kwargs['type'] == 'picture'):
			picture_file = get_object_or_404(Download,filetype = 'Pic',filename = kwargs['filename'])
			search = SearchForm()
			template = 'home/downloads.html'
			return render(request, template, {'picture_file':picture_file,'search':search})
		elif(kwargs['type'] == 'pdf'):
			pdf_file = get_object_or_404(Download,filetype = 'Pdf',filename = kwargs['filename'])
			search = SearchForm()
			template = 'home/downloads.html'
			return render(request, template, {'pdf_file':pdf_file,'search':search})
		elif(kwargs['type'] == 'other'):
			other_file = get_object_or_404(Download,filetype = 'O',filename = kwargs['filename'])
			search = SearchForm()
			template = 'home/downloads.html'
			return render(request, template, {'other_file':other_file,'search':search})
		elif(kwargs['type'] == ''):
			return HttpResponseRedirect(reverse('home:index'))
		else:
			return HttpResponseRedirect(reverse('home:index'))
		return HttpResponseRedirect(reverse('home:index'))

class ArticlesListView(View):
	def get(self, request, *args, **kwargs):
		if(kwargs['type'] == 'news'):
			template = 'home/articles_et_downloads_main.html'
			search = SearchForm()
			news_list = Article.objects.filter(pub_type = 'N').order_by('-pub_date_et_time')
			paginator = Paginator(news_list,10)
			page = request.GET.get('page')
			news_l = paginator.get_page(page)
			return render(request, template, {'news_list':news_l,'search':search})

		elif(kwargs['type'] == 'hab'):
			template = 'home/articles_et_downloads_main.html'
			search = SearchForm()
			hb_list = Article.objects.filter(pub_type = 'HB').order_by('-pub_date_et_time')
			paginator = Paginator(hb_list,10)
			page = request.GET.get('page')
			hb_l = paginator.get_page(page)
			return render(request, template, {'hb_llist':hb_l,'search':search})

		elif(kwargs['type'] == 'biblestudy'):
			template = 'home/articles_et_downloads_main.html'
			search = SearchForm()
			bstudy_list = Article.objects.filter(pub_type = 'B').order_by('-pub_date_et_time')
			paginator = Paginator(bstudy_list,10)
			page = request.GET.get('page')
			bstudy_l = paginator.get_page(page)
			return render(request, template, {'bstudy_list':bstudy_l,'search':search})

		elif(kwargs['type'] == 'others'):
			template = 'home/articles_et_downloads_main.html'
			search = SearchForm()
			otherA_list = Article.objects.filter(pub_type = 'O').order_by('-pub_date_et_time')
			paginator = Paginator(otherA_list,10)
			page = request.GET.get('page')
			otherA_l = paginator.get_page(page)
			return render(request, template, {'otherA_list':otherA_l,'search':search})

		elif(kwargs['type'] == ''):
			return HttpResponseRedirect(reverse('home:index'))
		else:
			return HttpResponseRedirect(reverse('home:index'))
		return HttpResponseRedirect(reverse('home:index'))

	def post(self, request, *args, **kwargs):
		if(kwargs['type'] == 'news'):
			searchquery = SearchForm(request.POST)
			if(searchquery.is_valid()):
				query = searchquery.cleaned_data['search']
				result =  Article.objects.filter(Q(publisher__icontains = query,pub_type = 'N') | Q(title__icontains = query,pub_type = 'N'))
				result_count = result.count()
				error_msg = None
				if(result_count == 0):
					error_msg = 'No results were found!'
				news_list = result
				template = 'home/articles_et_downloads_main.html'
				search = SearchForm()
				return render(request, template, {'news_list':news_list, 'result_count':result_count,'search':search,'error_msg':error_msg})
		elif(kwargs['type'] == 'hab'):
			searchquery = SearchForm(request.POST)
			if(searchquery.is_valid()):
				query = searchquery.cleaned_data['search']
				result =  Article.objects.filter(Q(publisher__icontains = query,pub_type = 'HB') | Q(title__icontains = query,pub_type = 'HB'))
				result_count = result.count()
				error_msg = None
				if(result_count == 0):
					error_msg = 'No results were found!'
				hab_list = result
				template = 'home/articles_et_downloads_main.html'
				search = SearchForm()
				return render(request, template, {'hab_list':hab_list, 'result_count':result_count,'search':search,'error_msg':error_msg})
		elif(kwargs['type'] == 'biblestudy'):
			searchquery = SearchForm(request.POST)
			if(searchquery.is_valid()):
				query = searchquery.cleaned_data['search']
				result =  Article.objects.filter(Q(publisher__icontains = query, pub_type = 'B') | Q(title__icontains = query, pub_type = 'B'))
				result_count = result.count()
				error_msg = None
				if(result_count == 0):
					error_msg = 'No results were found!'
				bstudy_list = result
				a = open("/home/jigani/debug1.txt", 'w+')
				a.write(str(result));a.write(str(result_count))
				a.close()
				template = 'home/articles_et_downloads_main.html'
				search = SearchForm()
				return render(request, template, {'bstudy_list':bstudy_list, 'result_count':result_count,'search':search,'error_msg':error_msg})
		elif(kwargs['type'] == 'others'):
			searchquery = SearchForm(request.POST)
			if(searchquery.is_valid()):
				query = searchquery.cleaned_data['search']
				result =  Article.objects.filter(Q(publisher__icontains = query, pub_type = 'O') | Q(title__icontains = query, pub_type = 'O'))
				result_count = result.count()
				error_msg = None
				if(result_count == 0):
					error_msg = 'No results were found!'
				otherA_list = result
				template = 'home/articles_et_downloads_main.html'
				search = SearchForm()
				return render(request, template, {'otherA_list':otherA_list, 'result_count':result_count,'search':search,'error_msg':error_msg})
		else:
			return HttpResponseRedirect(reverse('home:index'))

class ArticlesView(View):
	def get(self, request, *args, **kwargs):
		if(kwargs['type'] == 'news'):
			query = get_object_or_404(Article, title = kwargs['title'],pub_type = 'N')
			template = 'home/articles_main.html'
			return render(request, template, {'query': query})
		elif(kwargs['type'] == 'hab'):
			query = get_object_or_404(Article, title = kwargs['title'],pub_type = 'HB')
			template = 'home/articles_main.html'
			return render(request, template, {'query': query})
		elif(kwargs['type'] == 'biblestudy'):
			query = get_object_or_404(Article, title = kwargs['title'],pub_type = 'B')
			template = 'home/articles_main.html'
			return render(request, template, {'query': query})
		elif(kwargs['type'] == 'others'):
			query = get_object_or_404(Article, title = kwargs['title'],pub_type = 'O')
			template = 'home/articles_main.html'
			return render(request, template,{'query': query})
		elif(kwars['type'] == ''):
			return HttpResponseRedirect(reverse('home:index'))
		else:
			return HttpResponseRedirect(reverse('home:index'))
		return HttpResponseRedirect(reverse('home:index'))

class CommunityView(View):
	def get(self,request):
		# get all the latest contents from
		# other links like downloads and
		# articles
		self.music  = Download.objects.filter(filetype = 'M').order_by('-upload_date')[:3]
		self.video  = Download.objects.filter(filetype = 'V').order_by('-upload_date')[:3]
		self.picture  = Download.objects.filter(filetype = 'Pic').order_by('-upload_date')[:3]
		self.pdf  = Download.objects.filter(filetype = 'Pdf').order_by('-upload_date')[:3]
		self.otherD  = Download.objects.filter(filetype = 'O').order_by('-upload_date')[:3]
		self.news = Article.objects.filter(pub_type = 'N').order_by('-pub_date_et_time')[:3]
		self.history_bio = Article.objects.filter(pub_type = 'HB').order_by('-pub_date_et_time')[:3]
		self.bstudy = Article.objects.filter(pub_type = 'B').order_by('-pub_date_et_time')[:3]
		self.otherA = Article.objects.filter(pub_type = 'O').order_by('-pub_date_et_time')[:3]

		template = 'home/community.html'
		return render(request,template,{'music':self.music,'video':self.video \
			,'picture':self.picture,'pdf':self.pdf,'otherD':self.otherD, \
			'news':self.news, 'history_bio':self.history_bio, 'bstudy': \
			self.bstudy,'otherA': self.otherA})


class MemberAccountView(View):

	def __forumupdater__(self, useremail):
		self.useractiveforum = []
		self.useremail = useremail
		self.getallforum = Forum.objects.all()
		self.current_user = Member.objects.get(email = self.useremail)
		for forum in self.getallforum:
			if(self.current_user in forum.forum_members.all()):
				self.useractiveforum.append(forum)
		return self.useractiveforum


	def get(self, request,*args, **kwargs):
		if (request.user.is_authenticated):
			self.kwargs = kwargs
			self.useremail = self.kwargs['mail']
			if (request.user.username == self.useremail):
				members_count = Member.objects.all().count() - 1
				self.template = 'home/Member/membersindex.html'
				self.mail= self.kwargs['mail']
				self.member = Member.objects.get(email=self.mail)
				self.first_value = {'email':self.member.email,'phone':self.member.phone,'username':\
				self.member.username,'function_held': self.member.function_held,'path_to_pix':\
				self.member.pix}
				self.updateprofile = UpdateProfileForm(initial = self.first_value)
				first_values = {'posted_by':self.member}
				self.create_forum = ForumForm()
				self.post_form = PostForm(initial = first_values)
				self.activeforums = self.__forumupdater__(self.useremail)
				self.post = Post.objects.order_by('-upload_time')
				paginator = Paginator(self.post,20)
				page = request.GET.get('page')
				post_detail = paginator.get_page(page)
				# Update notification for members having their birthdays
				# on the day of the request of this view.
				self.all_members = Member.objects.all()
				current_date = dt.date.today()
				current_date_day = current_date.day
				current_date_month = current_date.month
				for one_member in self.all_members:
					if one_member.D_O_B is not None and one_member.D_O_B.day == current_date_day:
						if one_member.D_O_B.month == current_date_month:
							c1 = "%s has" % (one_member.firstname)
							if one_member.gender == "male" or one_member.gender == "m":
								c2 = " his birthday today"
								notification_content = c1 + c2
								birthday_notification = Notification(notifying = self.member, notification_content = notification_content)
								birthday_notification.save()
							elif one_member.gender == "female" or one_member.gender == "f":
								c2 = " her birthday today"
								notification_content = c1 + c2
								birthday_notification = Notification(notifying = self.member, notification_content = notification_content)
								birthday_notification.save()
							else:
								c2 = " birthday today"
								notification_content = c1 + c2
								birthday_notification = Notification(notifying = self.member, notification_content = notification_content)
								birthday_notification.save()
				notification_count = Notification.objects.filter(notifying = self.member)
				notification_count = notification_count.count()
				return render(request, self.template,{'member':self.member,'updateprofile':\
					self.updateprofile,'forum_form':self.create_forum,'active_forums':\
					self.activeforums,'post_form':self.post_form,'posts':post_detail,\
					'notification_count': notification_count,'members_count': members_count })
			else:
				return HttpResponseRedirect(reverse('home:index'))

		else:
			return HttpResponseRedirect(reverse('home:index'))

	def post(self, request,*args, **kwargs):
		if (request.user.is_authenticated):
			self.kwargs = kwargs
			self.useremail = self.kwargs['mail']
			self.member = Member.objects.get(email=self.useremail)
			self.first_value = {'email':self.member.email,'phone':self.member.phone,'username':\
				self.member.username,'function_held': self.member.function_held,'path_to_pix':\
				self.member.pix}
			self.updateprofile = UpdateProfileForm(initial = self.first_value)
			self.template = 'home/Member/membersindex.html'
			if (self.kwargs['post_for']):
				self.post_for = self.kwargs['post_for']
			if(request.user.username == self.useremail and self.post_for == 'create_forum'):
				forum_creator = ForumForm(request.POST, request.FILES)
				if(forum_creator.is_valid()):
					self.forum_cleaned = forum_creator.clean()
					self.forum = Forum(forum_name = self.forum_cleaned['forum_name'],\
						forum_logo = self.forum_cleaned['forum_logo'], forum_type = self.forum_cleaned['forum_type'],\
						forum_description = self.forum_cleaned['forum_description'],)
					self.source_forum = self.forum
					self.created_by = Member.objects.get(email = self.useremail).__str__()
					self.total_no_of_members = self.forum_cleaned['forum_members'].count()

					# save forum and forum details
					self.forum.save()
					print(self.forum_cleaned['forum_members'])
					self.forum.forum_members.set(self.forum_cleaned['forum_members'])
					# store forum details
					self.f = Forum.objects.get(forum_name = self.forum_cleaned['forum_name'],\
						forum_description = self.forum_cleaned['forum_description'])
					save_forum_details = ForumDetail(source_forum = self.f,\
						created_by = self.created_by,total_no_of_members = \
						self.total_no_of_members)
					save_forum_details.save()
					# Notify all members that they have been added to the new forum
					for member in self.f.forum_members.all():
						notifying = self.member
						notification_content = 'You have been added to a new forum, You are now a member of %s forum'%\
						self.f.forum_name
						new_notification = Notification(notifying = notifying, notification_content = notification_content)
						new_notification.save()
					template = 'home/success.html'
					the_member = Member.objects.get(email = self.useremail)
					the_forum_name = Forum.objects.get(forum_name = self.forum_cleaned['forum_name']).forum_name
					render_type = 'forum_creation'
					return render(request, template,{'render_type': render_type, 'the_forum_name':the_forum_name,\
						'member': the_member})
				else:
					return render(request, self.template,{'member':self.member,'updateprofile':\
					self.updateprofile,'forum_form': forum_creator})

			if (request.user.username == self.useremail and self.post_for == 'update_profile'):
				updater = UpdateProfileForm(request.POST, request.FILES)
				if(updater.is_valid()):
					updater.email = updater.cleaned_data['email']
					updater.phone = updater.cleaned_data['phone']
					updater.username = updater.cleaned_data['username']
					updater.function_held = updater.cleaned_data['function_held']
					if(request.FILES):
						updater.path_to_pix = request.FILES['path_to_pix']
					else:
						memberavatar = Member.objects.get(email = self.useremail)
						members_avatar = memberavatar.pix
						updater.path_to_pix = members_avatar
					toupdate = Member.objects.get(email = self.useremail)
					toupdate.email = updater.email
					toupdate.phone = updater.phone
					toupdate.username = updater.username
					toupdate.pix = updater.path_to_pix
					toupdate.function_held = updater.function_held
					# update for django model too
					toupdate0 = User.objects.get(email = self.useremail)
					toupdate0.email,toupdate0.username = updater.email, updater.email

					# store most current email
					self.currentmail = updater.email

					# save the update
					toupdate.save()
					toupdate0.save()

					return HttpResponseRedirect(reverse('home:member_account', kwargs = {'mail': self.currentmail}))

				else:
					print('Invalid Update')
					HttpResponseRedirect(reverse('home:index'))

class PostHandlerView(View):

	def post(self, request,*args, **kwargs):
		if (request.user.is_authenticated):
			self.kwargs = kwargs
			self.useremail = self.kwargs['mail']
			if (request.user.username == self.useremail):
				self.template = 'home/success.html'
				self.mail= self.kwargs['mail']
				self.member = Member.objects.get(email=self.mail)
				render_type = 'new_post'
				self.post_form = PostForm(request.POST, request.FILES)
				if(self.post_form.is_valid()):
					self.post_form.save()
					return render(request, self.template,{'member':self.member,'render_type':\
						render_type})
				print(self.post_form.errors)
			else:
				return HttpResponseRedirect(reverse('home:index'))

		else:
			return HttpResponseRedirect(reverse('home:index'))


class membersLogoutView(View):

	def get(self,request):
		logout(request)
		template = 'home/success.html'
		render_type = 'member_logout'
		return render(request,template,{'render_type': render_type})

	def post(self,request):
		return HttpResponse("Its a post request dummy")

class ForumMainView(View):

	def __forumupdater__(self, useremail):
		self.useractiveforum = []
		self.useremail = useremail
		self.getallforum = Forum.objects.all()
		self.current_user = Member.objects.get(email = self.useremail)
		for forum in self.getallforum:
			if(self.current_user in forum.forum_members.all()):
				self.useractiveforum.append(forum)
		return self.useractiveforum

	def get(self, request,*args, **kwargs):
		if (request.user.is_authenticated):
			self.kwargs = kwargs
			self.currentforum = self.kwargs['name']
			self.useremail = self.kwargs['mail']
			if (request.user.username == self.useremail):
				self.template = 'home/forum.html'
				self.member = Member.objects.get(email=self.useremail)
				self.getcurrentforum = Forum.objects.get(forum_name = self.currentforum)
				self.updatemembers = ForumForm(instance = self.getcurrentforum)
				self.getforumdetails = ForumDetail.objects.get(source_forum = self.getcurrentforum)
				self.first_value = {'source_forum': self.getcurrentforum,'posted_by': self.member.__str__()}
				self.Messenger = MessageForm(initial = self.first_value)
				messages = Message.objects.filter(source_forum = self.getcurrentforum).order_by('upload_time')[:200]
				self.activeforums = self.__forumupdater__(self.useremail)
				if (request.GET.get('msg') == 'all'):
					messages = Message.objects.filter(source_forum = self.getcurrentforum).order_by('upload_time')
				return render(request, self.template,{'member':self.member,'forum': self.getcurrentforum ,\
					'forum_detail': self.getforumdetails,'messenger': self.Messenger, 'messages':messages,\
					'active_forums':self.activeforums,'update_members':self.updatemembers})
			else:
				return HttpResponseRedirect(reverse('home:index'))

		else:
			return HttpResponseRedirect(reverse('home:index'))

	
	def post(self, request, *args, **kwargs):
			if (request.user.is_authenticated):
				self.kwargs = kwargs
				self.currentforum = self.kwargs['name']
				self.useremail = self.kwargs['mail']
				if (request.user.username == self.useremail):
					self.template = 'home/forum.html'
					self.member = Member.objects.get(email=self.useremail)
					self.getcurrentforum = Forum.objects.get(forum_name = self.currentforum)
					self.getforumdetails = ForumDetail.objects.get(source_forum = self.getcurrentforum)
					self.Messenger = MessageForm(request.POST)
					if(self.Messenger.is_valid()):
						self.Messenger.save()
						messages = Message.objects.filter(source_forum = self.getcurrentforum).order_by('upload_time')[:200]
						self.first_value = {'source_forum': self.getcurrentforum,'posted_by': self.member.__str__()}
						self.Messenge = MessageForm(initial = self.first_value)
						self.activeforums = self.__forumupdater__(self.useremail)
						return render(request, self.template,{'member':self.member,'forum': self.getcurrentforum ,\
					'forum_detail': self.getforumdetails,'messenger': self.Messenge, 'messages':messages,\
					'active_forums':self.activeforums})
					else:
						return HttpResponseRedirect(reverse('home:index'))

			else:
				return HttpResponseRedirect(reverse('home:index'))

class UpdateHandlerView(View):
	def __forumupdater__(self, useremail):
		self.useractiveforum = []
		self.useremail = useremail
		self.getallforum = Forum.objects.all()
		self.current_user = Member.objects.get(email = self.useremail)
		for forum in self.getallforum:
			if(self.current_user in forum.forum_members.all()):
				self.useractiveforum.append(forum)
		return self.useractiveforum

	def post(self, request, *args, **kwargs):
			if (request.user.is_authenticated):
				self.kwargs = kwargs
				self.currentforum = self.kwargs['name']
				self.useremail = self.kwargs['mail']
				if (request.user.username == self.useremail):
					self.template = 'home/forum.html'
					self.member = Member.objects.get(email=self.useremail)
					self.getcurrentforum = Forum.objects.get(forum_name = self.currentforum)
					self.getforumdetails = ForumDetail.objects.get(source_forum = self.getcurrentforum)
					self.addmoremembers = ForumForm(request.POST, instance = self.getcurrentforum)
					if(self.addmoremembers.is_valid()):
						print('update form is valid')
						self.addmoremembers.save()
						self.updatedforum = Forum.objects.get(forum_name = self.currentforum)
						self.getforumdetails.total_no_of_members = self.updatedforum.forum_members.count()
						self.getforumdetails.save()
						self.updatemembers = ForumForm(instance = self.updatedforum)
						messages = Message.objects.filter(source_forum = self.getcurrentforum).order_by('upload_time')[:200]
						self.first_value = {'source_forum': self.getcurrentforum,'posted_by': self.member.__str__()}
						self.Messenge = MessageForm(initial = self.first_value)
						self.activeforums = self.__forumupdater__(self.useremail)
						return render(request, self.template,{'member':self.member,'forum': self.getcurrentforum ,\
					'forum_detail': self.getforumdetails,'messenger': self.Messenge, 'messages':messages,\
					'active_forums':self.activeforums,'update_members':self.updatemembers})
					else:
						print('Invalid')
						print(self.addmoremembers.errors)
						return HttpResponseRedirect(reverse('home:index'))

			else:
				return HttpResponseRedirect(reverse('home:index'))

class ForumExploreView(View):

	def get(self, request,*args, **kwargs):
		if (request.user.is_authenticated):
			self.kwargs = kwargs
			self.useremail = self.kwargs['mail']
			if (request.user.username == self.useremail):
				self.template = 'home/forumexplore.html'
				self.member = Member.objects.get(email=self.useremail)
				self.allpubicforums = ForumDetail.objects.filter(source_forum__forum_type = 'PUBLIC').order_by('-created_on')
				paginator = Paginator(self.allpubicforums,20)
				page = request.GET.get('page')
				forum_detail = paginator.get_page(page)
				return render(request, self.template,{'member':self.member, 'forum_detail': forum_detail})
			else:
				return HttpResponseRedirect(reverse('home:index'))

		else:
			return HttpResponseRedirect(reverse('home:index'))

class AddToForumView(View):

	def get(self, request,*args, **kwargs):
		if (request.user.is_authenticated):
			self.kwargs = kwargs
			self.useremail = self.kwargs['mail']
			if (request.user.username == self.useremail):
				self.template = 'home/success.html'
				self.member = Member.objects.get(email=self.useremail)
				self.getforum = self.kwargs['name']
				self.getcurrentforum = Forum.objects.get(forum_name = self.getforum)
				self.getcurrentforum.forum_members.add(self.member)
				forum_name = self.getcurrentforum.forum_name
				self.getcurrentforumdetail = ForumDetail.objects.get(source_forum = self.getcurrentforum)
				author = self.getcurrentforumdetail.created_by
				self.getcurrentforum.save()
				self.getcurrentforum = Forum.objects.get(forum_name = self.getforum)
				new_count = self.getcurrentforum.forum_members.count()
				self.getcurrentforumdetail = ForumDetail.objects.get(source_forum = self.getcurrentforum)
				self.getcurrentforumdetail.created_by = author
				self.getcurrentforumdetail.total_no_of_members = new_count
				self.getcurrentforumdetail.save()
				render_type = 'add_member'
				return render(request, self.template,{'member':self.member, 'render_type': render_type,\
					'forum_name':forum_name})
			else:
				return HttpResponseRedirect(reverse('home:index'))

		else:
			return HttpResponseRedirect(reverse('home:index'))

class LeaveForumView(View):

	def get(self, request,*args, **kwargs):
		if (request.user.is_authenticated):
			self.kwargs = kwargs
			self.useremail = self.kwargs['mail']
			if (request.user.username == self.useremail):
				self.template = 'home/success.html'
				self.member = Member.objects.get(email=self.useremail)
				self.getforum = self.kwargs['name']
				self.getcurrentforum = Forum.objects.get(forum_name = self.getforum)
				self.getcurrentforum.forum_members.remove(self.member)
				forum_name = self.getcurrentforum.forum_name
				self.getcurrentforumdetail = ForumDetail.objects.get(source_forum = self.getcurrentforum)
				author = self.getcurrentforumdetail.created_by
				self.getcurrentforum.save()
				self.getcurrentforum = Forum.objects.get(forum_name = self.getforum)
				new_count = self.getcurrentforum.forum_members.count()
				self.getcurrentforumdetail = ForumDetail.objects.get(source_forum = self.getcurrentforum)
				self.getcurrentforumdetail.created_by = author
				self.getcurrentforumdetail.total_no_of_members = new_count
				self.getcurrentforumdetail.save()
				render_type = 'remove_member'
				return render(request, self.template,{'member':self.member, 'render_type': render_type,\
					'forum_name':forum_name})
			else:
				return HttpResponseRedirect(reverse('home:index'))

		else:
			return HttpResponseRedirect(reverse('home:index'))

class NotificationView(View):

	def get(self, request,*args, **kwargs):
		if (request.user.is_authenticated):
			self.kwargs = kwargs
			self.useremail = self.kwargs['mail']
			if (request.user.username == self.useremail):
				self.template = 'home/notifications.html'
				self.mail= self.kwargs['mail']
				self.member = Member.objects.get(email = self.useremail)
				self.notifications = Notification.objects.filter(notifying = self.member).order_by('-notify_time')
				return render(request, self.template,{'notifications':self.notifications})
			else:
				return HttpResponseRedirect(reverse('home:index'))

		else:
			return HttpResponseRedirect(reverse('home:index'))


class OtherMembersView(View):
	'''This is the view that gives
	a list of all the members on the
	website'''

	def get(self, request, *args, **kwargs):
		'''This is the method that
		handles all the get request
		sent to this view'''

		if (request.user.is_authenticated):
			self.kwargs = kwargs
			self.useremail = self.kwargs['mail']
			if (request.user.username == self.useremail):
				self.template = 'home/other_members.html'
				self.mail= self.kwargs['mail']
				self.member = Member.objects.get(email = self.useremail)
				self.other_members = Member.objects.all().order_by('-D_O_B')
				paginator = Paginator(self.other_members,20)
				page = request.GET.get('page')
				other_members = paginator.get_page(page)
				return render(request, self.template,{'other_members':other_members})
			else:
				return HttpResponseRedirect(reverse('home:index'))

		else:
			return HttpResponseRedirect(reverse('home:index'))


class PrivateForumView(View):
	'''This view facilitates
	user to user messaging for
	this site'''

	def get(self,request, *args, **kwargs):
		'''This method handles all
		get request sent to Private forum'''
		self.kwargs = kwargs
		self.useremail = self.kwargs['mail']
		self.current_user = Member.objects.get(email = self.useremail)
		self.other_user = Member.objects.get(email = self.kwargs['other_user_mail'])
		if (request.user.username == self.useremail):
			try:
				forum = Forum.objects.get(forum_name = '%s et %s' % (self.current_user.firstname,self.other_user.firstname))
				# more code on what to do if forum exist
				forum_name = '%s et %s' % (self.current_user.firstname,self.other_user.firstname)
				return HttpResponseRedirect(reverse('home:forum',kwargs = {'name': forum_name,'mail':self.useremail}))
				print("First Try")
			except Forum.DoesNotExist:
				print("First Except")
				try:
					print("Second Try")
					alt_forum = Forum.objects.get(forum_name = '%s et %s' % (self.other_user.firstname, self.current_user.firstname))
					# more code on what to do if forum exist
					forum_name =  '%s et %s' % (self.other_user.firstname, self.current_user.firstname)
					return HttpResponseRedirect(reverse('home:forum',kwargs = {'name': forum_name,'mail':self.useremail}))
				except Forum.DoesNotExist:
					print("Second Except")
					self.forum_creator = Forum(
					forum_name = '%s et %s' % (self.current_user.firstname,self.other_user.firstname),
					forum_logo = 'static/home/images/private_forum.png',
					forum_type = 'PRIVATE',
					forum_description = 'Private forum for {} and {}'.format(self.current_user.firstname,self.other_user.firstname))
					try:
						self.forum_creator.save()
						self.forum = Forum.objects.get(forum_name = '%s et %s' % (self.current_user.firstname,self.other_user.firstname))
						self.forum.forum_members.set((self.current_user,self.other_user))
						self.source_forum = self.forum
						self.created_by = self.current_user.__str__()
						self.total_no_of_members = self.forum.forum_members.count()
					except:
						print("Forum not clean")
						print(self.forum_creator.full_clean())

	
					
					save_forum_details = ForumDetail(source_forum = self.source_forum,\
						created_by = self.created_by,total_no_of_members = \
						self.total_no_of_members)
					save_forum_details.save()
					# Notify all members that they have been added to the new forum
					for member in self.source_forum.forum_members.all():
						notifying = member
						notification_content = 'You have been added to a new forum, You are now a member of %s forum'%\
						self.source_forum.forum_name
						new_notification = Notification(notifying = notifying, notification_content = notification_content)
						new_notification.save()
					template = 'home/success.html'
					the_member = Member.objects.get(email = self.useremail)
					the_forum_name = self.source_forum.forum_name
					render_type = 'forum_creation'
					return render(request, template,{'render_type': render_type, 'the_forum_name':the_forum_name,\
						'member': the_member})
		else:
			return HttpResponseRedirect(reverse('home:index'))