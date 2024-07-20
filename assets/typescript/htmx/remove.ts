const createRemoveExtension = () => {
    const htmx = window.htmx;
    htmx.defineExtension('remove', {
        onEvent: (name: string, { detail: { successful, requestConfig: { elt = null } = {} } }) => {
            if (name === 'htmx:afterSwap' && successful && elt) {
                const toRemove = (elt as HTMLElement)?.getAttribute('hx-remove');
                if (toRemove) {
                    htmx.findAll(toRemove).forEach(htmx.remove);
                }
            }
        }
    });
};

export default createRemoveExtension;
