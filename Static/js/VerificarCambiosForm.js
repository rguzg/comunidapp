/*
    Esta función agrega o quita el atributo disabled de boton_submit dependiendo de si los valores del form han cambiado o no
*/

const VerificarCambiosForm = (form, boton_submit, pill_inputs) => {
    if(form instanceof HTMLFormElement){
        let original_values = {};
        let current_values = {};

        // Verificación de los valores que son inputs
        for (let i = 0; i < form.elements.length; i++){
            let element = form.elements[i]; console.log(element);
        
            if( element.type != "submit" && element.type != "button" 
            && element.name != "csrfmiddlewaretoken" && element.name != "user"){
                element.addEventListener('input', () => {
                    if(element.type == "checkbox"){
                        current_values[element.name] = element.checked;
                    } else {
                        current_values[element.name] = element.value;
                    }
                    
                    for (const key in original_values) {
                        if(original_values[key] != current_values[key]){
                            // Como el valor del input se agrega a current_values cuando su valor cambia, current_value[key] puede ser
                            // igual a undefined si el valor todavía no ha cambiado
                            if(!(current_values[key] == undefined)){
                                boton_submit.removeAttribute('disabled');
                                break;
                            }
                        } else {
                            boton_submit.setAttribute('disabled', '');
                        }
                    }
                });
                
                if(element.type == "checkbox"){
                    original_values[element.name] = element.checked;
                } else {
                    original_values[element.name] = element.value;
                }
            }    
        }
        
        // Quitar el atributo disabled de boton_submit si se elimina una pill que no fue agregada por el usuario
        pill_inputs.forEach((pill_input) => {
            if(pill_input != null){
                pill_input.addEventListener('pill_deleted', ((event) => {
                    boton_submit.removeAttribute('disabled');
                }));
            }
        });
    } else {
        throw new TypeError("form debe ser un HTMLFormElement")
    }
}