// Gera as versões do logo (fundo transparente) a partir de src/assets/image.png.
// Executado automaticamente antes do build (npm run build).
import sharp from 'sharp';
import { mkdirSync } from 'node:fs';

const SRC = 'src/assets/image.png';
mkdirSync('public', { recursive: true });

async function transparent(region) {
  const { data, info } = await sharp(SRC).extract(region).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  const out = Buffer.alloc(info.width * info.height * 4);
  for (let i = 0, j = 0; i < data.length; i += 3, j += 4) {
    const r = data[i], g = data[i + 1], b = data[i + 2];
    const m = Math.max(r, g, b);
    out[j] = r; out[j + 1] = g; out[j + 2] = b;
    out[j + 3] = m < 16 ? 0 : Math.min(255, (m - 16) * 2.4);
  }
  return sharp(out, { raw: { width: info.width, height: info.height, channels: 4 } });
}

const full = { left: 130, top: 150, width: 1010, height: 895 };
const emblem = { left: 171, top: 167, width: 927, height: 696 };

await (await transparent(full)).resize({ width: 480 }).webp({ quality: 70, alphaQuality: 70, effort: 6 }).toFile('public/logo-full.webp');
await (await transparent(emblem)).resize({ height: 110 }).webp({ quality: 75, alphaQuality: 70, effort: 6 }).toFile('public/logo-emblem.webp');
const emb = await (await transparent(emblem)).png().toBuffer();
await sharp(emb).resize(64, 64, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } }).png().toFile('public/favicon.png');
await sharp(emb).resize(180, 180, { fit: 'contain', background: '#04070d' }).flatten({ background: '#04070d' }).png().toFile('public/apple-touch-icon.png');
console.log('Logos gerados em public/');
