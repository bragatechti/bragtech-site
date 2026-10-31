// Cloudflare Pages Function: POST /api/contato
// Envia o formulário do site por e-mail via Brevo, com remetente contato@bragagnolo.tec.br.
// Requer a variável de ambiente (secreta) BREVO_API_KEY configurada no Cloudflare Pages.

const SENDER = { name: 'BragaTech Contato', email: 'contato@bragagnolo.tec.br' };
const TO = [{ email: 'raul@bragagnolo.tec.br', name: 'Raul Bragagnolo' }];
const ALLOWED_ORIGINS = ['https://www.bragagnolo.tec.br', 'https://bragagnolo.tec.br', 'https://bragtech-site.pages.dev'];

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json; charset=utf-8' } });

const esc = (s) =>
  String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const clean = (s, max) => String(s ?? '').replace(/[\r\n]+/g, ' ').trim().slice(0, max);

export async function onRequestPost({ request, env }) {
  const origin = request.headers.get('Origin') || '';
  if (origin && !ALLOWED_ORIGINS.includes(origin) && !origin.endsWith('.bragtech-site.pages.dev')) {
    return json({ success: false, message: 'Origem não permitida.' }, 403);
  }
  if (!env.BREVO_API_KEY) return json({ success: false, message: 'Envio não configurado.' }, 503);

  let data;
  try {
    data = await request.json();
  } catch {
    return json({ success: false, message: 'Requisição inválida.' }, 400);
  }
  if (data.botcheck) return json({ success: true });

  const nome = clean(data.nome, 100);
  const email = clean(data.email, 120);
  const celular = clean(data.celular, 20);
  const whatsapp = clean(data.whatsapp, 20) || '(não informado)';
  const assunto = String(data.assunto ?? '').trim().slice(0, 3000);

  if (!nome || !assunto || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || celular.replace(/\D/g, '').length < 10) {
    return json({ success: false, message: 'Preencha todos os campos obrigatórios.' }, 422);
  }
  if (data.consentimento !== 'sim') return json({ success: false, message: 'Consentimento obrigatório.' }, 422);

  const linha = (k, v) =>
    `<tr><td style="padding:8px 12px;background:#0b1626;color:#7fb8ff;font-weight:600;width:140px">${k}</td><td style="padding:8px 12px;background:#101c2e;color:#e6eefc">${v}</td></tr>`;

  const htmlContent = `
  <div style="font-family:Arial,Helvetica,sans-serif;max-width:640px;margin:auto;background:#060b14;padding:24px;border-radius:12px">
    <h2 style="color:#38d6ff;margin:0 0 4px">Novo contato pelo site</h2>
    <p style="color:#9fb0cc;margin:0 0 16px">Formulário de contato da BragaTech</p>
    <table style="border-collapse:collapse;width:100%;border-radius:8px;overflow:hidden">
      ${linha('Nome', esc(nome))}
      ${linha('E-mail', `<a style="color:#38d6ff" href="mailto:${esc(email)}">${esc(email)}</a>`)}
      ${linha('Celular', esc(celular))}
      ${linha('WhatsApp', esc(whatsapp))}
      ${linha('Assunto', esc(assunto).replace(/\n/g, '<br>'))}
      ${linha('LGPD', 'Consentimento registrado')}
    </table>
    <p style="color:#6f7f99;font-size:12px;margin:16px 0 0">Responda este e-mail para falar diretamente com ${esc(nome)}.</p>
  </div>`;

  const textContent = `Novo contato pelo site BragaTech\n\nNome: ${nome}\nE-mail: ${email}\nCelular: ${celular}\nWhatsApp: ${whatsapp}\n\nAssunto:\n${assunto}\n\nConsentimento LGPD: sim`;

  const res = await fetch('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: { 'api-key': env.BREVO_API_KEY, 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify({
      sender: SENDER,
      to: TO,
      replyTo: { email, name: nome },
      subject: `Contato pelo site BragaTech: ${nome}`,
      htmlContent,
      textContent,
      tags: ['formulario-site'],
    }),
  });

  if (!res.ok) {
    console.log('Brevo error', res.status, await res.text());
    return json({ success: false, message: 'Falha no envio.' }, 502);
  }
  return json({ success: true });
}

export const onRequest = () => json({ success: false, message: 'Método não permitido.' }, 405);
