const lineas_investigacion = document.querySelector('#pills_lineas');
PillsBox(lineas_investigacion, 'lineas');

const niveles = document.querySelector('#pills_niveles');
PillsBox(niveles, 'niveles');

const facultades = document.querySelector('#pills_facultades');
PillsBox(facultades, 'facultades');

const form = document.querySelector('#perfilForm')

/* Para poder enviar los datos que hay en los PillsBox, 
JavaScript se va a encargar de crear el formdata que se le va a enviar al servidor. */
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

    let pills_niveles = niveles.querySelectorAll('.m-pills');
    let niveles_array = [];

    pills_niveles.forEach(element => {
       niveles_array.push(JSON.stringify({
           id: element.dataset.id,
           nombre: element.firstChild.textContent
        }));
    });
    data.append("niveles", niveles_array);

    let pills_facultades = facultades.querySelectorAll('.m-pills');
    let facultades_array = [];

    pills_facultades.forEach(element => {
       facultades_array.push(JSON.stringify({
           id: element.dataset.id,
           nombre: element.firstChild.textContent
        }));
    });
    data.append("facultades", facultades_array);

    try {
        await fetch('/proxy', {
            method: 'POST',
            body: data
        }).then(() => {
            location.reload();
        })
    } catch (error) {
        console.error("Error mandando la actualización de perfil");
    }

});

