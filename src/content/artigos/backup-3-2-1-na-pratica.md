---
title: 'Backup 3-2-1 na prática: como montar uma estratégia confiável'
description: 'Entenda a regra 3-2-1, a variação 3-2-1-1-0 e como aplicá-la em ambientes locais e na nuvem.'
pubDate: 2026-10-29
category: infraestrutura
tags: ['backup', 'infraestrutura', 'cloud']
---

A regra **3-2-1** continua sendo a base de qualquer estratégia de backup:

| Item | Significado |
|------|-------------|
| **3** | três cópias dos dados (produção + 2 backups) |
| **2** | em dois tipos de mídia diferentes |
| **1** | uma cópia fora do local (offsite / nuvem) |

## A evolução: 3-2-1-1-0

- **+1** cópia **imutável ou offline** (proteção contra ransomware);
- **0** erros na verificação — ou seja, **teste a restauração** regularmente.

## Exemplo de arquitetura

```text
Servidores/VMs ──> Repositório local (NAS) ──> Cópia em nuvem (Object Storage, imutável)
```

Defina RPO (quanto dado você aceita perder) e RTO (quanto tempo pode ficar parado) antes de escolher ferramentas.
