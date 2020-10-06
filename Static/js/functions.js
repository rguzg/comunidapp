function showEditPopup(url) {
    var win = window.open(url, "Edit",
        'height=500,width=800,resizable=yes,scrollbars=yes');
    return false;
}

function showAddPopup(triggeringLink) {
    const name = triggeringLink.id.replace(/^add_/, '');
    const href = triggeringLink.getAttribute('data-url');
    const win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function showAddPopupRevista(triggeringLink) {
    const name = triggeringLink.id.replace(/^add_/, '');
    const href = triggeringLink.getAttribute('data-url');
    const win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}


function closePopupRevista(win, newID, newRepr, id) {
    console.log(win, newID, newRepr, id);
    let select = document.getElementById(id);
    console.log(select);

    let option = document.createElement('option');
    option.appendChild(document.createTextNode(newRepr));
    option.value = newID;
    option.setAttribute('selected', 'selected');
    console.log(option);
    select.appendChild(option);
    console.log(select);
    // $(id).append('<option value=' + newID + ' selected >' + newRepr + '</option>')
    win.close();
}

function closePopup(win, newID, newRepr, id) {
    console.log(win, newID, newRepr, id);
    let select = document.getElementById(id);
    console.log(select);

    let option = document.createElement('option');
    option.appendChild(document.createTextNode(newRepr));
    option.value = newID;
    option.setAttribute('selected', 'selected');
    console.log(option);
    select.appendChild(option);
    console.log(select);
    // $(id).append('<option value=' + newID + ' selected >' + newRepr + '</option>')
    win.close();
}


