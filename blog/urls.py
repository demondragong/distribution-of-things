from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
# Serving the media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()