function showEditPopup(url) {
    var win = window.open(url, "Edit",
        'height=500,width=800,resizable=yes,scrollbars=yes');
    return false;
}

function showAddPopup(triggeringLink) {
    let name = triggeringLink.id.replace(/^add_/, '');
    let href = triggeringLink.getAttribute('data-url');
    let win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function closePopup(win, newID, newRepr, id) {
    $(id).append('<option value=' + newID + ' selected >' + newRepr + '</option>')
    win.close();
}


