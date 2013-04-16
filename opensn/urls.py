from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth import views as auth_views
from customuser import views as UserHome

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
    url(r'^profile/$', UserHome.profile, name="profile"),
    url(r'^wall/$', UserHome.wall, name="wall"),
    
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()