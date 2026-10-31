---
title: "Segurança na nuvem: o modelo de responsabilidade compartilhada"
description: "O provedor protege a plataforma; o cliente protege o que coloca nela. Entender essa divisão evita falhas graves."
pubDate: 2026-12-20
slug: responsabilidade-compartilhada
category: cloud
tags: ['cloud', 'segurança', 'responsabilidade compartilhada', 'configuração']
---

Uma das maiores fontes de incidentes em nuvem não é a falha do provedor, mas a **configuração incorreta feita pelo cliente**. Por isso, entender o modelo de responsabilidade compartilhada é essencial.

## Quem cuida do quê

**O provedor é responsável por:**
- Datacenters, energia, refrigeração e segurança física;
- Hardware, rede física e virtualização;
- Disponibilidade dos serviços contratados.

**O cliente é responsável por:**
- Identidades, senhas, MFA e permissões;
- Configuração de redes, firewalls e exposição de serviços;
- Proteção, classificação e backup dos dados;
- Atualização de sistemas operacionais em máquinas virtuais;
- Conformidade com leis e normas aplicáveis.

A divisão muda conforme o modelo: em **IaaS**, o cliente cuida de mais camadas; em **SaaS**, de menos. Mas **dados e acessos são sempre responsabilidade do cliente**.

## Falhas comuns

- Armazenamento de arquivos aberto publicamente por engano;
- Contas administrativas sem MFA;
- Chaves de acesso expostas em código;
- Portas de gerenciamento abertas para a internet;
- Ausência de logs e alertas.

## Boas práticas

1. Privilégio mínimo e revisão periódica de acessos;
2. MFA para todas as contas, especialmente administrativas;
3. Ferramentas de postura de segurança (CSPM) para detectar configurações de risco;
4. Criptografia de dados em repouso e em trânsito;
5. Backups independentes do ambiente principal.

Nuvem segura é resultado de boas decisões do cliente sobre uma plataforma segura.
