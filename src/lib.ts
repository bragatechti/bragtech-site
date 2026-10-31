import { getCollection } from 'astro:content';

export async function getArtigos() {
  const posts = await getCollection('artigos', ({ data }) => import.meta.env.DEV || !data.draft);
  return posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}

export async function getNoticias() {
  const items = await getCollection('noticias');
  return items.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}

export function readingTime(text: string) {
  const words = text.trim().split(/\s+/).length;
  return Math.max(1, Math.round(words / 200));
}

export function timeAgo(date: Date) {
  const diff = (Date.now() - date.getTime()) / 1000;
  if (diff < 3600) return `há ${Math.max(1, Math.round(diff / 60))} min`;
  if (diff < 86400) return `há ${Math.round(diff / 3600)} h`;
  const d = Math.round(diff / 86400);
  return d === 1 ? 'há 1 dia' : `há ${d} dias`;
}
