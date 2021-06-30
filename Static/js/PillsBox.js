/* 
    Encargado de la funcionalidad del input que contiene pills 

    Parametros de la función:
    - Contenedor: Contenedor donde se colocara la PillsBox
    - Recurso: Nombre del recurso de donde se obtendrá la información de autocompletar y las pills seleccionadas

    Los recursos tendrán el siguiente formato:
    [ 
        {
            id: 0,
            nombre: "pill"
        },

        {
            id: 0,
            nombre: "pill"
        }
        ...
    ]

*/


class PillsBox{
    /**
     * El objeto PillsBox es el encargado de manejar el comportamiento de los PillsBox
     * @param {HTMLDivElement} container - Contenedor donde se encuentra el PillsBox
     * @param {string} resource - Recurso que utilizará el PillsBox para obtener default pills y para obtener el contenido del autocompletar
     * @param {boolean} [useDefaultPills] - Indica si se cargaran algunas pills por defecto cuando se genere el PillsBox.
     */

    #pills;

    constructor(container, resource, useDefaultPills = true){
        this.container = container;
        this.#resource = resource;
        this.#useDefaultPills = useDefaultPills;
        this.#pills_initialized = false;

        // El número máximo de espacios en blanco separados por coma que aceptara el PillsBox antes de lanzar un error
        this.#maxBlankSpaces = 1;

        // Este es el estado del PillsBox, las pills que se muestran se sacan de aquí. Cuando se escribe algo en el input, se actualiza el 
        // estado; lo mismo también ocurre cuando se da click en algún objeto del autocompletar.
        this.#pills = {default: [], user_added: []};

        // El estado de pill_input que almacena las palabras añadidas por el usuario. Durante la actualización del DOM, el contenido de este 
        // arreglo se hace consistente con this.pills
        this.#input = [];

        // Arreglo que almacena los errores que pueda tener el PillsBox. Durante la actualización del DOM, los contenidos de este arreglo
        // se muestran debajo de PillsBox
        this.#errors = [];

        if(this.useDefaultPills){
            this.#AddDefaultPills();
        } else {
            this.#pills_initialized = true;
        }

        this.#AddInputEventListeners();
    }

    /**
     * Añadel al estado de la PillBox una pill
     * 
     * @param {Pill} pill 
     * @param {string} type 
     * @param {Number} id
     */
    #AddPill(name, type, id = 0){
        let new_pill = new Pill(name.trim(), id);

        switch(type){
            case "default":
                this.#pills.default.push(new_pill);
                break;
            case "user_added":
                this.#pills.user_added.push(new_pill);
                break;
            default:
                throw new Error("El tipo de pill es incorrecto");
        }

        let current_user_pill_count = this.#input.length - 1;

        new_pill.DOMRepresentation.addEventListener('deleted_pill', () => {
            this.#DeletePill(new_pill, type);

            if(type == 'user_added'){
                this.#input.splice(current_user_pill_count, 1);
            }

            this.#UpdateDOM();
        });
    }

    /**
     * Quita del estado de la PillBox una pill y actualiza el DOM
     * 
     * @param {Pill} pill_to_delete
     * @param {string} type
     */
    #DeletePill(pill_to_delete, type){
        switch(type){
            case "default":
                this.#pills.default = this.#pills.default.filter((pill) => pill != pill_to_delete);
                break;
            case "user_added":
                this.#pills.user_added = this.#pills.user_added.filter((pill) => pill != pill_to_delete);
                break;
            default:
                throw new Error("El tipo de pill es incorrecto");
        }
    }

    /**
     * Reemplaza old_pill por new_pill en el estado
     * @param {Pill} old_pill 
     * @param {Pill} new_pill 
     */
    #ReplaceUserAddedPill(old_pill, new_pill){
        let old_pill_index = this.#pills.user_added.findIndex((pill) => pill == old_pill);

        this.#pills.user_added[old_pill_index] = new_pill;
        new_pill.DOMRepresentation.addEventListener('deleted_pill', () => {
            this.#DeletePill(new_pill, 'user_added');
            this.#UpdateDOM();
        });
    }

    /**
     * Vuelve a hacer consistente el estado con el DOM. 
     * Quita todas las pills y agregar las DOMRepresentations de this.pills.default y después this.pills.user_added. 
     * Actualiza pill_input según el valor de this.input
     * Quita todos los errores presentes e inserta los errores que se encuentren en this.errors
     */
    #UpdateDOM(){
        let selected_pill_container = this.container.querySelector('.m-pill-input_selected-pills');
        let pill_input = this.container.querySelector('.m-pill-input_search');
        let error_container = this.container.querySelector('#errors');

        // childNodes se actualiza cuando cambia algo en el DOM, por eso se almacena aparte el valor
        let selected_pill_children_count = selected_pill_container.childElementCount;

        for (let i = 0; i < selected_pill_children_count; i++) {
            const pill =  selected_pill_container.children[selected_pill_container.childElementCount - 1];
            
            pill.remove();
        }

        // childNodes se actualiza cuando cambia algo en el DOM, por eso se almacena aparte el valor
        let error_children_count = error_container.childElementCount;

        for (let i = 0; i < error_children_count; i++) {
            const error =  error_container.children[error_container.childElementCount - 1];
            
            error.remove();
        }

        this.#pills.default.forEach((pill) => {
            selected_pill_container.appendChild(pill.DOMRepresentation);
        });

        this.#pills.user_added.forEach((pill) => {
            selected_pill_container.appendChild(pill.DOMRepresentation);
        });

        for (let i = 0; i < this.#errors.length; i++) {
            // Al final del for loop, this.errors quedará vacio. 
            // Es la responsabilidad de las funciones que modifican el estado de siempre verificar errores
            const error_string = this.#errors.pop();
            
            let error = document.createElement('small');
            error.innerText = error_string;
            error.classList.add('text-danger');
    
            error_container.appendChild(error);
        }

        let new_pill_input_value = "";
                
        this.#input.map((pill_name, i) => {
            new_pill_input_value += pill_name;

            if(i != this.#input.length - 1){
                new_pill_input_value += ",";
            }
        });

        pill_input.value = new_pill_input_value;

        this.#DispatchChangeEvent();
    }

    /**
     * Añade los event listeners de pill_input que ocupa el pill_box. Los primeros tres event listeners se encargan de mostrar y quitar 
     * el autocompletar cuando pill_input obtiene/pierde el focus. El cuarto event listener compara lo que está en el 
     * pill_input con el estado, haciendo consistente lo que está en el pill_input con el estado y 
     * muestra el autocompletar para el ultimo elemento de pill_input.
     */
    #AddInputEventListeners(){
        let pill_input = this.container.querySelector('.m-pill-input_search');

        pill_input.addEventListener('focusin', () => {
            let last_input = this.#input[this.#input.length - 1];

            if(last_input){
                this.#GenerateAutocomplete(last_input.trim());
            }
        });

        pill_input.addEventListener('keydown', (event) => {
            if(event.key === "Tab"){
                this.container.querySelector("#searchbox").classList.add("h-display-none");
            }
        });

        document.body.addEventListener('click', (event) => {
            if(event.target != pill_input){
                this.container.querySelector("#searchbox").classList.add("h-display-none");
            }
        });

        pill_input.addEventListener('input', () => {
            let blank_pills = 0;

            this.#input = pill_input.value.split(',');

            this.#GenerateAutocomplete(this.#input[this.#input.length - 1].trim());

            this.#input.forEach((pill_name, i) => {
                if(pill_name.trim() != ""){
                    let pill = this.#pills.user_added[i];

                    if(pill && pill.name != pill_name){
                        this.#ReplaceUserAddedPill(pill, new Pill(pill_name.trim()));
                    }

                    if(!pill){
                        this.#AddPill(pill_name, 'user_added');
                    }
                } else {
                    blank_pills++;
                }
            });

            if(blank_pills > this.#maxBlankSpaces){
                this.#errors.push("Elimina los espacios en blanco");
            }

            // Quitar las pills que no están representadas en el pill_input, comparando lo que está en pills.user_added con el input
            let pills_to_remove = []
            
            this.#pills.user_added.forEach((pill, i) => {
                if(!this.#input[i] || !(pill.name == this.#input[i].trim())){
                    pills_to_remove.push(pill);
                }
            });

            pills_to_remove.forEach((pill) => {
                this.#DeletePill(pill, 'user_added');
            });

            this.#UpdateDOM();
        });
    }

    /**
     * Realiza el envío de un evento 'change'
     */
    #DispatchChangeEvent(){
        this.container.dispatchEvent(new Event('change'));
    }

    /**
     * Realiza una petición a /buscar/this.recurso?q=name y agrega a un contenedor los que retorne la petición. Al hacer click en uno
     * de los resultados, se reemplazará el ultimo pill con el resultado
     * @param {string} name 
     */
    async #GenerateAutocomplete(name){ 
        let autocomplete_container = this.container.querySelector('#searchbox');

        // Si name está vacio, desaparecer el autocomplete_container (en caso de que se encuentre) y retornar
        if(!name){
            autocomplete_container.classList.add('h-display-none');
            return;
        }

        autocomplete_container.classList.remove('h-display-none');

        autocomplete_container.innerHTML = "";

        let request = await fetch(`/buscar/${this.#resource}?q=${name}`);
        let resources = await request.json();

        resources['mensaje'].forEach((resource) => {
            let result = new AutocompleteResult(resource.nombre);

            result.DOMRepresentation.addEventListener('click', () => {
                let last_pill = this.#pills.user_added[this.#pills.user_added.length - 1];
                let pill_input = this.container.querySelector('.m-pill-input_search');

                this.#input[this.#input.length - 1] = resource.nombre;

                this.#ReplaceUserAddedPill(last_pill, new Pill(resource.nombre));

                autocomplete_container.classList.add('h-display-none');
                pill_input.focus();

                this.#UpdateDOM();
            });

            autocomplete_container.appendChild(result.DOMRepresentation);
        });
    }

    /**
     * Añade a la PillsBox las pills proporcionados por defecto por resource. Resource debe retornar un arreglo con las default pills en
     * el siguiente formato: {id, nombre}
     */
     async #AddDefaultPills(){
        let request = await fetch(`/api/${this.#resource}`);
        let default_pills = await request.json();

        default_pills.forEach((pill) => {
            this.#AddPill(pill['nombre'], 'default', pill['id']);
        });

        this.#UpdateDOM();
        this.container.dispatchEvent(new Event('pills_loaded'));
        this.#pills_initialized = true;
    }

    /**
     * El PillsBox solo es valido si no tiene ningun error
     * @returns {Boolean}
     */
    IsValid(){
        return this.container.querySelector('#errors').childElementCount == 0;
    }

    /**
     * @returns {Promise}
     */
    get pills(){
        // Las pills por defecto son llenadas por un método asíncrono, así que es necesario que el getter de pills retorne una promesa
        return new Promise((resolve, reject) => {
            if(this.#pills_initialized){
                resolve(this.#pills);
            } else {
                this.container.addEventListener('pills_loaded', () => {
                    resolve(this.#pills);
                });
            }
        });
    }
}

class Pill{
    /**
     * Crea un objeto pill. Los objetos pill almacenan un nombre y un id
     * 
     * @param {string} name 
     * @param {number} [id]
     */
    constructor(name, id = 0){
        this.name = name;
        this.id = id;
        this.DOMRepresentation = this.#CreateDOMRepresentation();
    }

    #CreateDOMRepresentation(){
        // Definición del contenedor del pill
        let pill = document.createElement('div');
        pill.classList.add('m-pills');
        pill.setAttribute('data-id', this.id);

        // Definición del texto de la pill
        let text = document.createElement('span');
        text.classList.add("h-text-overflow");
        text.style.maxWidth = "100px";
        text.textContent = this.name;
        
        // Definición del botón eliminar
        let delete_icon = document.createElement('i');
        delete_icon.classList.add("fas", "fa-times", "mb-0");
        delete_icon.setAttribute("style", "color: white; font-size: 12px;  cursor: pointer;");

        let delete_container = document.createElement('div');
        delete_container.appendChild(delete_icon);

        delete_container.addEventListener('click', () => {
            this.DeletePill();
        });

        pill.appendChild(text);
        pill.appendChild(delete_container);

        return pill;
    }

    DeletePill(){
        this.DOMRepresentation.dispatchEvent(new Event('deleted_pill'));
    }
}

class AutocompleteResult{
    /**
     * Objeto AutocompleteResult que emite eventos cuando se da click
     * @param {string} name 
     */
    constructor(name){
        this.name = name;
        this.DOMRepresentation = this.#CreateDOMRepresentation();
    }

    #CreateDOMRepresentation(){
        let span = document.createElement('span');
        span.classList.add('p-2', 'col-12', 'm-search-result', 'd-flex')
        span.innerText = this.name;

        span.addEventListener('click', () => {
            span.dispatchEvent(new Event('autocomplete_click'));
        });

        return span;
    }
}

async function PcillsBox(contenedor, recurso, useDefaultPills = true){
    let request = await fetch(`/api/${recurso}`);
    let selected_pills = useDefaultPills ? await request.json() : {};
    let pill_container = contenedor.querySelector('.m-pill-input_selected-pills');
    let pill_input = contenedor.querySelector('.m-pill-input_search');

    
    let new_pill = (pill_object) => {
        // Por el momento, evento no se emite cuando se elimina una pill agregada por el usuario
        let pill_deleted_event = new CustomEvent('pill_deleted', {detail: pill_object});

        let pill = document.createElement('div');
        pill.classList.add('m-pills');
        pill.setAttribute('data-id', pill_object.id);

        let text = document.createElement('span');
        text.classList.add("h-text-overflow");
        text.style.maxWidth = "100px";
        text.textContent = pill_object.nombre;
        
        let delete_icon = document.createElement('i');
        delete_icon.classList.add("fas", "fa-times", "mb-0");
        delete_icon.setAttribute("style", "color: white; font-size: 12px;  cursor: pointer;");

        let delete_container = document.createElement('div');
        delete_container.appendChild(delete_icon);
        
        let delete_pill = (pill) => {
            pill.parentNode.removeChild(pill);
            let new_pills_input = "";
            
            let pill_array = pill_input.value.split(',')
            
            pill_array.forEach((element, index) => {
                let trimmed_element = element.trimEnd().trimStart();

                if(pill.innerText != trimmed_element){
                    if(index != pill_array.length - 1){
                        new_pills_input += `${element},`
                    } else {
                        new_pills_input += `${element}`
                    }
                }
            });

            pill_input.value = new_pills_input;
        };

        delete_container.addEventListener('click', () => {
            delete_pill(pill);
            contenedor.dispatchEvent(pill_deleted_event);
        });

        pill.appendChild(text);
        pill.appendChild(delete_container);

        return pill;
    };

    let generate_pills = (selected_pills, container) => {
        let pills = [];

        selected_pills.forEach(selected_pill => {
            let pill = new_pill(selected_pill);
            pills.push(pill);
        });
    
        pills.forEach(pill => {
            container.appendChild(pill);
        });
    }

    let generate_new_pills = (text_array) => {
        /* El contenedor de new_pills se genera de nuevo cada vez que se escribe en el input de  
        agregar pills */
        let new_pills = [];
    
        if(contenedor.querySelector('#new_pills')){
            contenedor.querySelector('#new_pills').remove();
        }

        let new_pills_container = document.createElement('div');
        new_pills_container.setAttribute('id', 'new_pills');
        new_pills_container.classList.add('col-12', 'p-0', 'd-flex', 'flex-row', 'flex-wrap');
        
        text_array.forEach((element) => {
            if(element != "" && element != " "){
                let trimmed_element = element.trimEnd().trimStart();
                new_pills.push({
                    id: 0,
                    nombre: trimmed_element
                });
            }
        });

        generate_pills(new_pills, new_pills_container);

        pill_container.appendChild(new_pills_container);
    }
    
    let generate_autocomplete = async (query_text) => {
        /*
        generate_result recibe result_object que contiene el id del objeto de la base de datos que se está
        sugiriendo y el texto que va a ir en span.m-search-result. result_object tiene el siguiente formato:
        
        {
            id: 0,
            nombre: "pill"
        },
        */   
        let generate_result = (result_object) => {
            let span = document.createElement('span');
            span.classList.add('p-2', 'col-12', 'm-search-result')
            span.innerText = result_object.nombre;

            span.addEventListener('click', () => {
                let split_input = pill_input.value.split(',');

                // Regenerar el value de pill_input a partir de lo que hay en el arreglo split_input
                split_input[split_input.length - 1] = result_object.nombre;
                pill_input.value = ""

                split_input.forEach((element) => {
                    pill_input.value += `${element}, `
                })

                contenedor.querySelector("#searchbox").classList.add("h-display-none");
                pill_input.focus();
        
                generate_new_pills(split_input);
            })

            return span;
        }        

        /* El contenedor de autocomplete se genera de nuevo cada vez que se escribe en el input de  
        agregar pills */
        if(contenedor.querySelector('#searchbox_results')){
            contenedor.querySelector('#searchbox_results').remove();
        }

        // Asegurarse de que no el ultimo elemento en el input no sea un espacio
        if(query_text != "" && query_text != " "){
            contenedor.querySelector("#searchbox").classList.remove("h-display-none");

            let contenedor_resultado = document.createElement('div');
            contenedor_resultado.classList.add('d-flex', 'flex-column');
            contenedor_resultado.id = "searchbox_results";

            let request = await fetch(`/buscar/${recurso}?q=${query_text}`);
            let resources = await request.json();

            resources['mensaje'].forEach((element) => {
                contenedor_resultado.appendChild(generate_result(element));
            });

            contenedor.querySelector("#searchbox").appendChild(contenedor_resultado);
        } else {
            contenedor.querySelector("#searchbox").classList.add("h-display-none");
        }
    }

    let show_error = (error_text) => {
        let error = document.createElement('span');
        error.classList.add('text-danger');
        error.id = "error";
        error.innerText = error_text;
        
        contenedor.appendChild(error);
    }

    let delete_error = () => {
        let error = contenedor.querySelector('#error');
        
        if(error){
            error.remove();
        }
    }

    pill_input.addEventListener('input', () => {
        delete_error();

        let split_input = [];
        // Si no hay nada escrito en m-pill-input_searchbox, el contenedor de autocompletar no se muestra
        // y no se realiza el split de pill_input
        if(pill_input.value.trim() == ""){
            contenedor.querySelector("#searchbox").classList.add("h-display-none");
        } else {
            contenedor.querySelector("#searchbox").classList.remove("h-display-none");
            split_input = pill_input.value.split(',');

            for (let i = 0; i < split_input.length; i++) {
                if(split_input[i].trim() == ""){
                    show_error("Elimina los espacios en blanco antes de continuar");
                    break;
                }
            }

            // Solo se va a hacer el query para mostrar en el autocompletar en el ultimo elemento
            let query = split_input[split_input.length - 1].trim();
            generate_autocomplete(query);
        }
        
        generate_new_pills(split_input);
    });

    document.body.addEventListener('click', () => {
        contenedor.querySelector("#searchbox").classList.add("h-display-none");
    })

    if(useDefaultPills){
        generate_pills(selected_pills, pill_container);
    }

}

function CreateFormData(form){
    let data = new FormData();
    
    // Agregar al FormData el valor de todos los inputs excepto los que sean botones o inputs de PillsBox
    for (let i = 0; i < form.elements.length; i++) {
        let element = form.elements[i];

        if(element.type != "submit" && element.type != "button" && element.name != "input_pill"){
            switch (element.type) {
                case "file":
                    data.append(element.name, element.files[0]);
                    break;
                case "checkbox":
                    data.append(element.name, element.checked);
                    break;
                default:
                    data.append(element.name, element.value);
                    break;
            }
        }
    }

   return data;
};

