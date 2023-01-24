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




/**
 * Format a DateTime object to a string.
 * 
 * @param {*} date 
 * @returns string
 */
const getTimestamp = (date) => {
    const pad = (n, s = 2) => (`${new Array(s).fill(0)}${n}`).slice(-s);
    return `${pad(date.getDate(),)}.${pad(date.getMonth() + 1)}.${pad(date.getFullYear(), 4)}`;
}

const writeErrorMessages = (errors) => {
    const errorContainer = document.getElementById('error-container');
    errorContainer.innerHTML = '';
    const errorTitle = document.createElement('div');
    errorTitle.innerText = `There is an overlap with existing orders:`;
    errorTitle.classList.add('block', 'mb-2', 'text-sm', 'font-medium', 'text-gray-900');
    errorContainer.appendChild(errorTitle);

    errors.forEach((error, index) => {
        const errorElement = document.createElement('div');
        errorElement.innerText = `(${index + 1}.) Timespan: ${getTimestamp(error.startedAt)} - ${getTimestamp(error.endedAt)}, Quantity: ${error.quantity}`;
        errorElement.classList.add('block', 'mb-2', 'text-sm', 'font-medium', 'text-gray-900', 'ml-4');
        errorContainer.appendChild(errorElement);
    });
}

/**
 * Check if the order overlaps with other orders.
 */
(async () => {
    const quantityInput = document.getElementById('id_quantity');
    const startedAtInput = document.getElementById('id_started_at');
    const endedAtInput = document.getElementById('id_ended_at');
    const itemId = Number.parseInt(document.getElementById('id_item').value, 10)
    const orderId = Number.parseInt(document.getElementById('order-id').innerText, 10)
    const orderSubmit = document.getElementById('order-submit');

    if (!itemId) {
        return;
    }

    /**
    * 
    * @returns {Promise<void>}
    */
    const changeCallback = async () => {
        const quantity = Number.parseInt(quantityInput.value, 10);
        const startedAt = new Date(startedAtInput.value);
        const endedAt = new Date(endedAtInput.value);

        const host = 'http://127.0.0.1:8000';
        const url = new URL(`${host}/api/orders-by-item/${itemId}`);

        const response = await fetch(url.href, {
            mode: 'cors',
            credentials: 'omit'
        })

        const data = await response.json();

        if (!data) {
            return;
        }

        const orders = data.map(dataSet => {
            const order = {}
            order.startedAt = new Date(dataSet.fields.started_at);
            order.endedAt = new Date(dataSet.fields.ended_at);
            order.quantity = dataSet.fields.quantity;
            order.pk = dataSet.pk;
            return order;
        });

        const ordersInTimeframe = orders
            .filter(order => {
                const selfDeclaredStartInTimeFrame = startedAt >= order.startedAt && startedAt <= order.endedAt;
                const selfDeclaredEndInTimeFrame = endedAt >= order.startedAt && endedAt <= order.endedAt;
                const orderCompleteInTimeframe = selfDeclaredStartInTimeFrame && selfDeclaredEndInTimeFrame || (selfDeclaredStartInTimeFrame && !selfDeclaredEndInTimeFrame) || (!selfDeclaredStartInTimeFrame && selfDeclaredEndInTimeFrame);
                const existingOrderStartInTimeframe = order.startedAt >= startedAt && order.startedAt <= endedAt;
                const existingOrderEndInTimeframe = order.endedAt >= startedAt && order.endedAt <= endedAt;
                const ExistingOrderInTimeframe = existingOrderStartInTimeframe && existingOrderEndInTimeframe || (existingOrderStartInTimeframe && !existingOrderEndInTimeframe) || (!existingOrderStartInTimeframe && existingOrderEndInTimeframe);
                return orderCompleteInTimeframe || ExistingOrderInTimeframe;
            })
            .filter(order => order.quantity <= quantity)
            .filter(order => order.pk !== orderId);

        const errorContainer = document.getElementById('error-container');
        errorContainer.innerHTML = '';
        ordersInTimeframe.length > 0 ? orderSubmit.disabled = true : orderSubmit.disabled = false;
        if (ordersInTimeframe.length > 0) {
            writeErrorMessages(ordersInTimeframe);
        }
    }
    quantityInput.addEventListener('change', changeCallback)
    startedAtInput.addEventListener('change', changeCallback);
    endedAtInput.addEventListener('change', changeCallback);
    changeCallback()
})();
