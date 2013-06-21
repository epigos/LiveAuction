from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'LiveAuction.views.index_view', name='index_view'),
	url(r'^login/$', 'LiveAuction.views.login_view', name='login_view'),
	url(r'^logout/$', 'LiveAuction.views.logout_view', name='logout_view'),
	url(r'^register/$', 'LiveAuction.views.register_view', name='register_view'),
    url(r'^admin/', include(admin.site.urls))
)
