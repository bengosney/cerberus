const createAutoTargetExtension = () => {
    const getTarget = (htmlString: string): HTMLElement | null => {
        const parser = new DOMParser();
        const element = parser.parseFromString(htmlString, 'text/xml').firstChild as HTMLElement;
        return element.id ? document.getElementById(element.id) : null;
    };

    window.htmx.defineExtension('auto-target', {
        onEvent: function (name: string, { detail }) {
            const {serverResponse, requestConfig} = detail;
            if (name == 'htmx:beforeSwap' && requestConfig.headers["HX-Target"] == null) {
                const target = getTarget(serverResponse);
                if (target) {
                    detail.target = target;
                    if (requestConfig.elt.hasAttribute('hx-swap') == false) {
                        requestConfig.elt.setAttribute('hx-swap', 'outerHTML');
                    }
                }
            }
        }
    });
};


export default createAutoTargetExtension;
