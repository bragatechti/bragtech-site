import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const categoria = z.enum(['ciberseguranca', 'cloud', 'infraestrutura', 'tecnologia']);

const artigos = defineCollection({
  loader: glob({ base: './src/content/artigos', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    category: categoria,
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const noticias = defineCollection({
  loader: glob({ base: './src/content/noticias', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    summary: z.string().default(''),
    pubDate: z.coerce.date(),
    category: categoria,
    source: z.string(),
    sourceUrl: z.string().url(),
  }),
});

export const collections = { artigos, noticias };
