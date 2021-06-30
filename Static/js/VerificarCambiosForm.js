/*
    Esta función agrega o quita el atributo disabled de boton_submit dependiendo de si los valores del form han cambiado o no
*/

const VerificarCambiosForm = (form, boton_submit, pill_inputs = null) => {
    if(form instanceof HTMLFormElement){
        let original_values = {};
        let current_values = {};

        // Verificación de los valores que son inputs
        for (let i = 0; i < form.elements.length; i++){
            let element = form.elements[i];
        
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
        
        if(pill_inputs){            
            pill_inputs.forEach(async (pill_input) => {
                if(pill_input != null){
                    let original_pills = await pill_input.pills;

                    pill_input.container.addEventListener('change', async () => {
                        let shouldDisableButton = true;
                        let current_pills = await pill_input.pills;

                        if(current_pills.length != original_pills.length){
                            shouldDisableButton = false;
                        } else {
                            // Los arreglos de pills se ordenan alfabeticamente para comprobar que no estén insertadas las mismas pills, 
                            // aunque esten en diferente orden. Solo es necesario realizar esta comprobación cuando 
                            // current_pills.length != original_pills.length
                            current_pills.sort();
                            original_pills.sort();

                            for (let i = 0; i < current_pills.length; i++) {
                                if(current_pills[i].name != original_pills[i].name){
                                    shouldDisableButton = false;
                                    break;
                                }
                            }
                        }

                        if(!pill_input.isValid()){
                            shouldDisableButton = true;
                        }

                        if(shouldDisableButton){
                            boton_submit.setAttribute('disabled', '');
                        } else {
                            boton_submit.removeAttribute('disabled');
                        }
                    });
                }
            });
        }
    } else {
        throw new TypeError("form debe ser un HTMLFormElement")
    }
}