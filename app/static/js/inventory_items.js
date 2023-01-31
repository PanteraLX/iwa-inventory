// Description: This file contains the javascript for the inventory items page
(() => {
    let params = new URLSearchParams(document.location.search);

    // Filter by category
    const inventoryFilterSelect = document.getElementById('inventory-filter-select');

    const category = params.get('category')
    if (category && category !== 'None') {
        inventoryFilterSelect.value = category;
    }
    inventoryFilterSelect.addEventListener('change', () => {
        params.set('category', inventoryFilterSelect.value);
        params.set('page', 1);
        window.location = window.location.pathname + '?' + params.toString();
    });

    // Search
    const inventorySearch = document.getElementById('inventory-search');

    const search = params.get('search')
    if (search && search !== 'None') {
        inventorySearch.value = search;
    }
    inventorySearch.addEventListener('change', () => {
        params.set('search', inventorySearch.value);
        params.set('page', 1);
        window.location = window.location.pathname + '?' + params.toString();
    });

    // Pagination
    const paginationSelect = document.getElementById('pagination-select');

    const page = params.get('paginate_by')
    if (page && page !== 'None') {
        paginationSelect.value = page;
    }

    paginationSelect.addEventListener('change', () => {
        params.set('page', 1);
        params.set('paginate_by', paginationSelect.value);
        window.location = window.location.pathname + '?' + params.toString();
    });

})();
