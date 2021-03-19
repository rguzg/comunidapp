const agregarEventListenerModales = () => {
    let activeTabpane = document.querySelector('.tab-pane.active');
    let products = activeTabpane.querySelectorAll('.m-product-card');
    
    products.forEach(element => {
        element.addEventListener('click', function(){
            showModal(element);
        });
    });
}

async function showModal(elementoHTML){
    // console.log(elementoHTML);
    // const idProducto = elementoHTML.dataset.idproducto;
    // console.log(idProducto);
    const producto = await getProducto(elementoHTML);

    let lineas = [];
    producto['lineas'].forEach(linea => {
        lineas.push(linea['nombre']);
    })


    let titulo = producto['titulo'] ? producto['titulo'] : 'Sin titulo definido';
    let publicacion = producto['publicacion'] ? producto['publicacion'] : 'Publicación en tramite';

    const modalProducto = document.getElementById('detallesModal');
    modalProducto.getElementsByClassName('modal-title')[0].textContent = titulo;
    modalProducto.getElementsByClassName('modal-date')[0].textContent = 'Publicacion: ' + publicacion;
    modalProducto.getElementsByClassName('modal-colabs')[0].textContent = 'Colaboradores: ' + producto['contribuidores'].join(', ');
    modalProducto.getElementsByClassName('modal-lines')[0].textContent = 'Líneas de Investigacion: ' + lineas.join(', ');
    $('#detallesModal').modal('show');
};

const getProducto = (elementoHTML) => {
    const csrftoken = getCookie('csrftoken');
    const tipoProducto = elementoHTML.dataset.tipoproducto;
    const idProducto = elementoHTML.dataset.idproducto;

    return fetch(server + 'getProducto', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'tipoProducto': tipoProducto,
            'idProducto': idProducto
        })
    })
        .then(res => {
            return res.json();
        })
        .then(res => {
            // console.log(res);
            // res = res;
            return res;
        })
        .catch(err => {
            // console.log(err);
            // res = err;
            return err;
        });
}

// Agrega el eventListener que muestra el modal a todos los productos de la 
// categoria activa

// En el caso de que sea la pestaña que se muestra al entrar a PerfilDetail
window.addEventListener('load', agregarEventListenerModales);
$('a[data-toggle="tab"]').on('shown.bs.tab', agregarEventListenerModales);