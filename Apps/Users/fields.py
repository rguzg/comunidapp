from django.forms import Select
from typing import Union, Set, Optional, Any, Dict

# Extensión del Select normal de Django que añade a los data-attributes de cada elemento del select el pais al que pertenece el estado.
# Esto se utiliza en el front-end para solo mostrar los estados que le pertenezcan al país seleccionado.
class EstadoSelect(Select):
    def create_option(self, name: str, value: Any, label: Union[int, str], selected: Union[Set[str], bool], index: int, subindex: Optional[int], attrs: Optional[Any]) -> Dict[str, Any]:
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)

        if(value):
            option['attrs']['data-pais'] = value.instance.pais

        return option

# Extensión del Select normal de Django que añade a los data-attributes de cada elemento del select el estado al que pertenece la ciudad.
# Esto se utiliza en el front-end para solo mostrar las ciudades que le pertenezcan al estado selecionado.
class CiudadSelect(Select):
    def create_option(self, name: str, value: Any, label: Union[int, str], selected: Union[Set[str], bool], index: int, subindex: Optional[int], attrs: Optional[Any]) -> Dict[str, Any]:
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)

        if(value):
            option['attrs']['data-estado'] = value.instance.estado

        return option