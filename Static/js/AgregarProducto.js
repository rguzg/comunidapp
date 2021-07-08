const palabras_clave_contenedor = document.querySelector('#pills_palabras');
const paises_select = document.querySelector('#id_pais');
const estadosP_select = document.querySelector('#id_estadoP');
const ciudades_select = document.querySelector('#id_ciudad');

let palabras_clave = null;

if(palabras_clave_contenedor){
    palabras_clave = new PillsBox(palabras_clave_contenedor, 'palabras', false);
}

const lineas_investigacion = new PillsBox(document.querySelector('#pills_lineas'), 'lineas', false);

const form = document.querySelector('form');
const boton_submit = form.querySelector('input[type="submit"]');

const notification_controller = new NotificationController('bottom-right');

/**
 * Esconde los estados cuyos atributo data-pais no sea pais
 * @param {String} pais 
 */
const HideEstados = (pais) => {
    let estados = estadosP_select.options;

    // Se empieza con el segundo elemento de estados porque el primero es el placeholder cuando nada está seleccionado
    for (let i = 1; i < estados.length; i++) {
        if(estados[i].dataset.pais == pais){
            estados[i].classList.remove('h-display-none');
        } else {
            estados[i].classList.add('h-display-none');
        }
    }
}

/**
 * Esconde las ciudades cuyos atributo data-pais no sea estado
 * @param {String} estado 
 */
const HideCiudades = (estado) => {
    let ciudades = ciudades_select.options;

    // Se empieza con el segundo elemento de estados porque el primero es el placeholder cuando nada está seleccionado
    for (let i = 1; i < ciudades.length; i++) {
        if(ciudades[i].dataset.estado == estado){
            ciudades[i].classList.remove('h-display-none');
        } else {
            ciudades[i].classList.add('h-display-none');
        }
    }
}

VerificarForm(form, boton_submit, [palabras_clave, lineas_investigacion]);

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Después de hacer click, se deshabilitará el boton de submit por 5 segundos (o hasta que se complete la petición) para evitar peticiones repetidas
    boton_submit.setAttribute('disabled', '');

    setTimeout(() => {
        boton_submit.removeAttribute('disabled', '');
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

if(estadosP_select && ciudades_select){
    // Esconder todas los estados y ciudades
    HideEstados("");
    HideCiudades("");

    paises_select.addEventListener('input', () => {
        let selected_pais_nombre = paises_select.options[paises_select.selectedIndex].innerText;
        let selected_estadoP = estadosP_select.options[estadosP_select.selectedIndex]
        
        HideEstados(selected_pais_nombre);

        // Quitar el estado seleccionado actual si ese estado no existe en el nuevo pais seleccionado 
        if(selected_estadoP.dataset.pais != selected_pais_nombre){
            estadosP_select.value = "";
        } 
        estadosP_select.dispatchEvent(new Event('input'));
    });

    estadosP_select.addEventListener('input', () => {
        let selected_estado_nombre = estadosP_select.options[estadosP_select.selectedIndex].innerText;
        let selected_ciudad = ciudades_select.options[ciudades_select.selectedIndex]
        
        HideCiudades(selected_estado_nombre);

        // Quitar la ciudad seleccionado actual si esa ciudad no existe en el nuevo estado seleccionado 
        if(selected_ciudad.dataset.estado != selected_estado_nombre){
            ciudades_select.value = "";
        } 
    });
}