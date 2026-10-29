from django.urls import path
from . import views
urlpatterns=[path("api/csrf/",views.csrf),path("api/register/",views.register),path("api/login/",views.login_view),path("api/logout/",views.logout_view),path("api/session/",views.session_view),path("api/cars/",views.cars),path("get_cars/",views.cars),path("get_dealers/",views.dealers),path("api/dealers/",views.dealers),path("api/dealers/<str:dealer_id>/",views.dealer_detail),path("api/dealers/<str:dealer_id>/reviews/",views.reviews),path("api/dealers/<str:dealer_id>/reviews/submit/",views.submit_review),path("api/analyze/",views.analyze),path("analyze/<path:text>/",views.analyze)]

