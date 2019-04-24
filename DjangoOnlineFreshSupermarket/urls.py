"""DjangoOnlineFreshSupermarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
# 上传的文件能直接通过url打开，以及setting中设置
from django.conf import settings
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt import views as simplejwt_views  # 引入simplejwt
from goods.views import GoodsListView, GoodsListViewSet, CategoryViewSet, ParentCategoryViewSet
from users.views import SendSmsCodeViewSet

# 创建一个路由器并注册我们的视图集
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name='goods')  # 配置goods的url
router.register(r'categories', CategoryViewSet, base_name='categories')  # 配置分类的url
router.register(r'parent_categories', ParentCategoryViewSet, base_name='parent_categories')  # 配置分类的url
router.register(r'code', SendSmsCodeViewSet, base_name='code')  # 发送短信验证码

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # drf 认证url
    path('api-token-auth/', views.obtain_auth_token),  # drf token获取的url
    # path('api/token/', simplejwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # simplejwt认证接口
    path('login/', simplejwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 登录一般是login
    path('api/token/refresh/', simplejwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # simplejwt认证接口
    path('ckeditor/', include('ckeditor_uploader.urls')),  # 配置富文本编辑器url

    path('', include(router.urls)),  # API url现在由路由器自动确定。

    # DRF文档
    path('docs/', include_docs_urls(title='DRF文档')),
]

# 上传的文件能直接通过url打开
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)