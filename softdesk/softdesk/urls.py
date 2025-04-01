from django.contrib import admin
from django.urls import path, include

from api.views import UserAPIViewset, ProjectAPIViewset, ContributorAPIViewset, IssueAPIViewset, CommentAPIViewset, WhoAmIView  # import CategoryAPIView
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView





#DS
from api.views import (
    
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
    #RegisterViewSet,
    
)








router = routers.SimpleRouter()
router.register(r'users', UserAPIViewset, basename='user')

router.register(r'projects', ProjectAPIViewset, basename='project')
router.register('contributor', ContributorAPIViewset, basename='contributor')
router.register('issue', IssueAPIViewset, basename='issue')
router.register('comment', CommentAPIViewset, basename='comment')
#router.register('register', RegisterView, basename='register')



# urlpatterns = [

#     # Authentification

#     path('admin/', admin.site.urls),
#     path('api-auth/', include('rest_framework.urls')),
#     path('api/login/', obtain_auth_token, name='api_token_auth'),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

#     #Projects
#     path('api/', include(router.urls)),
#     path('api/whoami/', WhoAmIView.as_view(), name='whoami')
   
    
# ]


# Routes imbriquées manuellement
urlpatterns = [
    # Authentification
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    
    path('api/whoami/', WhoAmIView.as_view(), name='whoami'),

    # Projets
    path('api/', include(router.urls)),

    # Contributors (imbriqué sous projets)
    path('api/projects/<int:project_id>/contributors/',
         ContributorViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='contributors'),
    path('api/projects/<int:project_id>/contributors/<int:pk>/',
         ContributorViewSet.as_view({'delete': 'destroy'}),
         name='contributor-detail'),

    # Issues (imbriqué sous projets)
    path('api/projects/<int:project_id>/issues/',
         IssueViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='issues'),
    path('api/projects/<int:project_id>/issues/<int:pk>/',
         IssueViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='issue-detail'),

    # Comments (imbriqué sous issues)
    path('api/issues/<int:issue_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='comments'),
    path('api/comments/<int:pk>/',
         CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='comment-detail'),
]