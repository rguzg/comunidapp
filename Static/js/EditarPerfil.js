const lineas_investigacion = new PillsBox(document.querySelector('#pills_lineas'), 'lineas');

const niveles = new PillsBox(document.querySelector('#pills_niveles'), 'niveles');

const facultades = new PillsBox(document.querySelector('#pills_facultades'), 'facultades');

const form = document.querySelector('#perfilForm');
const boton_submit = form.querySelector('input[type="submit"]');

const notification_controller = new NotificationController('bottom-right');

VerificarForm(form, boton_submit, [lineas_investigacion, niveles, facultades]);

/* Para poder enviar los datos que hay en los PillsBox.
JavaScript se va a encargar de crear el formdata que se le va a enviar al servidor. */
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    let data = CreateFormData(form);
    
    // Añadir los valores de los PillsBox
    data.append("lineas", JSON.stringify(await lineas_investigacion.pills));
    data.append("niveles", JSON.stringify(await niveles.pills));        
    data.append("facultades", JSON.stringify(await facultades.pills));

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
            notification_controller.ShowNotification("", message.body_text, {type: message.type, autohide: false})
        } catch (error) {
            console.error(error);
        }

    } catch (error) {
        console.error(`Error mandando la actualización de perfil ${error}`);
    }

});

