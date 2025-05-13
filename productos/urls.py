from django.urls import path, include
from rest_framework import routers
from .views import ProductoViewSet, CategoriaViewSet, InventarioViewSet
from . import views

router = routers.DefaultRouter()
router.register('productos', ProductoViewSet)
router.register('categorias', CategoriaViewSet)
router.register('inventarios', InventarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('inicio/', views.initial_view, name='initial'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('empleado-dashboard/', views.empleado_dashboard, name='empleado_dashboard'),
    path('exportar-inventarios-pdf/', views.exportar_inventarios_pdf, name='exportar_inventarios_pdf'),
    path('exportar-productos-pdf/', views.exportar_productos_pdf, name='exportar_productos_pdf'),
]