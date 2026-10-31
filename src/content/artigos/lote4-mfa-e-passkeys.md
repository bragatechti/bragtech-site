---
title: "Senhas, MFA e passkeys: o fim da senha está perto?"
description: "Credenciais roubadas seguem entre as principais portas de entrada de ataques. Veja como MFA e passkeys mudam esse cenário."
pubDate: 2026-11-30
slug: mfa-e-passkeys
category: ciberseguranca
tags: ['segurança', 'mfa', 'passkeys', 'identidade']
---

Senhas fracas, reutilizadas ou vazadas continuam sendo uma das formas mais simples de um atacante entrar em um ambiente. A boa notícia: existem alternativas maduras.

## O problema da senha

- Pessoas reutilizam a mesma senha em vários serviços;
- Vazamentos de terceiros expõem credenciais corporativas;
- Phishing captura senhas com páginas falsas muito convincentes.

## MFA: o mínimo obrigatório

A autenticação multifator exige algo além da senha: um código, uma aprovação no celular ou uma chave física. Mesmo que a senha vaze, o acesso não acontece sem o segundo fator.

Mas atenção: **nem todo MFA é igual**. SMS é melhor que nada, porém vulnerável a troca de chip (SIM swap). Aplicativos autenticadores e chaves físicas são mais seguros. Também é importante se proteger da "fadiga de MFA", quando o atacante dispara notificações até o usuário aprovar por cansaço; a correspondência de número resolve boa parte disso.

## Passkeys: o próximo passo

As **passkeys** usam criptografia de chave pública, baseada nos padrões FIDO2/WebAuthn. A chave privada fica no dispositivo do usuário e é liberada por biometria ou PIN. Não há senha para vazar nem para digitar em página falsa.

## Recomendações práticas

1. MFA obrigatório para e-mail, VPN, acesso remoto e contas administrativas;
2. Prefira métodos resistentes a phishing (chaves físicas e passkeys);
3. Use gerenciador de senhas corporativo;
4. Monitore vazamentos de credenciais do seu domínio;
5. Revise acessos privilegiados periodicamente.

A senha ainda não morreu, mas sozinha ela já não protege ninguém.
