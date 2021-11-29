function showAddPopup(triggeringLink, resultContainer) {
  const id = triggeringLink;
  const name = triggeringLink.id.replace(/^add_/, '');
  const href = triggeringLink.getAttribute('data-url');
  const win = window.open(
    href,
    name,
    'height=500,width=800,resizable=yes,scrollbars=yes'
  );
  localStorage.setItem('id_field', resultContainer);
  win.focus();
  return false;
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

  select.appendChild(option);
  win.close();

  localStorage.removeItem('id');

  $('#' + newItem.targetID).val(newItem.key);
  $('.selectpicker').selectpicker('refresh');
  $('.selectpicker').selectpicker('refresh');
}
