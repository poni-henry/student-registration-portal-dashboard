from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('',  views.login_view, name='login'),  # Default route to home view
    path('signup/', views.signup_view, name='signup'),
    path('enroll/', views.enroll, name='enroll'),
    path('register/', views.register_page, name='register'),
    path('download_receipt/', views.download_receipt, name='download_receipt'),
    path('upload_bank_statement/', views.upload_bank_statement, name='upload_bank_statement'),
    path('dashboard/', views.combined_view, name='dashboard'),
    path('your_view_function',views.your_view_function, name='your_view_function')
]

# Serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)