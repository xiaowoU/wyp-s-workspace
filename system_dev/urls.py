"""system_dev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from user_manage.views import index, RegisterView, LoginView, LogoutView, test


urlpatterns = [
    path('test/', test, name="test"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('admin/', admin.site.urls, name="admin"),

    re_path('^user_manage/', include(('user_manage.urls', 'user_manage'), namespace='user_manage')),
    re_path('^data_display/', include(('data_display.urls', 'data_display')), name="data_display"),

    re_path('^$', index, name='index'),    # 放在最后
    # re_path('^$', admin.site.urls, name="admin"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
