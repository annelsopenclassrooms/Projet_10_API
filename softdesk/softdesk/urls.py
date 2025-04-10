from django.contrib import admin
from django.urls import path, include

from api.views import UserAPIViewset, ProjectAPIViewset, ContributorAPIViewset, \
    IssueAPIViewset, CommentAPIViewset, WhoAmIView  # import CategoryAPIView
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.SimpleRouter()
router.register(r'users', UserAPIViewset, basename='user')

router.register(r'projects', ProjectAPIViewset, basename='project')
router.register(r'contributor', ContributorAPIViewset, basename='contributor')
router.register(r'issues', IssueAPIViewset, basename='issue')
router.register(r'comments', CommentAPIViewset, basename='comment')


urlpatterns = [

    # Authentification

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Projects
    path('api/', include(router.urls)),
    path('api/whoami/', WhoAmIView.as_view(), name='whoami')

]
