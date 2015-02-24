from django.conf.urls import patterns, url

from bizzfuzzUI import views
from bizzfuzzUI.views import UserListView, UserFormView, UserDeleteView, UserExcelDownloadView

urlpatterns = patterns('',
    url(r'^$', UserListView.as_view(), name='list_user'),
    url(r'^user_list_excel/$', UserExcelDownloadView.as_view(), name='list_user_excel'),
    url(r'^adduser/$', UserFormView.as_view(), name='add_user'),
    url(r'^(?P<user_id>\d+)/$', UserFormView.as_view(), name='edit_user'),
    url(r'^(?P<user_id>\d+)/saveuser/$', UserFormView.as_view(), name='save_user'),
    url(r'^(?P<user_id>\d+)/deleteuser/$', UserDeleteView.as_view(), name='delete_user'),
)