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
    
    #Clients
	url(r'^newclient$', views.newclient, name='newclient'),
	url(r'^list_clients$', views.list_clients, name='list_clients'),
    url(r'^list_clients_edit$', views.list_clients_edit, name='list_clients_edit'),
    url(r'^list_clients_delete$', views.list_clients_delete, name='list_clients_delete'),

    # Cartridges
    url(r'^newcartridges$', views.newcartridges, name='newcartridges'),
    url(r'^list_cartridges$', views.list_cartridges, name='list_cartridges'),
    url(r'^list_cartridges_edit$', views.list_cartridges_edit, name='list_cartridges_edit'),
    url(r'^list_cartridges_delete$', views.list_cartridges_delete, name='list_cartridges_delete'),
    url(r'^recharge_cartridge$', views.recharge_cartridge, name='recharge_cartridge'),
    url(r'^restore_cartridge$', views.restore_cartridge, name='restore_cartridge'),
    url(r'^list_cartridges_service_edit$', views.list_cartridges_service_edit, name='list_cartridges_service_edit'),
    url(r'^list_cartridges_clients/(?P<clientid>[^/]+)/$', views.list_cartridges_clients , name='list_cartridges_clients ')
    
)


