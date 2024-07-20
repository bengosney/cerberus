export const pad = (n: number, len: number): string =>  n.toString().padStart(len, '0').slice(-len);

export const removeFormPrefix = (element: Element, count: number) => {
    element.querySelectorAll('*').forEach((element) => {
        ['name', 'id'].forEach((attr) => {
          const attr_value = element.getAttribute(attr);
          if (attr_value !== null) {
            const new_attr_value = attr_value.replace('__prefix__', `${count}`);
            if (attr_value !== new_attr_value) {
                element.setAttribute(attr, new_attr_value);
            }
          }
        });
      });
}
