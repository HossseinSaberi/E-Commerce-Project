from django.urls import path
from .views import MainManagerPage , CreateShop , DeleteShop , EditShop , CreateProduct , CreateCategory , ShowAllCategory , DeleteCategory , EditCategory
from .views import CreateTag , ShowAllTag , EditTag , DeleteTag , EditProduct , ShowAllProduct , DeleteProduct

urlpatterns = [
    path('/' , MainManagerPage.as_view() , name='Manager'),
    path('/AddShop' , CreateShop.as_view()),
    path('/<int:pk>/DeleteShop', DeleteShop.as_view() , name='DeleteShop'),
    path('/<int:pk>/EditShop', EditShop.as_view() , name='EditShop'),
    path('/AddProduct/', CreateProduct.as_view() , name='AddProduct'),
    path('/<int:pk>/EditProduct/', EditProduct.as_view() , name='EditProduct'),
    path('/<int:pk>/DeleteProduct/', DeleteProduct.as_view() , name='DeleteProduct'),
    path('/AddCategory/', CreateCategory.as_view() , name='AddCategory'),
    path('/ListProduct/', ShowAllProduct.as_view() , name='ListProduct'),
    path('/ListCategory/', ShowAllCategory.as_view() , name='ListCategory'),
    path('/<int:pk>/DeleteCategory/', DeleteCategory.as_view() , name='DeleteCategory'),
    path('/<int:pk>/EditCategory/', EditCategory.as_view() , name='EditCategory'),
    path('/ListTag/', ShowAllTag.as_view() , name='ListTag'),
    path('/AddTag/', CreateTag.as_view() , name='AddTag'),
    path('/<int:pk>/EditTag/', EditTag.as_view() , name='EditTag'),
    path('/<int:pk>/DeleteTag/', DeleteTag.as_view() , name='DeleteTag'),
]