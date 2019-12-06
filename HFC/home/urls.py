# urlconf for home app
from django.urls import path, include
from . import views
from HFC import settings
from django.conf.urls.static import static

app_name = 'home'
urlpatterns = [
	path("", views.Index.as_view(), name = 'index'),
	path("alt", views.AltIndex.as_view(), name = 'altindex'),
	path("comments/", views.Suggestions.as_view()),
	path("forms/<str:form_type>", views.forms_view, name = 'forms'),
	path('success/<str:type>', views.Success.as_view(), name='success'),
	path('login',views.Login.as_view(), name='sign_in'),
	path('password/recovery', views.PasswordRecovery.as_view(), name = 'password_recovery'),
	path('downloads/<str:type>', views.DownloadsView.as_view(), name = 'downloads'),
	path('<str:type>/downloads/<str:filename>', views.OfficialDownloadsView.as_view(), name = 'download_now'),
	path('articles/<str:type>', views.ArticlesListView.as_view(), name = 'articles'),
	path('articles/<str:type>/<str:title>', views.ArticlesView.as_view(), name = 'active_article'),
	path('community/', views.CommunityView.as_view(), name = 'community'),
	path('accounts/activate/<str:mail>', views.ActivateAccount.as_view(), name = 'activate'),
	path('accounts/reset/<str:mail>', views.ResetPassword.as_view(), name = 'change_passwd'),
	path('accounts/member/<str:mail>/', views.MemberAccountView.as_view(), name = 'member_account'),
	path('accounts/member/<str:mail>/<str:post_for>', views.MemberAccountView.as_view(), name = 'member_account'),
	path('accounts/currentmember/logout', views.membersLogoutView.as_view(), name = 'member_logout'),
	path('forums/<str:name>/<str:mail>/', views.ForumMainView.as_view(), name = 'forum'),
	path('private/forums/<str:mail>/<str:other_user_mail>/', views.PrivateForumView.as_view(), name = 'private_forum'),
	path('update/members/<str:name>/<str:mail>/', views.UpdateHandlerView.as_view(), name = 'update'),
	path('explore/forums/<str:mail>/', views.ForumExploreView.as_view(), name = 'explore_forum'),
	path('forums/add_to_forum/<str:name>/<str:mail>/', views.AddToForumView.as_view(), name = 'add_to_forum'),
	path('forums/remove_from_forum/<str:name>/<str:mail>/', views.LeaveForumView.as_view(), name = 'remove_from_forum'),
	path('posts/<str:mail>/', views.PostHandlerView.as_view(), name = 'post'),
	path('accounts/member/notifications/<str:mail>/', views.NotificationView.as_view(), name = 'notification'),
	path('community/others/members/<str:mail>', views.OtherMembersView.as_view(), name = 'other_members'),]


if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
