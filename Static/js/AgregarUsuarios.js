let lineas_investigacion;
let niveles;
let facultades;

// La view de Agregar Usuarios tiene dos pestañas, una donde no hay input pills y otra donde están las tres, 
// entonces si una está presente, no tiene caso checar las demás
if(document.querySelector('#pills_lineas')){
    lineas_investigacion = new PillsBox(document.querySelector('#pills_lineas'), 'lineas', false);
    niveles = new PillsBox(document.querySelector('#pills_niveles'), 'niveles', false);
    facultades = new PillsBox(document.querySelector('#pills_facultades'), 'facultades', false);
}

const form = document.querySelector('form');
const boton_submit = form.querySelector('input[type="submit"]');

const notification_controller = new NotificationController('bottom-right');

VerificarForm(form, boton_submit, [lineas_investigacion, niveles, facultades]);

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    let data = CreateFormData(form);

    if(!lineas_investigacion){
        data.append("email", '');
    }
    
    // La view de Agregar Usuarios tiene dos pestañas, una donde no hay input pills y otra donde están las tres, 
    // entonces si una está presente, no tiene caso checar las demás
    if(lineas_investigacion){
        // Añadir los valores de los PillsBox

        data.append("lineas", JSON.stringify(await lineas_investigacion.pills));
        data.append("niveles", JSON.stringify(await niveles.pills));
        data.append("facultades", JSON.stringify(await facultades.pills));
    }
    
    try {
        let request = await fetch('/proxy', {
            method: 'POST',
            body: data,
            headers: {
                'PROXY': document.location.pathname
            }
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
        console.log(`Error agregando usuario: ${error}`);
    }
});
