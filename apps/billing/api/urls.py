from django.urls import path

from .views import (
    BillingCreateAPIView,
    BillingListAPIView,
    BillingRetrieveAPIView,
    BillingUpdateAPIView,
    BillingDeleteAPIView,
)

urlpatterns = [

    path(
        "create/",
        BillingCreateAPIView.as_view(),
        name="billing-create",
    ),

    path(
        "",
        BillingListAPIView.as_view(),
        name="billing-list",
    ),

    path(
        "<int:pk>/",
        BillingRetrieveAPIView.as_view(),
        name="billing-detail",
    ),

    path(
        "<int:pk>/update/",
        BillingUpdateAPIView.as_view(),
        name="billing-update",
    ),

    path(
        "<int:pk>/delete/",
        BillingDeleteAPIView.as_view(),
        name="billing-delete",
    ),

]