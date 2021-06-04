class NotificationController{

    /**  
     * 
     * @param {string} position Las posiciones posibles para options.position son: 'top-left', 'top-right', 'bottom-left' y 'bottom-right'
     */

    constructor(position){
        this.position = position;
        this.notification_container = this.#CreateNotificationContainer();
    }

    /**
     * 
     * @returns {HTMLDivElement} Retorna el contenedor de notificaciones. En caso de que no exista se crea dicho contenedor
     */

    #CreateNotificationContainer(){
        let notification_container = document.querySelector('.toast-container');

        if(!notification_container){
            // La posición de la notificación está definida por ciertas clases que se le agregan al contenedor de la notificación
            let position_classes = [];

            switch (this.position) {
                case 'top-left':
                    position_classes = ['top-0', 'start-0'];
                    break;
                case 'top-right':
                    position_classes = ['top-0', 'end-0'];
                    break;
                case 'bottom-left':
                    position_classes = ['bottom-0', 'start-0'];
                    break;
                case 'bottom-right':
                    position_classes = ['bottom-0', 'end-0'];
                    break;
                default:
                    throw new Error("No se ingresó una posición valida. Las posiciones permitidas son: 'top-left', 'top-right', 'bottom-left' y 'bottom-right'.");
            }

            notification_container = document.createElement('div');

            notification_container.classList.add('toast-container', 'position-fixed', 'p-3', ...position_classes);

            document.body.appendChild(notification_container);
        }

        return notification_container;
    }  
    
    /** 
     * 
     * @param {string} header_text Texto a mostrar en el header de la notificación
     * @param {string} body_text Texto a mostrar en el body de la notifiación
     * @param {object} options JSON con opciones sobre la notificacion. 
     * 
     * Por defecto options.animation y options.autohide son true. 
     * 
     * options.type determina el estilo de la notificación. Existen tres tipos de notificación: success, warning y error
     * 
     * options.number determina el tiempo de delay antes de cerrar la notificación cuando autohide es true
     * 
     * @param {boolean} [options.animation = true]
     * @param {boolean} [options.autohide = true]
     * @param {number} [options.delay = 5000]
     * @param {string} options.type     
     * @returns {object} Retorna un objeto boostrap.Toast
     */

    #CreateNotification(header_text, body_text, options){
        // Creación de los elementos que componene a la notificación
        let notification_container = document.createElement('div');
        let notification_header = document.createElement('div');
        let notification_body = document.createElement('div');
        let bootstrap_notification = new bootstrap.Toast(notification_container, options);

        // Definición del header
        let header_container = document.createElement('div');
        header_container.style.width = '70%'
        header_container.classList.add('d-flex', 'align-items-center', 'justify-content-start');

        let icon = document.createElement('i');
        icon.classList.add('text-white', 'mr-2');

        let header = document.createElement('strong');
        header.classList.add('me-auto', 'text-white');
        header.innerText = header_text;

        header_container.appendChild(icon);
        header_container.appendChild(header);

        let close_button = document.createElement('button');
        close_button.classList.add('btn', 'px-0');

        close_button.addEventListener('click', () => {
            bootstrap_notification.hide();
        });

        let close_icon = document.createElement('i');
        close_icon.classList.add('bi', 'bi-x', 'text-white');

        close_button.appendChild(close_icon);

        // El tipo de notificación definirá el background color del header y el tipo de icono a utilizar
        switch (options.type){
            case 'success':
                icon.classList.add('bi', 'bi-check2');
                notification_header.classList.add('bg-success');
                break;
            case 'warning':
                icon.classList.add('bi','bi-exclamation-triangle-fill');
                notification_header.classList.add('bg-warning');
                break;
            case 'error':
                icon.classList.add('bi','bi-x-circle-fill');
                notification_header.classList.add('bg-danger');
                break;
            default:
                throw new Error("El tipo de notificación no es válido");
        }

        notification_header.classList.add('toast-header', 'd-flex', 'justify-content-between');
        notification_header.style.minWidth = '200px';

        notification_header.appendChild(header_container);
        notification_header.appendChild(close_button);

        // Definición del body
        notification_body.classList.add('toast-body');
        notification_body.innerText = body_text;

        // Definición del container
        notification_container.classList.add('toast');
        notification_container.appendChild(notification_header);
        notification_container.appendChild(notification_body);

        // El evento 'hidden.bs.toast' ocurré cuando se cierra la notificación
        // Como estamos utilizando Bootstrap 4.0, se tiene que usar jQuery para escuchar el evento
        $(notification_container).on('hide.bs.toast', () => {
            notification_container.remove();
        });

        this.notification_container.appendChild(notification_container);

        return bootstrap_notification;
    }

    /** 
     * Muestra una notificación llenada con los argumentos que se le hayan pasado al método. La notificación se elimina automaticamente del DOM cuando se deja de mostrar la notificación
     * 
     * @param {string} header_text Texto a mostrar en el header de la notificación
     * @param {string} body_text Texto a mostrar en el body de la notifiación
     * @param {object} options JSON con opciones sobre la notificacion. 
     * 
     * Por defecto options.animation y options.autohide son true. 
     * 
     * options.type determina el estilo de la notificación. Existen tres tipos de notificación: success, warning y error
     * 
     * options.number determina el tiempo de delay antes de cerrar la notificación cuando autohide es true
     * 
     * @param {boolean} [options.animation = true]
     * @param {boolean} [options.autohide = true]
     * @param {number} [options.delay = 5000]
     * @param {string} options.type
     */

    ShowNotification(header_text, body_text, options){
        // Poner los valores por defecto. Si en options las keys de los valores por defecto existen, los valores por defecto serán remplazados por los que recibió como argumento la función
        options = {animation: true, autohide: true, delay: 5000, ...options};

        // Creación de los elementos que componene a la notificación
        let notification = this.#CreateNotification(header_text, body_text, options);

        notification.show();
    }
}