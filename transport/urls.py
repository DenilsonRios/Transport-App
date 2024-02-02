from django.urls import path, include 
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from transport import views

router = routers.DefaultRouter()
router.register(r'usersprofiles', views.UserProfileView)

urlpatterns = [
    path("api/", include(router.urls)),
    path("docs/", include_docs_urls(title="Transport API")),
    path('create_account/', views.create_account, name='create_account'),
    path('login/', views.login_view, name='login_view'),
    path('create_service/', views.create_service, name='create_service'),
    path('get_available_services/', views.get_available_services, name='get_available_services'),
    path('accept_service/', views.accept_service, name='accept_service'),
    path('cancel_service/', views.cancel_service, name='cancel_service')
]


