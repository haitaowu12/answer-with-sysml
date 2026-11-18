// Local presentation policy. Applied before delivery hashes are calculated,
// including live previews, comparisons and the viewer's exported share cards.
// Source attribution and licence notices remain in the package, not the UI.
const DETAILS = {
  'viewer.passport.eyebrow': 'Details',
  'viewer.passport.metadata': 'Details',
  'viewer.passport.close': 'Close details',
  'viewer.passport.move': 'Move details. Drag, use arrow keys, or press Home to reset.',
  'viewer.passport.reach': 'Follow connections',
};

export function readerMessage(locale, key, message) {
  const language = (locale || 'en').split('-')[0].toLowerCase();
  if (key.startsWith('diagram.description.') && /archify/i.test(message)) {
    return ({zh: '可交互图解。', ko: '인터랙티브 다이어그램.', es: 'Diagrama interactivo.'})[language]
      || 'Interactive diagram.';
  }
  if (key === 'viewer.guide.credit') return 'Diagram help';
  if (key === 'viewer.preset.badge.editorialPlate') return '04';
  if (key === 'viewer.export.card.routeBadge' || key === 'viewer.export.card.reachBadge') {
    return message.replace(/^ARCHIFY\s*·\s*/i, '');
  }
  return language === 'en' && DETAILS[key] ? DETAILS[key] : message;
}
