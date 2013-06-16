from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth import views as auth_views
from customuser import views as UserHome
from general import views as General
from customsearch import views as CustomSearch
from django.views.generic import RedirectView

from django_messages.views import *

#from messages_custom import views as CustomMessages

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'opensn.views.home', name='home'),
    # url(r'^opensn/', include('opensn.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^login/$',  auth_views.login, {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='auth_logout'),    
    url(r'^$',  UserHome.home, name="site_root"),
    url(r'^home/$', UserHome.home, name="home"),
    url(r'^me/$', UserHome.profile, name="me"),
    url(r'^friends/$', UserHome.friends, name="friends"),
    url(r'^vote$', UserHome.vote, name="vote"),
    
    url(r'^profile/(?P<user_id>\d)/$', UserHome.user_profile, name="user_profile"),
    url(r'^profile/edit/$', UserHome.profile_edit, name="profile_edit"),

    url(r'^wall/$', UserHome.wall, name="wall"),
    url(r'^searchUrls/$', UserHome.searchUrls, name="searchUrls"),
    url(r'^textCrawler/$', UserHome.textCrawler, name="textCrawler"),
    url(r'^settings/$', UserHome.settings, name="settings"),
    url(r'^password/change/$', auth_views.password_change, {'template_name': 'registration/password_change_form.html'},
         name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, 
        {'template_name': 'registration/password_change_done.html'},  name='auth_password_change_done'),
    
    
    url(r'^about/$', General.aboutus, name="aboutus"),
    url(r'^terms/$', General.terms, name="terms"),
    url(r'^privacy/$', General.privacy, name="privacy"),
    url(r'^blog/$', General.blog, name="blog"),
    url(r'^search/$', CustomSearch.home, name="search"),
    #url(r'^messages/$', CustomMessages.home, name="messages_home"),
    #url(r'^messages/$',  include('django_messages.urls')),

    url(r'^messages/$', RedirectView.as_view(url='inbox/'), name='messages_redirect'),
    url(r'^messages/inbox/$', inbox, name='messages_inbox'),
    url(r'^messages/outbox/$', outbox, name='messages_outbox'),
    url(r'^messages/compose/$', compose, name='messages_compose'),
    url(r'^messages/compose/(?P<recipient>[\w.@+-]+)/$', compose, name='messages_compose_to'),
    url(r'^messages/reply/(?P<message_id>[\d]+)/$', reply, name='messages_reply'),
    url(r'^messages/view/(?P<message_id>[\d]+)/$', view, name='messages_detail'),
    url(r'^messages/delete/(?P<message_id>[\d]+)/$', delete, name='messages_delete'),
    url(r'^messages/undelete/(?P<message_id>[\d]+)/$', undelete, name='messages_undelete'),
    url(r'^messages/trash/$', trash, name='messages_trash'),
)


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()