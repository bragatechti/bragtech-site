# BragaTech — www.bragagnolo.tec.br

Portal de tecnologia, cloud e cibersegurança. 100% gratuito: **Astro** (site estático) + **GitHub Actions** (notícias automáticas) + **Cloudflare Pages** (hospedagem + HTTPS).

## Como publicar um artigo novo (pelo navegador)
1. Abra a pasta `src/content/artigos/` no GitHub → **Add file → Create new file**.
2. Nome: `meu-artigo.md` (o nome vira a URL: `/artigos/meu-artigo/`).
3. Copie o cabeçalho do arquivo `_MODELO-novo-artigo.md.txt`, preencha e escreva em Markdown.
4. **Commit changes** → em ~1 minuto o Cloudflare publica o site atualizado.

## Notícias automáticas
- `.github/workflows/news.yml` roda 2x por dia (06:17 e 18:17) e também manualmente em **Actions → Atualizar noticias → Run workflow**.
- Fontes em `data/feeds.json` (adicione/remova feeds RSS e defina a categoria: `ciberseguranca`, `cloud`, `infraestrutura`, `tecnologia`).
- Notícias com mais de 45 dias são removidas automaticamente.

## Estrutura
```
src/content/artigos/   artigos autorais (Markdown)
src/content/noticias/  notícias geradas pelo robô (não editar)
src/pages/             páginas (início, sobre, contato, privacidade, categorias)
src/styles/global.css  cores e visual
src/consts.ts          nome do site, slogan e categorias
scripts/fetch_news.py  coletor de RSS
```

## Cloudflare Pages
Framework: Astro · Build: `npm run build` · Saída: `dist` · Variável `NODE_VERSION=24`.

## Rodar localmente (opcional)
```
npm install
npm run dev
```
