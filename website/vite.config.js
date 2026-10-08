import { defineConfig } from 'vite';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import Sitemap from 'vite-plugin-sitemap';

const __dirname = dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [
    Sitemap({
      hostname: 'https://wachannelexporter.me',
      generateRobotsTxt: false,
      dynamicRoutes: [
        '/',
        '/export-to-pdf',
        '/download-media',
        '/documentation',
        '/privacy-policy',
        '/about',
        '/support',
        '/faq',
        '/how-to-export-whatsapp-channel-messages',
        '/whatsapp-channel-archive-guide',
        '/terms-of-service',
        '/es/',
        '/es/privacy-policy',
        '/es/support',
        '/pt-br/',
        '/pt-br/privacy-policy',
        '/pt-br/support'
      ]
    })
  ],
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        pdf: resolve(__dirname, 'export-to-pdf.html'),
        media: resolve(__dirname, 'download-media.html'),
        privacy: resolve(__dirname, 'privacy-policy.html'),
        docs: resolve(__dirname, 'documentation.html'),
        about: resolve(__dirname, 'about.html'),
        support: resolve(__dirname, 'support.html'),
        faq: resolve(__dirname, 'faq.html'),
        exportGuide: resolve(__dirname, 'how-to-export-whatsapp-channel-messages.html'),
        archiveGuide: resolve(__dirname, 'whatsapp-channel-archive-guide.html'),
        terms: resolve(__dirname, 'terms-of-service.html'),
        es: resolve(__dirname, 'es/index.html'),
        esPrivacy: resolve(__dirname, 'es/privacy-policy.html'),
        esSupport: resolve(__dirname, 'es/support.html'),
        ptBr: resolve(__dirname, 'pt-br/index.html'),
        ptBrPrivacy: resolve(__dirname, 'pt-br/privacy-policy.html'),
        ptBrSupport: resolve(__dirname, 'pt-br/support.html')
      }
    }
  }
});
