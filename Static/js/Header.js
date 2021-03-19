// Funcionalidad del header dropdown

const dropdown_parent = document.querySelector('#dropdown_parent');

dropdown_parent.addEventListener('click', () => {
    const dropdown = document.querySelector('#dropdown');
    dropdown.classList.toggle('h-display');
});
