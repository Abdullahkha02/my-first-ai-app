from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect  # Add this
from core.api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    # Redirect the empty home page to our API docs
    path("", lambda request: redirect("api/docs")),
]
