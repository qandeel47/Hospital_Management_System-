from django.urls import path

from .views import (
    ReceptionistCreateAPIView,
    ReceptionistListAPIView,
    ReceptionistRetrieveAPIView,
    ReceptionistUpdateAPIView,
    ReceptionistDeleteAPIView,
)

urlpatterns = [

    path("", ReceptionistListAPIView.as_view(), name="receptionist-list",  ),
    path( "create/", ReceptionistCreateAPIView.as_view(), name="receptionist-create",),
    path( "<int:pk>/", ReceptionistRetrieveAPIView.as_view(),name="receptionist-detail",),
    path( "<int:pk>/update/", ReceptionistUpdateAPIView.as_view(), name="receptionist-update",),
    path("<int:pk>/delete/",ReceptionistDeleteAPIView.as_view(),name="receptionist-delete",  ),

       
        
]