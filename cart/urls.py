from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^detail/$', views.CartDetail, name='CartDetail'),
    url(r'^remove/(?P<product_id>\d+)/$', views.CartRemove, name='CartRemove'),
    url(r'^add/(?P<product_id>\d+)/$', views.CartAdd, name='CartAdd'),
#    url(r'^submit/$', views.CartSubmit, name='CartSubmit'),  # for sent order
    url(r'^sent/$', views.CartSubmit, name='CartSubmit')  # test shit

]
