export const SITE_TITLE = 'BragaTech';
export const SITE_TAGLINE = 'Tecnologia que informa. Segurança que protege.';
export const SITE_DESCRIPTION =
  'Portal de notícias e análises sobre Inteligência Artificial, Cibersegurança, Cloud, Infraestrutura e o mundo da tecnologia.';

export const CATEGORIES = [
  { slug: 'ia', name: 'Inteligência Artificial', short: 'IA', desc: 'LLMs, agentes, Copilot, Gemini, Claude, governança e o impacto da IA.', color: '#a855f7', icon: 'ia' },
  { slug: 'ciberseguranca', name: 'Cibersegurança', short: 'Segurança', desc: 'Ameaças, ransomware, vulnerabilidades, SOC, Zero Trust e LGPD.', color: '#ff7a1a', icon: 'shield' },
  { slug: 'cloud', name: 'Cloud Computing', short: 'Cloud', desc: 'Azure, AWS, Google Cloud, multicloud e FinOps.', color: '#38bdf8', icon: 'cloud' },
  { slug: 'infraestrutura', name: 'Infraestrutura de TI', short: 'Infra', desc: 'Redes, servidores, virtualização, observabilidade e backup.', color: '#22c55e', icon: 'server' },
  { slug: 'tecnologia', name: 'Tecnologia & Mercado', short: 'Tecnologia', desc: 'Big techs, gadgets, software, negócios e inovação.', color: '#1e9bff', icon: 'chip' },
] as const;

export type CategorySlug = (typeof CATEGORIES)[number]['slug'];
export const getCategory = (slug: string) => CATEGORIES.find((c) => c.slug === slug) ?? CATEGORIES[4];
export const categoryName = (slug: string) => getCategory(slug).name;

export const CREATOR = {
  name: 'José Raul Bragagnolo Filho',
  role: 'Coordenador de Infraestrutura, Segurança da Informação e IA',
  headline: 'Gestão de TI • Infraestrutura • Cloud (Azure/AWS) • Cybersecurity • Plataformas de IA',
  linkedin: 'https://www.linkedin.com/in/joseraulbragagnolofilho/',
  location: 'São Paulo, Brasil',
};
