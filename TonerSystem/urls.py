from django.conf.urls import patterns, include, url
from django.contrib import admin
from app import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TonerSystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.login ),
    url(r'^admin/', include(admin.site.urls)),
)
