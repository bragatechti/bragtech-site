#!/usr/bin/env python3
"""Cotações e indicadores do mercado financeiro (fontes públicas e gratuitas).

- Moedas: AwesomeAPI (economia.awesomeapi.com.br)
- Bolsas: Yahoo Finance (cotações com atraso)
- Juros e inflação: API SGS do Banco Central do Brasil

Grava src/content/noticias/_data/mercado.json. Se alguma fonte falhar,
mantém o último valor conhecido.
"""
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "content" / "noticias" / "_data" / "mercado.json"
UA = {"User-Agent": "Mozilla/5.0 (compatible; BragaTechBot/1.0; +https://www.bragagnolo.tec.br)"}

MOEDAS = [("USD-BRL", "USDBRL", "Dólar"), ("EUR-BRL", "EURBRL", "Euro"),
          ("GBP-BRL", "GBPBRL", "Libra"), ("BTC-BRL", "BTCBRL", "Bitcoin")]
YAHOO_FX = {"USD-BRL": "USDBRL=X", "EUR-BRL": "EURBRL=X", "GBP-BRL": "GBPBRL=X", "BTC-BRL": "BTC-BRL"}
BOLSAS = [("^BVSP", "Ibovespa", "Brasil"), ("^GSPC", "S&P 500", "EUA"), ("^IXIC", "Nasdaq", "EUA"),
          ("^DJI", "Dow Jones", "EUA"), ("^STOXX50E", "Euro Stoxx 50", "Europa"), ("^N225", "Nikkei 225", "Japão")]
JUROS = [(432, "selic", "Selic (meta)", "% a.a."), (4389, "cdi", "CDI", "% a.a."),
         (13522, "ipca", "IPCA (12 meses)", "%")]


def get_json(url: str):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def yahoo(sym: str):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}?range=5d&interval=1d"
    meta = get_json(url)["chart"]["result"][0]["meta"]
    price = float(meta["regularMarketPrice"])
    base = float(meta.get("chartPreviousClose") or meta.get("previousClose") or price)
    return price, (round((price / base - 1) * 100, 2) if base else 0.0)


def main() -> None:
    old = {}
    if OUT.exists():
        try:
            old = json.loads(OUT.read_text(encoding="utf-8"))
        except ValueError:
            old = {}
    prev = {i["id"]: i for k in ("moedas", "bolsas", "juros") for i in old.get(k, [])}

    moedas = []
    try:
        data = get_json("https://economia.awesomeapi.com.br/json/last/" + ",".join(m[0] for m in MOEDAS))
    except Exception as exc:  # noqa: BLE001
        print(f"[AVISO] Moedas: {exc}")
        data = {}
    for pair, key, nome in MOEDAS:
        d = data.get(key)
        if d:
            moedas.append({"id": pair, "nome": nome, "valor": float(d["bid"]), "var": float(d["pctChange"])})
            continue
        try:  # alternativa: Yahoo Finance
            price, var = yahoo(YAHOO_FX[pair])
            moedas.append({"id": pair, "nome": nome, "valor": price, "var": var})
        except Exception as exc:  # noqa: BLE001
            print(f"[AVISO] {nome}: {exc}")
            if pair in prev:
                moedas.append(prev[pair])

    bolsas = []
    for sym, nome, regiao in BOLSAS:
        try:
            price, var = yahoo(sym)
            bolsas.append({"id": sym, "nome": nome, "regiao": regiao, "valor": price, "var": var})
        except Exception as exc:  # noqa: BLE001
            print(f"[AVISO] {nome}: {exc}")
            if sym in prev:
                bolsas.append(prev[sym])

    juros = []
    for serie, jid, nome, unidade in JUROS:
        try:
            d = get_json(f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie}/dados/ultimos/1?formato=json")[-1]
            juros.append({"id": jid, "nome": nome, "valor": float(d["valor"]), "unidade": unidade, "ref": d["data"]})
        except Exception as exc:  # noqa: BLE001
            print(f"[AVISO] {nome}: {exc}")
            if jid in prev:
                juros.append(prev[jid])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "moedas": moedas, "bolsas": bolsas, "juros": juros,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Mercado: {len(moedas)} moedas, {len(bolsas)} bolsas, {len(juros)} indicadores")


if __name__ == "__main__":
    main()
