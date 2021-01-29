// Encargado de la funcionalidad del input que contiene pills
function PillsBox(contenedor){
    let selected_pills = ["Software", "Software con olor a limón", "Tu corazón"];

    let pill_container = contenedor.querySelector('.m-pill-input_selected-pills');
    let pill_input = contenedor.querySelector('.m-pill-input_search');

    let new_pill = (pill_text) => {
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
        });

        pill.appendChild(text);
        pill.appendChild(delete_container);

        return pill;
    };

    let generate_pills = (text_array, container) => {
        let pills = [];

        text_array.forEach(selected_pill => {
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

                // ¿Qué pasa si se repite un elemento?
                if(!new_pills.includes(trimmed_element)){
                    new_pills.push(trimmed_element);
                }
            }
        });

        generate_pills(new_pills, new_pills_container);

        pill_container.appendChild(new_pills_container);
    }
    
    let generate_autocomplete = (query_text) => {
        let generate_result = (text) => {
            let span = document.createElement('span');
            span.classList.add('p-2', 'col-12', 'm-search-result')
            span.innerText = text;

            span.addEventListener('click', () => {
                let split_input = pill_input.value.split(',');

                pill_input.value = pill_input.value.replace(split_input[split_input.length - 1], `${text}, `);
                split_input[split_input.length - 1] = text;

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
            contenedor_resultado.appendChild(generate_result(query_text));
    
            contenedor.querySelector("#searchbox").appendChild(contenedor_resultado);
        } else {
            contenedor.querySelector("#searchbox").classList.add("h-display-none");
        }
    }


    pill_input.addEventListener('keyup', () => {
        // Si no hay nada escrito en m-pill-input_searchbox, el contenedor de autocompletar desaparece
        if(pill_input.value == ""){
            contenedor.querySelector("#searchbox").classList.add("h-display-none");
        } else {
            contenedor.querySelector("#searchbox").classList.remove("h-display-none");
        }

        let split_input = pill_input.value.split(',');
        
        generate_autocomplete(split_input[split_input.length - 1]);
        generate_new_pills(split_input);
    });

    generate_pills(selected_pills, pill_container);

}