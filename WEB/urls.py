from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import settings

from asker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('question/<int:id>/', views.question, name='question'),
    path('admin/', admin.site.urls),
    path('ask/', views.ask, name='ask'),
    path('hot/', views.hot, name='hot'),
    path('registration_page/', views.registration_page, name='registration_page'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login, name='login'),
    path('tag/<str:tag>/', views.tag, name='tag'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
