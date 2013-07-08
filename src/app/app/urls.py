from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'LiveAuction.views.index_view', name='index_view'),
	url(r'^login/$', 'LiveAuction.views.login_view', name='login_view'),
	url(r'^logout/$', 'LiveAuction.views.logout_view', name='logout_view'),
	url(r'^register/$', 'LiveAuction.views.register_view', name='register_view'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auctions/page/(?P<pagina>.*)/$', 'LiveAuction.views.auction_index_view', name='auction_index_view'),
    url(r'^auction/(?P<id_auction>.*)/$','LiveAuction.views.singleAuction_view',name='singleAuction_view')
)