import fs from 'node:fs';

const path = process.argv[2] ?? 'dist/sitemap.xml';
const allowed = new Set([
  'https://wachannelexporter.me/',
  'https://wachannelexporter.me/about',
  'https://wachannelexporter.me/documentation',
  'https://wachannelexporter.me/download-media',
  'https://wachannelexporter.me/export-to-pdf',
  'https://wachannelexporter.me/privacy-policy',
  'https://wachannelexporter.me/support',
  'https://wachannelexporter.me/faq',
  'https://wachannelexporter.me/how-to-export-whatsapp-channel-messages',
  'https://wachannelexporter.me/whatsapp-channel-archive-guide',
  'https://wachannelexporter.me/terms-of-service',
  'https://wachannelexporter.me/es/',
  'https://wachannelexporter.me/es/privacy-policy',
  'https://wachannelexporter.me/es/support',
  'https://wachannelexporter.me/pt-br/',
  'https://wachannelexporter.me/pt-br/privacy-policy',
  'https://wachannelexporter.me/pt-br/support',
]);
const canonicalAliases = new Map([
  ['https://wachannelexporter.me/es', 'https://wachannelexporter.me/es/'],
  ['https://wachannelexporter.me/pt-br', 'https://wachannelexporter.me/pt-br/'],
]);
const xml = fs.readFileSync(path, 'utf8');
// Truthful per-URL last modify dates. 2026-10-13 = SEO/GEO remediation
// (schema, authorship, freshness, hreflang, evidence) shipped this date.
const lastmodByUrl = new Map([
  ['https://wachannelexporter.me/', '2026-10-13'],
  ['https://wachannelexporter.me/about', '2026-10-13'],
  ['https://wachannelexporter.me/documentation', '2026-10-13'],
  ['https://wachannelexporter.me/download-media', '2026-10-13'],
  ['https://wachannelexporter.me/export-to-pdf', '2026-10-13'],
  ['https://wachannelexporter.me/privacy-policy', '2026-10-13'],
  ['https://wachannelexporter.me/support', '2026-10-13'],
  ['https://wachannelexporter.me/faq', '2026-10-13'],
  ['https://wachannelexporter.me/how-to-export-whatsapp-channel-messages', '2026-10-13'],
  ['https://wachannelexporter.me/whatsapp-channel-archive-guide', '2026-10-13'],
  ['https://wachannelexporter.me/terms-of-service', '2026-10-13'],
  ['https://wachannelexporter.me/es/', '2026-09-20'],
  ['https://wachannelexporter.me/es/privacy-policy', '2026-10-13'],
  ['https://wachannelexporter.me/es/support', '2026-10-13'],
  ['https://wachannelexporter.me/pt-br/', '2026-09-20'],
  ['https://wachannelexporter.me/pt-br/privacy-policy', '2026-09-20'],
  ['https://wachannelexporter.me/pt-br/support', '2026-10-13'],
]);
const defaultLastmod = '2026-09-20';
const urls = [...xml.matchAll(/<url>([\s\S]*?)<\/url>/g)].map((m) => m[1]);
const seen = new Set();
const kept = [];
for (const block of urls) {
  const generatedLoc = block.match(/<loc>([^<]+)<\/loc>/)?.[1];
  const loc = generatedLoc && (canonicalAliases.get(generatedLoc) ?? generatedLoc);
  if (loc && allowed.has(loc) && !seen.has(loc)) {
    seen.add(loc);
    // Omit build-time lastmod and the ignored changefreq/priority hints.
    const canonicalBlock = block.replace(/<loc>[\s\S]*?<\/loc>/i, `<loc>${loc}</loc>`);
    const withoutOptionalMetadata = canonicalBlock.replace(/<(lastmod|changefreq|priority)>[\s\S]*?<\/\1>/gi, '');
    const lastmod = lastmodByUrl.get(loc) ?? defaultLastmod;
    kept.push(`<url>${withoutOptionalMetadata}<lastmod>${lastmod}</lastmod></url>`);
  }
}
fs.writeFileSync(path, `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${kept.join('')}</urlset>\n`);
console.log(`Sitemap cleaned: ${kept.length} URLs`);
