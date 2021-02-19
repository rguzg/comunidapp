/*
    Esta función agrega o quita el atributo disabled de boton_submit dependiendo de si los valores del form han cambiado o no
*/

const VerificarCambiosForm = (form, boton_submit, pill_inputs) => {
    if(form instanceof HTMLFormElement){
        let original_values = {};
        let current_values = {};

        // Verificación de los valores que son inputs
        for (let i = 0; i < form.elements.length; i++){
            let element = form.elements[i];
        
            if( element.type != "submit" && element.type != "button" 
            && element.name != "csrfmiddlewaretoken" && element.name != "user"){
                element.addEventListener('input', () => {
                    current_values[element.name] = element.value;
                    
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
        
                original_values[element.name] = element.value;
            }    
        }
        
        // Quitar el atributo disabled de boton_submit si se elimina una pill que no fue agregada por el usuario
        pill_inputs.forEach((pill_input) => {
            pill_input.addEventListener('pill_deleted', ((event) => {
                boton_submit.removeAttribute('disabled');
            }));
        });
    } else {
        throw new TypeError("form debe ser un HTMLFormElement")
    }
}

const lineas_investigacion = document.querySelector('#pills_lineas');
PillsBox(lineas_investigacion, 'lineas');

const niveles = document.querySelector('#pills_niveles');
PillsBox(niveles, 'niveles');

const facultades = document.querySelector('#pills_facultades');
PillsBox(facultades, 'facultades');

const form = document.querySelector('#perfilForm');
const boton_submit = form.querySelector('input[type="submit"]');

VerificarCambiosForm(form, boton_submit, [lineas_investigacion, niveles, facultades]);

/* Para poder enviar los datos que hay en los PillsBox.
JavaScript se va a encargar de crear el formdata que se le va a enviar al servidor. */
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    let data = CreateFormData(form);
    
    // Añadir los valores de los PillsBox
    let pills_lineas = lineas_investigacion.querySelectorAll('.m-pills');

    if(pills_lineas.length != 0){
        let lineas_array = [];
    
        pills_lineas.forEach(element => {
            lineas_array.push(JSON.stringify({
                id: element.dataset.id,
                nombre: element.firstChild.textContent
             }));
        });
        data.append("lineas", lineas_array);
    }

    let pills_niveles = niveles.querySelectorAll('.m-pills');
    if(pills_niveles.length != 0){
        let niveles_array = [];
    
        pills_niveles.forEach(element => {
           niveles_array.push(JSON.stringify({
               id: element.dataset.id,
               nombre: element.firstChild.textContent
            }));
        });
        data.append("niveles", niveles_array);        
    }

    let pills_facultades = facultades.querySelectorAll('.m-pills');

    if(pills_facultades.length != 0){
        let facultades_array = [];
    
        pills_facultades.forEach(element => {
           facultades_array.push(JSON.stringify({
               id: element.dataset.id,
               nombre: element.firstChild.textContent
            }));
        });
        data.append("facultades", facultades_array);
    }

    try {
        let request = await fetch('/proxy', {
            method: 'POST',
            body: data,
            headers: {
                'PROXY': document.location.pathname
            },
        });

        let html = await request.text();
        
        let messageDOM = new DOMParser().parseFromString(html, 'text/html');
        document.querySelector('#messages').replaceWith(messageDOM.querySelector('#messages'));

    } catch (error) {
        console.error(`Error mandando la actualización de perfil ${error}`);
    }

});

