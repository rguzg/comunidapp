const form = document.querySelector('#perfilForm');
const boton_submit = form.querySelector('input[type="submit"]');

const notification_controller = new NotificationController('bottom-right');

VerificarCambiosForm(form, boton_submit);

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    let data = CreateFormData(form);

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

