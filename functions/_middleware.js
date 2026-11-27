// Bloqueio geográfico: só o Brasil acessa o site.
// Exceção: robôs verificados de buscadores (Google, Bing etc.), para o site continuar no Google.
const PAISES = new Set(['BR']);

const bloqueado = () =>
  new Response(
    `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Acesso restrito</title><style>body{font-family:system-ui,Arial,sans-serif;background:#060b14;color:#e6eefc;display:grid;place-items:center;min-height:100vh;margin:0;text-align:center;padding:1rem}h1{font-size:1.6rem;margin:0 0 .5rem}p{color:#9fb0cc;margin:0}</style></head><body><main><h1>Acesso restrito</h1><p>Este site está disponível apenas no Brasil.</p><p lang="en" style="margin-top:.6rem">This website is only available in Brazil.</p></main></body></html>`,
    { status: 403, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains' } }
  );

function buscadorVerificado(request, cf) {
  // Só buscadores (Google, Bing etc.). Outros robôs verificados (monitoramento, IA, SEO) continuam bloqueados.
  if (cf.verifiedBotCategory === 'Search Engine Crawler') return true;
  const ua = (request.headers.get('User-Agent') || '').toLowerCase();
  const asn = Number(cf.asn);
  if (/googlebot|google-inspectiontool|googleother|adsbot-google|mediapartners-google|storebot-google/.test(ua) && asn === 15169) return true; // rede do Google
  if (/bingbot|adidxbot|bingpreview/.test(ua) && asn === 8075) return true; // rede da Microsoft
  return false;
}

export async function onRequest(context) {
  const { request, next } = context;
  const cf = request.cf;
  if (!cf) return next(); // ambiente local (sem dados do Cloudflare)
  if (PAISES.has(cf.country)) return next();
  if (buscadorVerificado(request, cf)) return next();
  return bloqueado();
}
