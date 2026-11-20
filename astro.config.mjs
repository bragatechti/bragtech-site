import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { readdirSync, readFileSync } from 'node:fs';

// Datas dos artigos (updatedDate ou pubDate) para o <lastmod> do sitemap
const dir = './src/content/artigos';
const datas = {};
for (const f of readdirSync(dir).filter((f) => /\.mdx?$/.test(f))) {
  const fm = readFileSync(`${dir}/${f}`, 'utf8').split('---')[1] || '';
  const get = (k) => (fm.match(new RegExp(`^${k}:\\s*['"]?([^'"\\n]+)`, 'm')) || [])[1];
  const d = new Date(get('updatedDate') || get('pubDate'));
  if (!isNaN(d)) datas[`/artigos/${get('slug') || f.replace(/\.mdx?$/, '')}/`] = d;
}
const agora = new Date();

export default defineConfig({
  site: 'https://www.bragagnolo.tec.br',
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/404'),
      serialize(item) {
        const path = new URL(item.url).pathname;
        item.lastmod = (datas[path] ?? agora).toISOString();
        return item;
      },
    }),
  ],
});
