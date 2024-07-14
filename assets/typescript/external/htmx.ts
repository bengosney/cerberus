import htmx from 'htmx.org/dist/htmx.esm';
import createRemoveExtension from '../htmx/remove';
import createAutoTargetExtension from '../htmx/auto-target';

declare global {
    interface Window {
        htmx: typeof htmx;
    }
}

window.htmx = htmx;

createRemoveExtension();
createAutoTargetExtension();
