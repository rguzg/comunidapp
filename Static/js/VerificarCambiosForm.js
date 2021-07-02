/*
    Esta función agrega o quita el atributo disabled de boton_submit dependiendo de si los valores del form han cambiado o no y de que si la form es valida o no.
*/

const VerificarForm = (form, boton_submit, pill_inputs = null) => {
    if(form instanceof HTMLFormElement){
        let original_values = {};
        let original_pills = [];

        // Verificación de los valores que son inputs
        for (let i = 0; i < form.elements.length; i++){
            let element = form.elements[i];

            if( element.type != "submit" && element.type != "button" 
            && element.name != "csrfmiddlewaretoken" && element.name != "user" && element.name != "input_pill"){
                if(element.type == "checkbox"){
                    original_values[element.name] = element.checked;
                } else {
                    original_values[element.name] = element.value;
                }
            }

            element.addEventListener('input', async () => {
                let current_values = {};

                for (let i = 0; i < form.elements.length; i++){
                    let element = form.elements[i];
        
                    if( element.type != "submit" && element.type != "button" 
                    && element.name != "csrfmiddlewaretoken" && element.name != "user" && element.name != "input_pill"){
                        if(element.type == "checkbox"){
                            current_values[element.name] = element.checked;
                        } else {
                            current_values[element.name] = element.value;
                        }
                    }
                }

                let [hasInputPillsChanged, hasErrors] = await VerificarInputPills(original_pills, pill_inputs);
                let hasInputChanged = VerificarInputs(original_values, current_values);

                if(hasErrors){
                    boton_submit.setAttribute('disabled', '');
                } else {
                    if(hasInputChanged || hasInputPillsChanged){
                        boton_submit.removeAttribute('disabled');
                    } else {
                        boton_submit.setAttribute('disabled', '');
                    }
                }
            });
        }
        
        if(pill_inputs){
            pill_inputs.forEach(async (pill_input) => {
                if(pill_input != null){
                    let pill_names = [];
                    let pills = await pill_input.pills;
            
                    pills.forEach((pill) => {
                        pill_names.push(pill.name);
                    });
                    
                    pill_names.sort();
                    original_pills.push(pill_names);

                    pill_input.container.addEventListener('change', async () => {
                        let current_values = {};

                        for (let i = 0; i < form.elements.length; i++){
                            let element = form.elements[i];
                
                            if( element.type != "submit" && element.type != "button" 
                            && element.name != "csrfmiddlewaretoken" && element.name != "user" && element.name != "input_pill"){
                                if(element.type == "checkbox"){
                                    current_values[element.name] = element.checked;
                                } else {
                                    current_values[element.name] = element.value;
                                }
                            }
                        }
        
                        let [hasInputPillsChanged, hasErrors] = await VerificarInputPills(original_pills, pill_inputs);
                        let hasInputChanged = VerificarInputs(original_values, current_values);

                        if(hasErrors){
                            boton_submit.setAttribute('disabled', '');
                        } else {
                            if(hasInputChanged || hasInputPillsChanged){
                                boton_submit.removeAttribute('disabled');
                            } else {
                                boton_submit.setAttribute('disabled', '');
                            }
                        }
                            });
                        }
                    });
        }
    } else {
        throw new TypeError("form debe ser un HTMLFormElement")
    }
}

const VerificarInputs = (original_values, current_values) => {
    let hasInputChangedMatrix = [];
    let hasChanged = false;

    for (const key in original_values) {
        // Si al menos un input cambió, entonces se considera que los inputs han cambiado
        if(current_values[key] && original_values[key] != current_values[key]){
            hasInputChangedMatrix.push(true);
            break;
        } else {
            hasInputChangedMatrix.push(false);
        }
    }

    hasInputChangedMatrix.forEach((hasInputChanged) => {
        hasChanged |= hasInputChanged;
    });

    return hasChanged;
}

const VerificarInputPills = async (original_pills, pill_inputs) => {
    if(original_pills == []){
        return [true, true];
    }

    let current_pills = [];

    for (let i = 0; i < pill_inputs.length; i++) {
        const pill_input = pill_inputs[i];
 
        if(pill_input){
            let pill_names = [];
            let pills = await pill_input.pills;
    
            pills.forEach((pill) => {
                pill_names.push(pill.name);
            });
            
            current_pills.push(pill_names);
        }
    }
        
    // Se almacenan todos los valores de si los pill_inputs son validos y si no tienen los mismos contenidos que al principio. 

    // Al final si al menos uno de estos valores es falso, boton_submit se deshabilita
    let errorsMatrix = [];
    // Al final si nada ha cambiado, boton_submit se deshabilita
    let hasChangedMatrix = [];

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
        if(pill_inputs[i]){
            errorsMatrix.push(pill_inputs[i].isValid());
        }
    }

    let haveInputsChanged = false;
    let hasErrors = errorsMatrix.includes(false);
    
    hasChangedMatrix.forEach((hasChanged) => {
        haveInputsChanged |= hasChanged;
    });

   return [haveInputsChanged, hasErrors];
}