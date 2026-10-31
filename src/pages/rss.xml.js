import rss from '@astrojs/rss';
import { SITE_TITLE, SITE_DESCRIPTION } from '../consts';
import { getArtigos } from '../lib';

export async function GET(context) {
  const posts = await getArtigos();
  return rss({
    title: SITE_TITLE,
    description: SITE_DESCRIPTION,
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      link: `/artigos/${post.id}/`,
    })),
    customData: '<language>pt-br</language>',
  });
}
