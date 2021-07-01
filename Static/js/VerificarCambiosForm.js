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
            && element.name != "csrfmiddlewaretoken" && element.name != "user" && element.name != "input_pill"){
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
            let original_pills = [];
            
            pill_inputs.forEach(async (pill_input) => {
                if(pill_input != null){
                    original_pills.push(await pill_input.pills);
                    original_pills.sort();

                    pill_input.container.addEventListener('change', async () => {
                        let current_pills = [];

                        // Se almacenan todos los valores de si los pill_inputs son validos y si no tienen los mismos contenidos que al principio. 

                        // Al final si al menos uno de estos valores es falso, boton_submit se deshabilita
                        let isValidMatrix = [];
                        // Al final si nada ha cambiado, boton_submit se deshabilita
                        let hasChangedMatrix = [];

                        pill_inputs.forEach((pill_input) => {
                            current_pills.push(pill_input.pills);
                        });

                        for (let i = 0; i < current_pills.length; i++) {
                            current_pills[i] = await current_pills[i];
                            let hasChanged = false;

                            if(current_pills[i].length != original_pills[i].length){
                                hasChanged = true;
                            } else {
                                // Los arreglos de pills se ordenan alfabeticamente para comprobar que no estén insertadas las mismas pills, 
                                // aunque esten en diferente orden. Solo es necesario realizar esta comprobación cuando 
                                // current_pills.length != original_pills.length
                                current_pills[i].sort();
    
                                for (let j = 0; j < current_pills[i].length; j++) {
                                    if(current_pills[i][j] != original_pills[i][j]){
                                        hasChanged = true;
                                        break;
                                    }
                                }
                            }

                            hasChangedMatrix.push(hasChanged);
                            isValidMatrix.push(pill_input.isValid());
                        }

                        let shouldDisable = false;

                        if(isValidMatrix.includes(false)){
                            shouldDisable = true;
                        } else {
                            let haveInputsChanged = false;

                            hasChangedMatrix.forEach((hasChanged) => {
                                haveInputsChanged |= hasChanged;
                            });

                            shouldDisable = !haveInputsChanged;
                        }

                        if(shouldDisable){
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