
'use strict';
{
    let filters = JSON.parse(sessionStorage.getItem('django.admin.filtersState'));

    if (!filters) {
        filters = {};
    }

    Object.entries(filters).forEach(([key, value]) => {
        const detailElement = document.querySelector(`[data-filter-title='${CSS.escape(key)}']`);

        if (detailElement) {
            value ? detailElement.setAttribute('open', '') : detailElement.removeAttribute('open');
        }
    });

    const details = document.querySelectorAll('details');
    details.forEach(detail => {
        detail.addEventListener('toggle', event => {
            filters[`${event.target.dataset.filterTitle}`] = detail.open;
            sessionStorage.setItem('django.admin.filtersState', JSON.stringify(filters));
        });
    });
}
