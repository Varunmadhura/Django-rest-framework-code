from django.urls import path
from .views import LoginView, RegisterView, RegisterDetails, LoginDetails, DeleteAllLoginUsers, ResendOTPView, CommandExecutionView, CustomTokenObtainView, CustomRefreshTokenView, logout, is_authenticated

urlpatterns = [
    path("api/token/",CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/",CustomRefreshTokenView.as_view(), name='token_refresh'),
    path("api/login/",LoginView.as_view(), name="loginlist"),
    path("api/register/",RegisterView.as_view(),name="reglist"),
    path("api/regdelete/<int:pk>", RegisterDetails.as_view(), name="regdelete"),
    path("api/logdelete/<int:pk>", LoginDetails.as_view(), name="logdelete"),
    path("api/logusersdel/",DeleteAllLoginUsers.as_view(), name="logusersdel" ),
    path("api/resendotp/", ResendOTPView.as_view(), name="resendotp"),
    path("api/execute/",CommandExecutionView.as_view(), name="execute"),
    path("api/logout/", logout),
    path("api/authenticated/", is_authenticated)
]
