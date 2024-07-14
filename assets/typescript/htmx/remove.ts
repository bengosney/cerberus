import * as htmx from 'htmx.org';

type HTMX = typeof htmx;

const createRemoveExtension = (htmx: HTMX) => {
    htmx.defineExtension('remove', {
        onEvent: function (name, { detail : { successful = false, elt = null } }) {
            if (name === 'htmx:afterSwap' && successful && elt) {
                const toRemove = elt.getAttribute('hx-remove');
                if (toRemove) {
                    htmx.findAll(toRemove).forEach(htmx.remove);
                }
            }
        }
    });
};

export default createRemoveExtension;
