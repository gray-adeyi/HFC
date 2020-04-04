from django.db import models
from django.utils import timezone

# Create your models here.
class Member(models.Model):
	'''
	This model is for all the members
	'''

	sex = ('Male',
		'Female') # work on this too
	firstname = models.CharField(max_length = 50, default = 'UNKNOWN')
	lastname = models.CharField(max_length = 50, default = 'UNKNOWN')
	email = models.EmailField()
	phone = models.CharField(max_length = 14)
	D_O_B = models.DateField(blank = True, null=True)
	gender = models.CharField(max_length = 10)
	username = models.CharField(max_length = 50)
	passwd = models.CharField(max_length = 64)
	function_held = models.CharField(max_length = 30)
	pix = models.ImageField(upload_to = 'home/images/members_image')
	date_joined = models.DateTimeField(auto_now_add = True, editable=True)

	def __str__(self):
		return '%s @%s'%(self.firstname, self.username)

	def member_to_string(self):
		return '%s @%s'%(self.firstname, self.username)

	def get_members_details(self):
		return "First-name: {1}\nLast-name: {2}\nEmail: {3}\nPhone: {4}\nD.O.B:\
		 {5}\nGender: {6}\nUser-name: {7}\nfunction_held: {8}\npath_to_pix:\
		  {9}\nDate joined: {10}".format(self.firstname, self.lastame, self.email, self.phone,\
		   self.D_O_B, self.gender, self.username, self.function_held, self.pix, self.date_joined)


class Article(models.Model):
	'''
	This model helps to store data for articles,
	news and bible study
	'''
	articles_type_short = (
		('N','News'),
		('HB','History and Biography'),
		('B','Bible Study'),
		('O','Others'))
	publisher = models.CharField(max_length = 500)
	pub_type = models.CharField(max_length = 100, choices = articles_type_short)
	title = models.CharField(max_length = 1000)
	content = models.TextField()
	pub_date_et_time = models.DateTimeField(default = timezone.now)
	article_image = models.ImageField(upload_to = 'home/articles')

	def __str__(self):
		return self.title

	def get_articles_details(self):
		return print("Publisher: {0}\nPublication Type: {1}\nTitle: {2}\nPublication Date: {3}".\
		format(self.publisher, self.pub_type, self.title, self.pub_date_et_time))

class Download(models.Model):
	filetype_short = (
		('M', 'Music'),
		('V', 'Video'),
		("Pic", 'Pictures'),
		("Pdf", 'Pdf'),
		("O", "Others"))
	filename = models.CharField(max_length = 1000)
	filetype = models.CharField(max_length = 100, choices = filetype_short)
	upload_date = models.DateTimeField()

class DownloadFile(models.Model):
	download = models.ForeignKey(Download, on_delete = models.CASCADE)
	poster = models.ImageField(upload_to = 'downloads/posters')
	data = models.FileField(upload_to = 'downloads')

class Page(models.Model):
	name = models.CharField(max_length = 50)

	def __str__(self):
		return self.name

class PageContent(models.Model):
	page = models.ForeignKey(Page,on_delete = models.CASCADE)
	content_name = models.CharField(max_length = 100, unique = True)
	content_store = models.TextField()

	def __str__(self):
		return self.content_name

class Reply(models.Model):
	name = models.CharField(max_length = 50, default = "Anonymous")
	reply = models.TextField()
	reply_type = models.CharField(max_length = 20)

	def __str__(self):
		return self.name

class Forum(models.Model):
	forum_typ = (
		('PUBLIC','public'),
		('PRIVATE','private'))
	forum_name = models.CharField(max_length = 500, unique = True)
	forum_logo = models.ImageField(upload_to = 'forum logos')
	forum_type = models.CharField(max_length = 15, choices = forum_typ)
	forum_description = models.TextField(default = "This forum was created to....")
	forum_members = models.ManyToManyField(Member)

	def __str__(self):
		return self.forum_name

class ForumDetail(models.Model):
	source_forum = models.OneToOneField(Forum, on_delete = models.CASCADE)
	created_by = models.CharField(max_length = 200)
	created_on = models.DateTimeField(auto_now_add = True)
	total_no_of_members = models.CharField(max_length = 10)

	def __str__(self):
		return self.source_forum.forum_name

class Message(models.Model):
	source_forum = models.ForeignKey(Forum, on_delete = models.CASCADE)
	posted_by = models.CharField(max_length = 50)
	upload_time = models.DateTimeField(auto_now_add = True)
	content = models.TextField()

	def __str__(self):
		return self.content

class MessageReply(models.Model):
	reply_by = models.CharField(max_length = 50)
	reply_to = models.CharField(max_length = 50)
	upload_time = models.DateTimeField(auto_now_add = True)
	content = models.TextField()
	source_message = models.ForeignKey(Message, on_delete = models.CASCADE)

	def __str__(self):
		return "%s replied to %s"%(self.reply_by,self.reply_to)

class Post(models.Model):
	posted_by = models.ForeignKey(Member, on_delete=models.CASCADE)
	text = models.TextField(max_length = 10000, blank = True)
	picture = models.ImageField(upload_to = 'posts/pictures', blank = True)
	video = models.FileField(upload_to = 'posts/videos', blank = True)
	upload_time = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return '%s @%s'%(self.posted_by.firstname, self.posted_by.username)

class Notification(models.Model):
	notifying = models.ForeignKey(Member, on_delete = models.CASCADE)
	notification_content = models.TextField(max_length = 5000)
	notify_time = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return '%s @%s'%(self.notifying.firstname, self.notifying.username)

class Developer(models.Model):
	full_name = models.CharField(max_length = 45)
	email = models.EmailField()
	phone = models.CharField(max_length = 14)
	photo = models.ImageField(upload_to = 'developers/images')
	languages = models.TextField()
	contributions = models.TextField()

	def __str__(self):
		return self.full_name

class Contributor(models.Model):
	full_name = models.CharField(max_length = 45)
	email = models.EmailField()
	phone = models.CharField(max_length = 14)
	photo = models.ImageField(upload_to = 'developers/images')
	contributions = models.TextField()

	def __str__(self):
		return self.full_name

class Tool(models.Model):
	'''This model stores the details
	of programming tools used on this site'''
	name = models.CharField(max_length = 100)
	photo = models.ImageField(upload_to = 'Tools/images')
	use = models.TextField()
	website = models.CharField(max_length = 200)

	def __str__(self):
		return self.name


class ChurchDetail(models.Model):
	name = models.CharField(max_length = 200)
	email = models.EmailField()
	account_name = models.CharField(max_length = 20)
	account_no = models.CharField(max_length = 14)
	account_bank = models.CharField(max_length = 20)
	mission_statement = models.TextField()
	vision_statement = models.TextField()
	address = models.TextField()

	def __str__(self):
		return self.name

class Phone(models.Model):
	name = models.CharField(max_length = 200)
	number = models.CharField(max_length = 14)
	church_detail = models.ForeignKey(ChurchDetail, on_delete = models.CASCADE)

	def __str__(self):
		return self.name

class Service(models.Model):
	title = models.CharField(max_length = 200)
	summary = models.TextField()
	held_on = models.TextField()
	held_at = models.TextField()
	church_detail = models.ForeignKey(ChurchDetail, on_delete = models.CASCADE)

	def __str__(self):
		return self.title

class ChurchOfficial(models.Model):
	title = models.CharField(max_length = 100)
	full_name = models.CharField(max_length = 100)
	photo = models.ImageField(upload_to = 'church officials/images')
	position = models.CharField(max_length = 100)
	email = models.EmailField(blank = True)
	phone = models.CharField(max_length = 14, blank = True)
	small_bio = models.TextField()
	church_detail = models.ForeignKey(ChurchDetail, on_delete = models.CASCADE)

	def __str__(self):
		return self.full_name
	

class About(models.Model):
	title = models.CharField(max_length = 200)
	content = models.TextField()
	church_detail = models.ForeignKey(ChurchDetail, on_delete = models.CASCADE)

	def __str__(self):
		return self.title

class AboutImage(models.Model):
	title = models.CharField(max_length = 200)
	photo = models.ImageField(upload_to = 'about/images')
	church_detail = models.ForeignKey(ChurchDetail, on_delete = models.CASCADE)

	def __str__(self):
		return self.title