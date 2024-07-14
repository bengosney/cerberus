import * as htmx from 'htmx.org';

type HTMX = typeof htmx;

const createAutoTargetExtension = (htmx: HTMX) => {
    const getTarget = (htmlString: string): HTMLElement | null => {
        const parser = new DOMParser();
        const element = parser.parseFromString(htmlString, 'text/xml').firstChild as HTMLElement;
        return element.id ? document.getElementById(element.id) : null;
    };

    htmx.defineExtension('auto-target', {
        onEvent: function (name, { detail }) {
            if (name == 'htmx:beforeSwap' && detail.requestConfig.headers["HX-Target"] == null) {
                const target = getTarget(detail.serverResponse);
                if (target) {
                    detail.target = target;
                    detail.requestConfig.swap = detail.requestConfig.swap || "outerHTML";
                }
            }
        }
    });
};


export default createAutoTargetExtension;
