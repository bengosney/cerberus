import * as htmx from 'htmx.org';

type HTMX = typeof htmx;

const createAutoTargetExtension = (htmx: HTMX) => {
    const getTarget = (htmlString: string): HTMLElement | null => {
        const parser = new DOMParser();
        const element = parser.parseFromString(htmlString, 'text/xml').firstChild as HTMLElement;
        return element.id ? document.getElementById(element.id) : null;
    };

    htmx.defineExtension('auto-target', {
        onEvent: function (name, event) {
            if (name == 'htmx:beforeSwap' && event.detail.requestConfig.headers["HX-Target"] == null) {
                const target = getTarget(event.detail.serverResponse);
                if (target) {
                    event.detail.target = target;
                }
            }
        }
    });
};


export default createAutoTargetExtension;
