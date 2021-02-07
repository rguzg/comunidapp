const palabras_clave = document.querySelector('#pills_palabras');
PillsBox(palabras_clave, 'palabras');

const lineas_investigacion = document.querySelector('#pills_lineas');
PillsBox(lineas_investigacion, 'lineas');

const form = document.querySelector('form');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    let data = CreateFormData(form);

        // Añadir los valores de los PillsBox
        let pills_lineas = lineas_investigacion.querySelectorAll('.m-pills');
        let lineas_array = [];
    
        pills_lineas.forEach(element => {
            lineas_array.push(JSON.stringify({
                id: element.dataset.id,
                nombre: element.firstChild.textContent
             }));
        });
        data.append("lineas", lineas_array);
    
        // El pill_input de niveles no está en todos los forms de AgregarProducto
        if(palabras_clave){
            let pills_palabras = palabras_clave.querySelectorAll('.m-pills');
            let palabras_array = [];
        
            pills_palabras.forEach(element => {
               palabras_array.push(JSON.stringify({
                   id: element.dataset.id,
                   nombre: element.firstChild.textContent
                }));
            });
            data.append("palabras", palabras_array);
        }

        try {
            await fetch('/proxy', {
                method: 'POST',
                body: data
            }).then(() => {
                // location.reload();
            })
        } catch (error) {
            console.error("Error mandando la actualización de perfil");
        }
})