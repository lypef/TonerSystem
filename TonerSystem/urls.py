from django.conf.urls import patterns, include, url
from django.contrib import admin
from app import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TonerSystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', views.login ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name = 'login' ),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', name = 'logout' ),
	url(r'^manage$', views.manage, name='manage'),	
	url(r'^newclient$', views.newclient, name='newclient'),
	url(r'^search$', views.search, name='search'),
    url(r'^list_clients$', views.list_clients, name='list_clients'),
    url(r'^list_clients_edit$', views.list_clients_edit, name='list_clients_edit'),
    url(r'^list_clients_delete$', views.list_clients_delete, name='list_clients_delete')
)
