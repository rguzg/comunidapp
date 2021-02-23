const lineas_investigacion = document.querySelector('#pills_lineas');
const niveles = document.querySelector('#pills_niveles');
const facultades = document.querySelector('#pills_facultades');

// La view de Agregar Usuarios tiene dos pestañas, una donde no hay input pills y otra donde están las tres, 
// entonces si una está presente, no tiene caso checar las demás
if(lineas_investigacion){
    PillsBox(lineas_investigacion, 'lineas');
    PillsBox(niveles, 'niveles');
    PillsBox(facultades, 'facultades');
}

const form = document.querySelector('form');
const boton_submit = form.querySelector('input[type="submit"]');

VerificarCambiosForm(form, boton_submit, [lineas_investigacion, niveles, facultades]);

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    let data = CreateFormData(form);
    
    // La view de Agregar Usuarios tiene dos pestañas, una donde no hay input pills y otra donde están las tres, 
    // entonces si una está presente, no tiene caso checar las demás
    if(lineas_investigacion){
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
        document.querySelector('#messages').replaceWith(messageDOM.querySelector('#messages'));

    } catch (error) {
        console.log(`Error agregando usuario: ${error}`);
    }
});
