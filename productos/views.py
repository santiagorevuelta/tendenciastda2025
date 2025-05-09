from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Producto, Categoria, Inventario
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings
from .serializers import ProductoSerializer, CategoriaSerializer, InventarioSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
import sys

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

@login_required
def dashboard(request):
    if request.user.profile.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.profile.role == 'employee':
        return redirect('empleado_dashboard')
    else:
        return redirect('login')

@login_required
def admin_dashboard(request):
    if request.user.profile.role != 'admin':
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    productos = Producto.objects.all()
    return render(request, 'admin_dashboard.html', {'productos': productos})


@login_required
def empleado_dashboard(request):
    if request.user.profile.role != 'employee':
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    inventarios = Inventario.objects.all()
    return render(request, 'empleado_dashboard.html', {'inventarios': inventarios})


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    @swagger_auto_schema(
        operation_description="Listar todas las categorías disponibles.",
        responses={
            200: openapi.Response(
                description="Lista de categorías obtenida correctamente.",
                schema=CategoriaSerializer(many=True)
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crear una nueva categoría.",
        responses={
            201: openapi.Response(
                description="Categoría creada correctamente.",
                schema=CategoriaSerializer
            ),
            400: "Solicitud incorrecta. Verifique los datos enviados.",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtener una categoría específica por su ID.",
        responses={
            200: openapi.Response(
                description="Categoría obtenida correctamente.",
                schema=CategoriaSerializer
            ),
            404: "No encontrado. La categoría con el ID especificado no existe.",
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar una categoría específica por su ID.",
        responses={
            200: openapi.Response(
                description="Categoría actualizada correctamente.",
                schema=CategoriaSerializer
            ),
            400: "Solicitud incorrecta. Verifique los datos enviados.",
            404: "No encontrado. La categoría con el ID especificado no existe.",
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente una categoría específica por su ID.",
        responses={
            200: openapi.Response(
                description="Categoría actualizada correctamente.",
                schema=CategoriaSerializer
            ),
            400: "Solicitud incorrecta. Verifique los datos enviados.",
            404: "No encontrado. La categoría con el ID especificado no existe.",
        }   
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Eliminar una categoría específica por su ID.",
        responses={
            204: "Categoría eliminada correctamente.",
            404: "No encontrado. La categoría con el ID especificado no existe.",
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_permissions(self):
        if getattr(settings, 'TESTING', False):
         return[AllowAny()]

    @swagger_auto_schema(
        operation_description="Listar todos los productos disponibles (requiere autenticación JWT).",
        responses={
            200: openapi.Response(
                description="Lista de productos obtenida correctamente.",
                schema=ProductoSerializer(many=True)
            ),
            401: "No autorizado. El token JWT no está presente o es inválido.",
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crear un nuevo producto (requiere autenticación JWT).",
        
        responses={
            201: openapi.Response(
                description="Producto creado correctamente.",
                schema=ProductoSerializer
            ),
            400: "Solicitud incorrecta. Verifique los datos enviados.",
            401: "No autorizado. El token JWT no está presente o es inválido.",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Obtener un producto específico por su ID (requiere autenticación JWT).",
        responses={
            200: openapi.Response(
                description="Producto obtenido correctamente.",
                schema=ProductoSerializer
            ),
            404: "No encontrado. El producto con el ID especificado no existe.",
            401: "No autorizado. El token JWT no está presente o es inválido.",
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar un producto específico por su ID (requiere autenticación JWT).",
        responses={
            200: openapi.Response(
                description="Producto actualizado correctamente.",
                schema=ProductoSerializer
            ),
            400: "Solicitud incorrecta. Verifique los datos enviados.",
            404: "No encontrado. El producto con el ID especificado no existe.",
            401: "No autorizado. El token JWT no está presente o es inválido.",
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Actualizar parcialmente un producto específico por su ID (requiere autenticación JWT).",
        responses={
            200: openapi.Response(
                description="Producto actualizado correctamente.",
                schema=ProductoSerializer
            ),
            400: "Solicitud incorrecta. Verifique los datos enviados.",
            404: "No encontrado. El producto con el ID especificado no existe.",
            401: "No autorizado. El token JWT no está presente o es inválido.",
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Eliminar un producto específico por su ID (requiere autenticación JWT).",
        responses={
            204: "Producto eliminado correctamente.",
            404: "No encontrado. El producto con el ID especificado no existe.",
            401: "No autorizado. El token JWT no está presente o es inválido.",
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

    def perform_create(self, serializer):
        inventario = serializer.save()
        producto = inventario.producto
        if inventario.tipo == 'entrada':
             producto.stock += inventario.cantidad
        elif inventario.tipo == 'salida':
             if producto.stock >= inventario.cantidad:
                producto.stock -= inventario.cantidad
        producto.save()