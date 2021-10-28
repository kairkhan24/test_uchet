from django.urls import path

from .views import TaskViewSet, TaskExecuteView

urlpatterns = [
    path('', TaskViewSet.as_view({'get': 'list',
                                  'post': 'create'})),
    path('<int:pk>/', TaskViewSet.as_view({'get': 'retrieve',
                                           'patch': 'partial_update',
                                           'delete': 'destroy'})),
    path('<int:pk>/execute/', TaskExecuteView.as_view())
]
