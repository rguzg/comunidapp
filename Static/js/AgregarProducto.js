const palabras_clave = document.querySelector('#pills_palabras');

if(palabras_clave){
    PillsBox(palabras_clave, 'palabras', false);
}

const lineas_investigacion = document.querySelector('#pills_lineas');
PillsBox(lineas_investigacion, 'lineas', false);

const form = document.querySelector('form');
const boton_submit = form.querySelector('input[type="submit"]');

VerificarCambiosForm(form, boton_submit, [palabras_clave, lineas_investigacion]);

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
    
        // El pill_input de niveles no está en todos los forms de AgregarProducto
        if(palabras_clave){
            let pills_palabras = palabras_clave.querySelectorAll('.m-pills');
            if(pills_palabras.length != 0){
                let palabras_array = [];
            
                pills_palabras.forEach(element => {
                   palabras_array.push(JSON.stringify({
                       id: element.dataset.id,
                       nombre: element.firstChild.textContent
                    }));
                });
                data.append("palabras", palabras_array);
            }
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
            
            if(messageDOM.querySelector('#messages'));{
                document.querySelector('#messages').replaceWith(messageDOM.querySelector('#messages'));
            }

        } catch (error) {
            console.error(`Error agregando producto ${error}`);
        }
})