from django.urls import path
from .views import CreditListCreateView, CreditDetailView

app_name = 'credits'

urlpatterns = [
    path('api/credits/', CreditListCreateView.as_view(), name='credit-list-create'),
    path('api/credits/<int:pk>/', CreditDetailView.as_view(), name='credit-detail'),
    path('api/credits/<int:pk>/close/', CreditDetailView.as_view(), name='credit-close'),
]
