() => {
  const SELECTOR = 'a[href], button, input, select, textarea, details, summary, [role="button"], [role="link"], [role="combobox"], [contenteditable="true"]';
  const nodes = document.querySelectorAll(SELECTOR)
  return Array.from(nodes).map((el, i) => {
    const tag = el.tagName.toLowerCase()
    const id = el.id || ''
    let label = ''
    if (el.getAttribute('aria-label')) {
      label = el.getAttribute('aria-label')
    } else if (id && document.querySelector('label[for="' + CSS.escape(id) + '"]')) {
      label = document.querySelector('label[for="' + CSS.escape(id) + '"]').innerText
    } else if (el.closest('label')) {
      label = el.closest('label').innerText
    } else if (el.placeholder) {
      label = el.placeholder
    } else if (el.name) {
      label = el.name
    } else {
      label = el.innerText || ''
    }
    label = label.trim().replace(/\s+/g, ' ').slice(0, 80)
    const type = el.type && el.type !== 'text' ? ':' + el.type : ''
    return {
      index: i,
      tag: tag + type,
      label,
      value: (el.value || '').slice(0, 120),
      visible: !!el.getClientRects().length
    }
  }).filter(r => r.visible)
}
