from django.contrib import admin
from django.urls import path

from .views import request_yellowant_oauth_code, yellowant_oauth_redirect, yellowant_api,api_key


urlpatterns = [

    path("create-new-integration/", request_yellowant_oauth_code, name="request-yellowant-oauth"),
    path("redirecturl/", yellowant_oauth_redirect, name="yellowant-oauth-redirect"),
    #path("redirecturl/", yellowant_oauth_redirect, name="home"),
    path("apiurl/", yellowant_api, name="yellowant-api"),
    path("apikey/",api_key,name="yellowant_api")
   # path("/",yell)
]
