import { getCollection } from 'astro:content';

export async function getArtigos() {
  const posts = await getCollection('artigos', ({ data }) => import.meta.env.DEV || !data.draft);
  return posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}

export async function getNoticias() {
  const items = await getCollection('noticias');
  return items.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}
