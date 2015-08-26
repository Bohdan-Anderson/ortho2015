from django.conf.urls import url
from form import views

urlpatterns = [
	# url(r'^project/(?P<url>[a-z 0-9 \. \/]+)$', views.project_edit),
	url(r'^$',views.home),
	url(r'success/$',views.success)
]
