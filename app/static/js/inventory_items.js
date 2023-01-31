// Description: This file contains the javascript for the inventory items page
(() => {
    let params = new URLSearchParams(document.location.search);
    const inventoryFilterSelect = document.getElementById('inventory-filter-select');
    if (params.get('category')) {
        inventoryFilterSelect.value = params.get('category');
    }
    inventoryFilterSelect.addEventListener('change', () => {
        params.set('category', inventoryFilterSelect.value);
        params.set('page', 1);
        window.location = window.location.pathname + '?' + params.toString();
    });

    const inventorySearch = document.getElementById('inventory-search');
    if (params.get('search')) {
        inventorySearch.value = params.get('search');
    }
    inventorySearch.addEventListener('change', () => {
        params.set('search', inventorySearch.value);
        params.set('page', 1);
        window.location = window.location.pathname + '?' + params.toString();
    });
})();
