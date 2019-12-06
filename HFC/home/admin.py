from django.contrib import admin
from .models import Reply, Member, Page, PageContent, Download, Article, DownloadFile,\
Forum, ForumDetail, Message, MessageReply, Post, Notification,Developer,ChurchOfficial,\
Tool, Contributor, ChurchDetail, About, Phone, Service, AboutImage
# Register your models here.


class PageContentInline(admin.StackedInline):
	model = PageContent
	extra = 3

class PageAdmin(admin.ModelAdmin):
	fieldsets = [
	('Page Content Administration', {'fields': ['name',]}),
	]
	inlines = [PageContentInline]

class DownloadFileInline(admin.StackedInline):
	model = DownloadFile
	extra = 1

class DownloadAdmin(admin.ModelAdmin):
	fieldsets = [
	('Downloads Administration', {'fields':['filename', 'filetype', 'upload_date']}),
	]
	inlines = [DownloadFileInline]


admin.site.register(Reply)
admin.site.register(Member)
#admin.site.register(Page, PageAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(Article)
admin.site.register(Forum)
admin.site.register(Message)
admin.site.register(MessageReply)
admin.site.register(ForumDetail)
admin.site.register(Post)
admin.site.register(Notification)
admin.site.register(ChurchOfficial)
admin.site.register(Developer)
admin.site.register(Tool)
admin.site.register(Contributor)
admin.site.register(ChurchDetail)
admin.site.register(About)
admin.site.register(Phone)
admin.site.register(Service)
admin.site.register(AboutImage)