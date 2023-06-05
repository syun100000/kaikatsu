from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("calculateFee/", views.calculateFee, name="calculateFee"),
    # path("about/", views.about, name="about"),
    # 他のURLパターンをここに追加する
]