const lineas_investigacion = document.querySelector('#pills_lineas');
PillsBox(lineas_investigacion, 'lineas');

const niveles = document.querySelector('#pills_niveles');
PillsBox(niveles, 'niveles');

const facultades = document.querySelector('#pills_facultades');
PillsBox(facultades, 'facultades');

const form = document.querySelector('#perfilForm')

/* Para poder enviar los datos que hay en los PillsBox, 
JavaScript se va a encargar de crear el formdata que se le va a enviar al servidor. */
form.addEventListener('submit', (event) => {
    let data = CreateFormData(form);

    // Añadir los valores de los PillsBox
    let pills_lineas = lineas_investigacion.querySelectorAll('.m-pills');
    pills_lineas.forEach(element => {
       data.append("lineas", JSON.stringify({
           id: element.dataset.id,
           nombre: element.firstChild.textContent
        }));
    });

    let pills_niveles = niveles.querySelectorAll('.m-pills');
    pills_niveles.forEach(element => {
       data.append("niveles", JSON.stringify({
           id: element.dataset.id,
           nombre: element.firstChild.textContent
        }));
    });

    let pills_facultades = facultades.querySelectorAll('.m-pills');
    pills_facultades.forEach(element => {
       data.append("facultades", JSON.stringify({
           id: element.dataset.id,
           nombre: element.firstChild.textContent
        }));
    });

    let request = new XMLHttpRequest();

    request.open('POST', '/profile');
    request.send(data);

    event.preventDefault();
});

