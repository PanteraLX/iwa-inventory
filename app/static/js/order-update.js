/**
 * Create a HTMLSpanElement with a click event that sets the value of an input field.
 * @param {string} text 
 * @param {HTMLInputElement} inputElement 
 * @param {object} dateOffset 
 * @param {boolean} readFromInput 
 * @returns HTMLSpanElement
 */
const createDateShortcut = (text, inputElement, dateOffset = {}, readFromInput) => {
    const link = document.createElement('span');
    link.innerText = text;
    dateOffset.year = dateOffset.year || 0;
    dateOffset.month = dateOffset.month || 0;
    dateOffset.day = dateOffset.day || 0;
    const date = readFromInput ? new Date(inputElement.value) : new Date();
    link.addEventListener('click', () => {
        const dateWithOffset = new Date(
            date.getFullYear() + dateOffset.year,
            date.getMonth() + dateOffset.month,
            date.getDate() + dateOffset.day,
            date.getHours(),
        );
        inputElement.value = dateWithOffset.toISOString().split('T')[0];
    });
    link.classList.add('iwa-badge');
    return link;
}


/**
 * Add custom buttons to a date input field.
 */
(() => {
    const startedAtButtons = document.getElementById('custom_started_at');
    const startedAtInput = document.getElementById('id_started_at');
    startedAtButtons.hidden = false

    startedAtButtons.appendChild(createDateShortcut('Today', startedAtInput, { year: 0, month: 0, day: 0 }));
})();

(() => {
    const endedAtButtons = document.getElementById('custom_ended_at');
    const endedAtInput = document.getElementById('id_ended_at');
    endedAtButtons.hidden = false

    const todayLinks = createDateShortcut('Today', endedAtInput, { year: 0, month: 0, day: 0 });
    todayLinks.classList.add('mr-2');
    endedAtButtons.appendChild(todayLinks);


    const inOneWeekLinks = createDateShortcut('In One Week', endedAtInput, { year: 0, month: 0, day: 7 });
    inOneWeekLinks.classList.add('mr-2');
    endedAtButtons.appendChild(inOneWeekLinks);


    const inOneMonthLinks = createDateShortcut('In One Month', endedAtInput, { year: 0, month: 1, day: 0 });
    endedAtButtons.appendChild(inOneMonthLinks);
})();



/**
 * Prefill a form with values from query parameters.
 */
(() => {
    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());

    if (params && params.inventory_item) {
        Array
            .from(document.getElementById('id_item').options)
            .map(option => option.selected = (option.value === params.inventory_item));
    }

    if (params && params.user) {
        Array
            .from(document.getElementById('id_user').options)
            .map(option => option.selected = (option.value === params.user));
    }

    if (params && params.now) {
        const today = (new Date()).toISOString().split('T')[0];
        document.getElementById('id_started_at').value = today;
        document.getElementById('id_ended_at').value = today;
    }
})();

