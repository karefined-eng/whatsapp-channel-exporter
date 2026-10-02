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
    kept.push(`<url>${withoutOptionalMetadata}</url>`);
  }
}
fs.writeFileSync(path, `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${kept.join('')}</urlset>\n`);
console.log(`Sitemap cleaned: ${kept.length} URLs`);
