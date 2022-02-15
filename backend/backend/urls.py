from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('testproject.urls')),
    path('account/', include('account.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# if settings.DEBUG:
#     import debug_toolbar

#     urlpatterns += [
#         path("__debug__/", include("debug_toolbar.urls")),
#     ]