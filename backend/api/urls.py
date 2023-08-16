from django.urls import path,include
from api import views
from .views import RegisterAPI
from knox import views as knox_views
from .views import LoginAPI

urlpatterns = [
    # path('user/', views.UserList.as_view())
    path('', views.apiOverview, name="api-overview"),
    path('restaurants-list/', views.restaurantList, name="restaurants-list"),
    path('restaurants-detail/<str:pk>/', views.restaurantDetail, name="restaurants-detail"),
    path('restaurants-create/', views.restaurantCreate, name="restaurants-create"),
    path('restaurants-update/<str:pk>/', views.restaurantUpdate, name="restaurants-update"),
    path('restaurants-delete/<str:pk>/', views.restaurantDelete, name="restaurants-delete"),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('verify/<token>',views.verify, name='verify'),
    path('menus-list/', views.menuList, name="menus-list"),
    path('menus-create/', views.menuCreate, name="menus-create"),
    path('menus/<str:pk>/', views.menu, name="menus"),
    path('contact-create/', views.contactCreate, name="contact-create"),
    path('menu-delete/<str:pk>/', views.menuDelete, name="menus-delete"),
    path('menu-update/<str:pk>/', views.menuUpdate, name="menus-update"),
    path('profile/<int:pk>/', views.profile, name="profile"),
    path('place-order/',views.placeOrder, name="place-order"),
    path('profilecreate/',views.profileCreate, name="profileCreate"),
    path('profileupdate/<str:pk>/',views.profileUpdate, name="profileupdate"),
    path('reviewDetails/<str:pk>/',views.reviewDetail, name="profileupdate"),
    path('postreview/',views.postReview, name="postreview"),
    path('reviewdelete/<str:pk>/', views.reviewDelete, name="reviewdelete"),
    path('order-list/', views.orderList, name="order-list"),
    path('order-list/<int:pk>/', views.orderListOfUser, name="order-list-user"),
    path('order-detail/<str:pk>/', views.orderDetail, name="order-detail"),
    path('order/<str:pk>/', views.order, name="order"),


]
