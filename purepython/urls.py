from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from fb.views import (
    index, post_details, login_view, logout_view, profile_view,
    edit_profile_view, like_view, delete_post, delete_comment, edit_post,
    edit_comment, dislike_view, send_gift_view, show_gift_view,
)


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^post/(?P<pk>\d)/$', post_details, name='post_details'),
    url(r'^post/(?P<pk>\d)/like$', like_view, name='like'),
    url(r'^post/(?P<pk>\d)/dislike$', dislike_view, name='dislike'),
    url(r'^post/(?P<pk>\d)/edit$', edit_post, name='edit'),
    url(r'^post/(?P<pk>\d)/delete$', delete_post, name='delete'),
    url(r'^post/(?P<pk>\d)/delete_comment$', delete_comment,
        name='delete_comment'),
    url(r'^post/(?P<pk>\d)/edit_comment$', edit_comment,
        name='edit_comment'),
    url(r'^accounts/login/$', login_view, name='login'),
    url(r'^accounts/logout/$', logout_view, name='logout'),
    url(r'^profile/(?P<user>\w+)/$', profile_view, name='profile'),
    url(r'^profile/(?P<user>\w+)/edit$',
        edit_profile_view, name='edit_profile'),
    url(r'^profile/(?P<username>\w+)/send_gift$',
        send_gift_view, name='send_gift'),
    url(r'^profile/(?P<username>\w+)/show_gift$',
        show_gift_view, name='show_gift'),
    # url(r'^profile/(?P<username>\w+)/single_gift$',
    #    single_gift_view, name='single_gift'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
