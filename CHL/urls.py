from django.conf.urls import url,include
import views

urlpatterns = [
    url(r'^$', views.app, name='app'),
    url(r'^patient_viewer/', views.patient_viewer, name="patient_viewer"),
    url(r'^codelist$', views.codelist, name="codelist"),
]
