
from django.conf.urls import url, include
from lists import urls as list_urls
from accounts import urls as accounts_urls
from lists.views import home_page

urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^lists/', include(list_urls)),
    url(r'^accounts/', include(accounts_urls))

]
