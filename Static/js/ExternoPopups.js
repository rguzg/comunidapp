/**
 * Show the add-externo popup
 * @param {HTMLAnchorElement} triggeringLink DOM Element that triggered the popup
 * @param {String} containerID DOM ID of the element where the new item will be added
 */

function showAddPopup(triggeringLink, containerID) {
  window.open(
    triggeringLink.getAttribute('data-url'),
    'add-externo_popup',
    'height=500,width=800,resizable=yes,scrollbars=yes'
  );

  // The ID of the element where the new item will be added needs to be saved in localStorage because 
  // closePopup will be called from the another window context and the triggeringLink will be lost
  localStorage.setItem('id_field', containerID);
  window.focus();
}

/**
 * This function is called by the add-externo popups to close itself and to add the new item to the main window
 * @param {Window} win Reference to popup window object
 * @param {Object} newItem Data to be added to the new item
 * @param {Number} newItem.key Primary key assigned to the new item in the database. Used when sending the form to the server.
 * @param {String} newItem.name Name of the new item. Used when displaying the new item in the main window.
 * @param {String} newItem.targetID DOM ID of the element where the new item will be added.
 * @param {Object?} newItem.extraData Extra data to be added to the new item. Used when displaying the new item in the main window.
 * @param {String} newItem.extraData.type Type of the extra data. Can be 'estado' or 'ciudad'.
 * @param {String} newItem.extraData.data Extra data to be added to the new item. Used when displaying the new item in the main window.
 */
function closePopup(win, newItem) {
  let select = document.getElementById(newItem.targetID);

  let option = document.createElement('option');
  option.appendChild(document.createTextNode(newItem.name));
  option.value = newItem.key;
  option.setAttribute('selected', 'selected');

  if(newItem.extraData) {
    switch (newItem.extraData.type) {
      case 'estado':
        option.setAttribute('data-pais', newItem.extraData.data);
        break;
      case 'ciudad':
        option.setAttribute('data-estado', newItem.extraData.data);
        break;
      default:
        break;
    }  
  }

  select.appendChild(option);
  win.close();
  localStorage.removeItem('id');

  // Used to select the new item on select elements that use bootstrap-select
  $('#' + newItem.targetID).val(newItem.key);
  $('.selectpicker').selectpicker('refresh');
  $('.selectpicker').selectpicker('refresh');
}
