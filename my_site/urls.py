from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', include('common.urls', namespace='common')),
    path('', include('p_library.urls', namespace='p_library')),
    path('', include('social_django.urls')),
]
