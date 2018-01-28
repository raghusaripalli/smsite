from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework.urlpatterns import format_suffix_patterns

from myapp import views
from django.contrib.auth import views as aviews
urlpatterns = [
    url(r'^$', views.landing_page,name="landing_page"),
    url(r'^register/$', views.registration_page, name="registration_page"),
    url(r'^register/camera/$', views.camera_page, name="camera_page"),
    url(r'^dashboard/$', csrf_exempt(views.dashboard), name="dashboard_page"),
    url(r'^logout/$', aviews.logout, {'next_page': 'landing_page'}, name="logout_page"),
    ## Rest APi's
    url(r'^rest/get/$', views.widget_list, name="rest_widget_list"),
    url(r'^rest/getimages/$', views.user_image_sync, name="rest_image_sync"),
    url(r'^rest/get/(?P<slug>[\w-]+)/$', views.widget_detail, name="rest_widget_detail"),
    url(r'^rest/compare/$',csrf_exempt(views.compareFaces), name="rest_compare_images")
]

urlpatterns = format_suffix_patterns(urlpatterns)