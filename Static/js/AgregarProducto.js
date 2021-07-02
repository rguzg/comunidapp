const palabras_clave_contenedor = document.querySelector('#pills_palabras');

let palabras_clave = null;

if(palabras_clave_contenedor){
    palabras_clave = new PillsBox(palabras_clave_contenedor, 'palabras', false);
}

const lineas_investigacion = new PillsBox(document.querySelector('#pills_lineas'), 'lineas', false);

const form = document.querySelector('form');
const boton_submit = form.querySelector('input[type="submit"]');

const notification_controller = new NotificationController('bottom-right');

VerificarForm(form, boton_submit, [palabras_clave, lineas_investigacion]);

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Después de hacer click, se deshabilitará el boton de submit por 5 segundos (o hasta que se complete la petición) para evitar peticiones repetidas
    boton_submit.setAttribute('disabled', '');

    setTimeout(() => {
        boton_submit.removeAttribute('disabled', '');
        console.log("A");
    }, 50000);

    let data = CreateFormData(form);

    data.append("lineas", JSON.stringify(await lineas_investigacion.pills));
    
        // El pill_input de niveles no está en todos los forms de AgregarProducto
        if(palabras_clave){
            data.append("palabras", JSON.stringify(await palabras_clave.pills));
        }

        try {
            let request = await fetch('/proxy', {
                method: 'POST',
                headers: {
                    'PROXY': document.location.pathname
                },
                body: data
            });

            let html = await request.text();

            let messageDOM = new DOMParser().parseFromString(html, 'text/html');
            let message = ExtractMessageFromDOM(messageDOM);

            try {
                notification_controller.ShowNotification("", message.body_text, {type: message.type, autohide: false})
            } catch (error) {
                console.error(error);
            }

            // Como esto está después de varios awaits, no se ejecutará hasta que todas esas promesas se cumplan
            boton_submit.removeAttribute('disabled', '');

        } catch (error) {
            console.error(`Error agregando producto ${error}`);
        }
})