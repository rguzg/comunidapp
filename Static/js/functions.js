function showEditPopup(url) {
    var win = window.open(url, "Edit",
        'height=500,width=800,resizable=yes,scrollbars=yes');
    return false;
}

function showAddPopup(triggeringLink) {
    const id = triggeringLink;
    // console.log(id.id);
    const sibilingId = id.previousElementSibling.id;
    // console.log(sibilingId);
    const name = triggeringLink.id.replace(/^add_/, '');
    const href = triggeringLink.getAttribute('data-url');
    const win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    localStorage.setItem('id_field', sibilingId);
    win.focus();
    return false;
}

function closePopup(win, newID, newRepr, id) {
    // console.log(win, newID, newRepr, id);
    let select = document.getElementById(id);
    let option = document.createElement('option');
    option.appendChild(document.createTextNode(newRepr));
    option.value = newID;
    option.setAttribute('selected', 'selected');
    select.appendChild(option);
    win.close();

    localStorage.removeItem('id');
}