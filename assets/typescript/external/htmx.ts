import * as htmx from 'htmx.org';
import createRemoveExtension from '../htmx/remove';
import createAutoTargetExtension from '../htmx/auto-target';

declare global {
    interface Window {
        htmx: typeof htmx;
    }
}

window.htmx = htmx;

createRemoveExtension(htmx);
createAutoTargetExtension(htmx);
