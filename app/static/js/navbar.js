document.getElementById('user-menu-button').addEventListener('click', () => {
    const userMenu = document.getElementById("user-menu");
    userMenu.classList.toggle('show');
    userMenu.classList.toggle('hide');

})