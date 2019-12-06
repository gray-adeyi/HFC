

class Notification(models.Model):
	notifications_for = models.ForeignKey(Member, on_delete = models.CASCADE)
	content = models.TextField()
	upload_time = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return "Notification for %s"%(self.notifications_for)

class TextPost(models.Model):
	content = models.TextField()

	def __str__(self):
		return self.content

class PicturePost(models.Model):
	picture = models.ImageField(upload_to = 'posts/pictures')

	def __str__(self):
		return self.picture

class VideoPost(models.Model):
	video = models.FileField(upload_to = 'posts/videos')

	def __str__(self):
		return self.video


		widgets = {
		'posted_by': forms.TextInput(attrs = {'class': 'validate hide', 'id':'posted_by'}),
		'content': forms.Textarea(attrs = {'class':'materialize-textarea', 'placeholder':'Please type in your message here...','id':'content',\
			'autofocus':'autofocus'})
		}
