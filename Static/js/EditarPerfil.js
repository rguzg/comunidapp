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
    console.log(event);
    event.preventDefault();
})

