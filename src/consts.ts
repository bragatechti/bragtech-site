export const SITE_TITLE = 'BragaTech';
export const SITE_TAGLINE = 'Tecnologia que informa. Segurança que protege.';
export const SITE_DESCRIPTION =
  'Artigos técnicos, notícias selecionadas, análises e tutoriais sobre cibersegurança, cloud computing e infraestrutura de TI.';

export const CATEGORIES = [
  { slug: 'ciberseguranca', name: 'Cibersegurança', desc: 'Ameaças, SOC, EDR, LGPD e proteção.' },
  { slug: 'cloud', name: 'Cloud Computing', desc: 'Azure, AWS, Google Cloud e multicloud.' },
  { slug: 'infraestrutura', name: 'Infraestrutura de TI', desc: 'Redes, servidores, virtualização e backup.' },
  { slug: 'tecnologia', name: 'Notícias de Tecnologia', desc: 'Microsoft, Google, IA e mercado.' },
] as const;

export type CategorySlug = (typeof CATEGORIES)[number]['slug'];
export const categoryName = (slug: string) =>
  CATEGORIES.find((c) => c.slug === slug)?.name ?? slug;
