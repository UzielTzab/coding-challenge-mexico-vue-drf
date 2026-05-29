from django.urls import path
from .views import OpportunityListView, OpportunitySummaryView

urlpatterns = [
    path('', OpportunityListView.as_view(), name='opportunity-list'),
    path('summary/', OpportunitySummaryView.as_view(), name='opportunity-summary'),
]
