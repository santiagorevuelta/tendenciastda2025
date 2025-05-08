from rest_framework import serializers
from .models import Producto, Categoria,Inventario

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria']

class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = ['producto', 'cantidad', 'fecha_actualizacion']
