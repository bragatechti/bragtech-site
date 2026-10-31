---
title: "Firewall de nova geração: o que muda na prática"
description: "NGFW vai além de liberar portas: identifica aplicações, usuários e ameaças. Entenda o que considerar na escolha e na operação."
pubDate: 2026-11-30
slug: firewall-de-nova-geracao
category: infraestrutura
tags: ['infraestrutura', 'firewall', 'rede', 'segurança']
---

O firewall tradicional decidia com base em IP e porta. Hoje quase tudo trafega pelas portas 80 e 443, e esse modelo já não é suficiente. O **firewall de nova geração (NGFW)** resolve essa lacuna.

## O que um NGFW faz

- **Controle por aplicação:** distingue, por exemplo, uso corporativo de uma ferramenta de colaboração do uso de um serviço de streaming;
- **Identidade:** regras por usuário e grupo, integradas ao diretório;
- **IPS:** detecção e bloqueio de explorações conhecidas;
- **Filtro web e DNS:** bloqueio de categorias e domínios maliciosos;
- **Inspeção TLS:** análise de tráfego criptografado, quando permitido pela política.

## Erros comuns

1. **Regra "any-any" esquecida:** o equipamento é moderno, mas a política continua permissiva;
2. **Recursos comprados e desligados:** IPS e filtro web desativados para "não dar problema";
3. **Firmware desatualizado:** dispositivos de borda são alvos frequentes de vulnerabilidades críticas;
4. **Gerência exposta à internet:** a interface administrativa nunca deve ficar aberta.

## Boas práticas

- Revisão periódica de regras, removendo o que não é usado;
- Segmentação interna, não só proteção de perímetro;
- Logs enviados para uma central (SIEM) e monitorados;
- Alta disponibilidade para links e equipamentos críticos;
- Janela regular de atualização.

Firewall bom é o que está bem configurado, atualizado e monitorado. A marca vem depois.
