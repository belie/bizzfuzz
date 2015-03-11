from django.conf.urls import patterns, url

from bizzfuzzUI import views
from bizzfuzzUI.views import UserListView, UserFormView, UserDeleteView, UserExcelDownloadView, UserForgotPassword, UserNeedLogin, UserForgotPasswordSend, UserForgotPasswordReset, UserLogin, UserLogout, BizzHome

urlpatterns = patterns('',
    url(r'^$', BizzHome.as_view(), name='bizzfuzz_index'),
    url(r'^listusers/$', UserListView.as_view(), name='list_user'),
    url(r'^user_list_excel/$', UserExcelDownloadView.as_view(), name='list_user_excel'),
    url(r'^adduser/$', UserFormView.as_view(), name='add_user'),
    url(r'^(?P<user_id>\d+)/$', UserFormView.as_view(), name='edit_user'),
    url(r'^(?P<user_id>\d+)/saveuser/$', UserFormView.as_view(), name='save_user'),
    url(r'^(?P<user_id>\d+)/deleteuser/$', UserDeleteView.as_view(), name='delete_user'),
    url(r'^needlogin/$', UserNeedLogin.as_view(), name='need_login'),
    url(r'^forgotpassword/$', UserForgotPassword.as_view(), name='forgot_password'),
    url(r'^forgotpassword/sendreminder$', UserForgotPasswordSend.as_view(), name='forgot_password_send'),
    url(r'^forgotpassword/reset/(?P<forgot_password_code>[^/]+)/$', UserForgotPasswordReset.as_view(), name='forgot_password_reset'),
    url(r'^forgotpassword/reset/(?P<forgot_password_code>[^/]+)/saveuser$', UserForgotPasswordReset.as_view(), name='forgot_password_reset_update'),
    url(r'^login/$', UserLogin.as_view(), name='user_login'),
    url(r'^logout/$', UserLogout.as_view(), name='user_logout')
)