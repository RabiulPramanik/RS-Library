
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import Home, home


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', Home.as_view(), name="home"),
    path('', home, name="home"),
    path('category/<slug:category_slug>/', home, name="category_wise_book"),
    path('accounts/', include("accounts.urls")),
    path('books/', include("books.urls")),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
