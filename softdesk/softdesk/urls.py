from django.contrib import admin
from django.urls import path, include

from api.views import UserAPIViewset, ProjectAPIViewset, ContributorAPIViewset, IssueAPIViewset, CommentAPIViewset, RegisterView, WhoAmIView  # import CategoryAPIView
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.SimpleRouter()
router.register('user', UserAPIViewset, basename='user')
router.register('project', ProjectAPIViewset, basename='project')
router.register('contributor', ContributorAPIViewset, basename='contributor')
router.register('issue', IssueAPIViewset, basename='issue')
router.register('comment', CommentAPIViewset, basename='comment')
router.register('register', RegisterView, basename='register')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/whoami/', WhoAmIView.as_view(), name='whoami')
   
    
]


