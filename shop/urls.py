from django.urls import path
from shop import views
from utils.constans import LIST_CREATE, RETRIEVE_UPDATE_DESTROY

urlpatterns = [
    path('api/v1/categories/', views.category_list_create_api_view),
    path('api/v1/categories/<int:id>/', views.category_detail_api_view),
    path('api/v1/products/', views.product_list_create_api_view),
    path('api/v1/products/<int:id>/', views.product_detail_api_view),
    path('api/v1/reviews/', views.review_list_create_api_view),
    path('api/v1/reviews/<int:id>/', views.review_detail_api_view),
    path('api/v1/products/reviews/', views.product_list_create_api_view),
]