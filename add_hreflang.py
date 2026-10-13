import os
pages = [
    'website/documentation.html',
    'website/about.html',
    'website/download-media.html',
    'website/export-to-pdf.html',
    'website/how-to-export-whatsapp-channel-messages.html',
    'website/whatsapp-channel-archive-guide.html',
    'website/support.html',
    'website/terms-of-service.html',
    'website/privacy-policy.html',
]
for p in pages:
    path = p
    if not os.path.exists(path):
        print('SKIP', p)
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.splitlines(keepends=True)
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        if not inserted and '<link rel="canonical"' in line:
            url = line.split('href="')[1].split('"')[0]
            new_lines.append('    <link rel="alternate" hreflang="en" href="' + url + '" />\n')
            new_lines.append('    <link rel="alternate" hreflang="es" href="https://wachannelexporter.me/es/" />\n')
            new_lines.append('    <link rel="alternate" hreflang="pt-BR" href="https://wachannelexporter.me/pt-br/" />\n')
            new_lines.append('    <link rel="alternate" hreflang="x-default" href="https://wachannelexporter.me/" />\n')
            inserted = True
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print('DONE', p)
