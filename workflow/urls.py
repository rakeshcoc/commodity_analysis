from django.contrib import admin
from django.urls import path,include
from workflow import views
app_name ='workflow'
urlpatterns = [
    path('index',views.index,name = "index"),
    # path('refresh_data',views.refresh_data,name="refresh_data"),
    path('search_query',views.search_query.as_view(),name="search_query"),
]
