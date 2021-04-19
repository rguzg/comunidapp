# Esta función recibe algún producto y lo analiza para agregar las relaciones que esté creando al modelo
# Relaciones_Profesores
from .models import Autor, Relaciones_Profesores, Articulo, CapituloLibro, Patente, Congreso, Investigacion
from typing import Union

def CrearRelacion(producto: Union[Articulo, CapituloLibro, Patente, Congreso, Investigacion], profesor1: Autor, profesor2: Autor):
    switch_productos = {
        "Articulo": lambda : Relaciones_Profesores.objects.create(profesor1 = profesor1, profesor2 = profesor2, tipo_producto = Relaciones_Profesores.ARTICULO, articulo = producto),
        "Capitulo/Libro": lambda : Relaciones_Profesores.objects.create(profesor1 = profesor1, profesor2 = profesor2, tipo_producto = Relaciones_Profesores.CAPITULO_LIBRO, capituloLibro = producto),
        "Patente": lambda : Relaciones_Profesores.objects.create(profesor1 = profesor1, profesor2 = profesor2, tipo_producto = Relaciones_Profesores.PATENTE, patente = producto),
        "Congreso": lambda : Relaciones_Profesores.objects.create(profesor1 = profesor1, profesor2 = profesor2, tipo_producto = Relaciones_Profesores.CONGRESO, congreso = producto),
        "Investigacion": lambda : Relaciones_Profesores.objects.create(profesor1 = profesor1, profesor2 = profesor2, tipo_producto = Relaciones_Profesores.INVESTIGACION, investigacion = producto),
    }

    switch_productos[producto.TipoProducto]()

def AñadirRelacion(producto: Union[Articulo, CapituloLibro, Patente, Congreso, Investigacion]) -> None:
    # A diferencia de los demas modelos, la propiedad autores es diferente en el modelo Patente
    autores = None

    if(not isinstance(producto, Patente)):
        autores = producto.autores
    else:
        autores = list(producto.autores.all())

    if(len(autores) > 1):
        while(autores):
            for i in range(1,len(autores)):
                CrearRelacion(producto, autores[0], autores[i])
            autores.remove(autores[0])

        


