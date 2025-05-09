from django.urls import path, include
from rest_framework import routers
from .views import ProductoViewSet, CategoriaViewSet, InventarioViewSet
from . import views

router = routers.DefaultRouter()
router.register('Productos', ProductoViewSet)
router.register('Categorias', CategoriaViewSet)
router.register('Inventarios', InventarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('empleado-dashboard/', views.empleado_dashboard, name='empleado_dashboard'),
]