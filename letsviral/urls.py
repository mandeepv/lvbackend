from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('creator/', include('creator.urls')),
    path('admin/', admin.site.urls),
]
