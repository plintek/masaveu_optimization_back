from django.urls import path
from . import views

urlpatterns = [
    path('execute-algorithm/', views.ExecuteAlgorithmApiView.as_view(),
         name='execute-algorithm'),
    path('load-data/', views.LoadDataApiView.as_view(), name='load-data'),
    path('save-data/', views.SaveDataApiView.as_view(), name='save-data'),
]
