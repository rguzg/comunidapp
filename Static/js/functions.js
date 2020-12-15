const server = 'http://127.0.0.1:8000/'

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

window.onload = function () {
    // const divSearch = document.getElementsByClassName("bs-searchbox")[0];
    // const inputSearch = divSearch.getElementsByClassName("form-control")[0];
    const dropdown_parent = document.querySelector('#dropdown_parent');
    const logo = document.querySelector('#logo');
    const editar_button = document.querySelector('#editar_button');
    const file = document.querySelector('.m-file_input');
    const lineas_investigacion = document.querySelector('#pills_lineas');
    const boton_cancelar = document.querySelector('#cancel');
    // const search_boxes = document.querySelectorAll('.m-pill-input_search');

    dropdown_parent.addEventListener('click', toggleDropdown);
    logo.addEventListener('click', goHome);

    // search_boxes.forEach(element => {
    //     let parent = element.parentElement;
        
    //     let search_box = parent.querySelector('.m-pill-input_searchbox');
    //     let search_input = parent.querySelector('.m-pill-input_search');

    //     search_input.addEventListener('focus', () => {
    //         search_box.classList.toggle('h-display-none');
    //     });

    //     search_input.addEventListener('blur', () => {
    //         search_box.classList.toggle('h-display-none');
    //     });
    // });
    
    // Agrega el eventListener que muestra el modal a todos los productos de la 
    // categoria activa

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        let activeTabpane = document.querySelector('.tab-pane.active');
        let products = activeTabpane.querySelectorAll('.m-product-card');
        
        products.forEach(element => {
            element.addEventListener('click', function(){
                showModal(element);
            });
        });
    })

    

    if (editar_button) {
        editar_button.addEventListener('click', goToEditar);
    }

    if (file) {
        let input_file = document.querySelector(`#${file.attributes["for"].value}`);
        input_file.addEventListener('change', () => {
            let filename = input_file.value.replace(/^C:\\fakepath\\/, "");
            file.innerHTML = `<img src="/static/img/foto.svg" alt="" srcset=""> ${filename}`;
        });
    }


    // inputSearch.onkeyup = searchUsers(inputSearch);
    
    // Funcionalidad del input que contiene pills
    if(lineas_investigacion){
        sessionStorage.setItem("pills_lineas", JSON.stringify(["Software", "Software con olor a limón", "Tu corazón"]));

        PillsBox(lineas_investigacion);
    }

    if(boton_cancelar){
        boton_cancelar.addEventListener('click', () => {
            window.history.back();
        });
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

getProducto = (elementoHTML) => {
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

// function showEditPopup(url) {
//     var win = window.open(url, "Edit",
//         'height=500,width=800,resizable=yes,scrollbars=yes');
//     return false;
// }

function showAddPopup(triggeringLink, resultContainer) {
    const id = triggeringLink;
    const name = triggeringLink.id.replace(/^add_/, '');
    const href = triggeringLink.getAttribute('data-url');
    const win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    localStorage.setItem('id_field', resultContainer);
    win.focus();
    return false;
}

function closePopup(win, newID, newRepr, id) {
    let select = document.getElementById(id);
    let option = document.createElement('option');
    option.appendChild(document.createTextNode(newRepr));
    option.value = newID;
    option.setAttribute('selected', 'selected');
    select.appendChild(option);
    win.close();

    localStorage.removeItem('id');
}

// function searchUsers(text) {
//     // console.log(text.value);
//     const csrftoken = getCookie('csrftoken');

//     fetch('http://127.0.0.1:8000/searchUsers', {
//         method: 'POST',
//         credentials: 'same-origin',
//         headers: {
//             'Accept': 'application/json',
//             'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
//             'X-CSRFToken': csrftoken,
//         },
//         body: JSON.stringify({
//             'textoBusqueda': text.value
//         })

//     })
//         .then(res => {
//             return res.json();
//         })
//         .then(res => {
//             const users = res['users'];
//             const selectUsers = document.getElementsByClassName("dropdown-menu inner show")[0];
//             users.forEach(user => {
//                 console.log(user["first_name"]);
//                 console.log(selectUsers);

//                 // let newLi = document.createElement("li");
//                 // let newAnchor = document.createElement("a");
//                 // newAnchor.id = "bs-select-1-"+user["id"];
//                 // newAnchor.className = "dropdown-item";
//                 // newAnchor.role = "option";
//                 // newAnchor.tabIndex = "0";
//                 // // newAnchor.aria-setsize=3;
//                 // // newAnchor.aria-pointset=2;

//                 // let spanText = document.createElement("span");
//                 // spanText.className = "text";
//                 // spanText.appendChild(document.createTextNode(user["first_name"]));


//                 // newAnchor.appendChild(spanText);
//                 // // console.log(newAnchor);
//                 // newLi.appendChild(newAnchor);
//                 // selectUsers.appendChild(newLi);

//                 // console.log(selectUsers);

//                 selectUsers.innerHTML+='<li><a role="option" class="dropdown-item active selected" id="bs-select-1-0" tabindex="0" aria-setsize="4" aria-posinset="1" aria-selected="true"><span class="text">Mustardddddd</span></a></li>';







//             });

//         })
//         .catch(err => {
//             console.log(err);
//         });
// }

async function showModal(elementoHTML){
    // console.log(elementoHTML);
    // const idProducto = elementoHTML.dataset.idproducto;
    // console.log(idProducto);
    const producto = await getProducto(elementoHTML);

    let lineas = [];
    producto['lineas'].forEach(linea => {
        // console.log(linea['nombre']);
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
}

function toggleDropdown() {
    const dropdown = document.querySelector('#dropdown');
    dropdown.classList.toggle('h-display');
}

function goHome() {
    window.location.href = "/home";
}

function goToEditar() {
    window.location.href = "/profile";
}


async function getLineasForm() {
    // showAddPopup('investigacion');

    let form = await fetch('/lineas/create');
    let response = await form.text();

    let modal = document.querySelector('.modal-body');
    modal.innerHTML = response;
}

// Encargado de la funcionalidad del input que contiene pills
function PillsBox(contenedor){
    let selected_pills = JSON.parse(sessionStorage.getItem("pills_lineas"));
    let pill_container = contenedor.querySelector('.m-pill-input_selected-pills');
    let pill_input = contenedor.querySelector('.m-pill-input_search')
    let pills = [];

    let add_pill = (pill_text) => {
        let pill = document.createElement('div');
        pill.classList.add('m-pills');

        let text = document.createElement('span');
        text.classList.add("h-text-overflow");
        text.style.maxWidth = "100px";
        text.textContent = pill_text;
        
        let delete_icon = document.createElement('i');
        delete_icon.classList.add("fas", "fa-times", "mb-0");
        delete_icon.setAttribute("style", "color: white; font-size: 12px;  cursor: pointer;");

        let delete_container = document.createElement('div');
        delete_container.appendChild(delete_icon);
        
        let delete_pill = (pill) => {
            pill_container.removeChild(pill);
            /*
                Decirle al back que elimine la pill
            */
        };

        delete_container.addEventListener('click', () => {
            delete_pill(pill);
        });

        pill.appendChild(text);
        pill.appendChild(delete_container);

        return pill;
    };

    selected_pills.forEach(selected_pill => {
        let pill = add_pill(selected_pill);
        pills.push(pill);
    });

    pills.forEach(pill => {
        pill_container.appendChild(pill);
    })
}
