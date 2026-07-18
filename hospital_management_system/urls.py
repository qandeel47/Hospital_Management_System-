
from django.contrib import admin
from django.urls import path, include 
from drf_spectacular.views import ( SpectacularAPIView,SpectacularSwaggerView,SpectacularRedocView,)  
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    #apps urls
    path('admin/', admin.site.urls),
    path("api/users/", include("apps.users.api.urls")),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/departments/", include("apps.departments.api.urls")),
    path("api/doctors/", include("apps.doctors.api.urls")),
    path("api/receptionists/", include("apps.receptionists.api.urls")),
    path("api/patients/", include("apps.patients.api.urls")),
    path("api/appointments/", include("apps.appointments.api.urls")),
    path("api/medical-records/", include("apps.medical_records.api.urls")),
    path("api/prescriptions/", include("apps.prescriptions.api.urls")),
    path("api/billing/", include("apps.billing.api.urls")),
]