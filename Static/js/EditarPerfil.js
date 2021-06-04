const lineas_investigacion = document.querySelector('#pills_lineas');
PillsBox(lineas_investigacion, 'lineas');

const niveles = document.querySelector('#pills_niveles');
PillsBox(niveles, 'niveles');

const facultades = document.querySelector('#pills_facultades');
PillsBox(facultades, 'facultades');

const form = document.querySelector('#perfilForm');
const boton_submit = form.querySelector('input[type="submit"]');

const notification_controller = new NotificationController('bottom-right');

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
        let message = ExtractMessageFromDOM(messageDOM);

        try {
            notification_controller.ShowNotification("", message.body_text, {type: message.type, delay: 10000})
        } catch (error) {
            console.error(error);
        }

    } catch (error) {
        console.error(`Error mandando la actualización de perfil ${error}`);
    }

});

