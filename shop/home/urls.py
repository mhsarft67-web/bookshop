from django.urls import path
from . import views
app_name = 'home'

urlpatterns = [

    path('' , views.HomeView.as_view()  , name = 'home'),
    path('<int:product_id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('reply/<int:product_id>/<int:comment_id>/', views.ProductAddReplyView.as_view(), name="add_reply"),


]