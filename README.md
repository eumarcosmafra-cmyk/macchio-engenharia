# Macchio Engenharia — novo site (v4)

Redesign do site https://macchioengenharia.com.br/ (WordPress 6.1 + Elementor) como site estático: HTML, CSS e JS puros, sem framework. As páginas são geradas por um script Python a partir de um JSON com os dados das obras.

- Prévia: https://macchio-engenharia.vercel.app/ (com `noindex` em `*.vercel.app`)
- A v3 aplicou o "Plano de melhorias UX/UI" enviado em 29/10/2026.
- A v4 mantém **exatamente as mesmas URLs do site atual**: cada página existente tem a sua própria página, com os mesmos slugs.

## Estrutura (idêntica ao sitemap do WordPress: 22 URLs)

| URL | Conteúdo |
|---|---|
| `/` | Hero com posicionamento, 2 CTAs e atalhos por serviço · "Nós somos a Macchio" + registros (link para Sobre) · grade com 6 projetos (link para Portfólio) · resumo dos 4 serviços (link para Serviços) · 3 depoimentos · faixa de orçamento |
| `/sobre/` | "Nós somos a Macchio" · história e fundador · missão, visão e valores (texto do site atual) · dados da empresa · faixa de orçamento |
| `/servicos/` | "Nossos serviços" · 4 cards (o que inclui + WhatsApp próprio + formulário já com o serviço escolhido) · etapas do atendimento · FAQ · faixa de orçamento |
| `/portfolio/` | 17 projetos em grade uniforme ou lista; filtro por tipo |
| `/portfolio/<slug original>/` | As 17 páginas de projeto, com os slugs do site atual (inclusive `https-macchioengenharia-com-br-portfolio-residencia-unifamiliar-n-e-a`, mantido para não quebrar a URL indexada). Título descritivo + nome original, ficha técnica, descrição, galeria, plantas, CTA e relacionados |
| `/contato/` | "O que você precisa resolver?" · formulário que abre o WhatsApp com a mensagem pronta (aceita `?interesse=projetos\|obras\|financiamento\|imoveis\|regularizacao`) · canais de contato |

Menu igual ao atual: Início · Sobre a empresa · Serviços · Portfólio · Contato · botão **Orçamento** (para `/contato/`).

## Regras de conteúdo aplicadas

- **Render × obra:** todas as imagens do portfólio são perspectivas 3D. Isso aparece no selo de cada card, na legenda da imagem principal, no texto das seções e no FAQ.
- **Escopo:** "Projeto" para todas as obras. "Execução: prevista pela Macchio" só nas 4 em que o site atual diz "a execução dessa obra também será da Macchio" (P e R, Multifamiliar 01, 02 e 03). Nenhuma obra é apresentada como executada.
- **Títulos descritivos** (ex.: "Chalé com mezanino e vista panorâmica em Aurora") tirados da descrição real de cada obra. O nome original (ex.: "Residência P e R") aparece logo abaixo.
- **Financiamento:** sem promessa de aprovação. Há um aviso de que crédito, condições e prazos dependem da instituição financeira.
- **WhatsApp contextual:** cada serviço e cada obra abre o WhatsApp com uma mensagem própria. O formulário monta a mensagem a partir da área escolhida e informa o que acontece depois do envio.
- **Sem carrossel, slideshow ou texto escondido:** depoimentos, etapas e serviços ficam visíveis de uma vez.

## Qualidade (Lighthouse 12.6, celular, servidor local, 29/10/2026)

| Página | Performance | Acessibilidade | Boas práticas | SEO |
|---|---|---|---|---|
| Início | 98 | 100 | 100 | 100 |
| Sobre | 99 | 100 | 100 | 100 |
| Serviços | 99 | 100 | 100 | 100 |
| Contato | 99 | 100 | 100 | 100 |
| Portfólio | 95 | 100 | 100 | 100 |
| Projeto (P e R) | 99 | 100 | 100 | 100 |

Os números finais devem ser confirmados no PageSpeed com o domínio definitivo.

Testado: rastreamento completo pelos links internos (as 22 páginas são alcançadas, sem link quebrado e com um H1 por página), sitemap idêntico ao do WordPress, menu mobile, filtros e lista, galeria por teclado e toque, formulário (validação, confirmação e serviço pré-selecionado), mensagens de WhatsApp e console sem erros.

## Como editar

1. Dados das obras: `_build/projetos.json` (título descritivo, nome, tipo, cidade, área, escopo, execução, descrição, imagens).
2. Serviços, etapas, depoimentos, FAQ e mensagens de WhatsApp: constantes no topo de `_build/build.py`.
3. Gerar as páginas: `python3 _build/build.py` (precisa do Pillow para as imagens OG).
4. Estilos: `assets/css/site.css`. Interações: `assets/js/site.js`.

## Validar com a Macchio antes de publicar no domínio

1. **Serviços:** confirmar as entregas listadas em cada card. Saíram do site atual e dos depoimentos: tipos de projeto, regularização, ampliação, execução × gerenciamento, reuniões de acompanhamento, intermediação, busca de terrenos e apoio burocrático.
2. **Prioridade comercial:** qual serviço destacar primeiro. Hoje a ordem é Projetos → Obras → Financiamento → Imóveis.
3. **Execução das 4 obras "previstas":** se foram executadas, trocar para "Obra executada" e, se possível, incluir fotos reais da obra pronta.
4. **Títulos descritivos:** revisar os 17 títulos em `_build/projetos.json`.
5. **Cidade da F e M** ("Autora" no site atual, corrigido para Aurora/SC), **N e C** (publicada como residência) e **J e D** (ampliação e interiores).
6. **Facebook oficial** (`/macchio.imobi` × `/macchio.eng`), **razão social/CNPJ**, **titular do CREA 177418-0**.
7. **Logo vetorial oficial** e **foto do Djonas e do escritório**.
8. **Domínio da imobiliária** (macchioimobiliaria.com.br): unificar aqui com 301.
9. **Formulário:** hoje abre o WhatsApp. Se quiserem receber por e-mail também, é preciso um serviço de envio (Formspree, Resend etc.).

## Publicar

- Vercel: cada push na `main` atualiza o site. Framework "Other", sem build command. `_build/` e este README ficam fora do deploy (`.vercelignore`).
- Endereços `*.vercel.app` recebem `X-Robots-Tag: noindex` (em `vercel.json`) para a prévia não competir no Google com o site atual. O domínio final não é afetado.
- As URLs são as mesmas do WordPress, então não há redirect de páginas. `vercel.json` só redireciona resíduos do WordPress (`/feed/`, `/comments/feed/`, `/author/*`, `/elementor-hf/*` → início; `/wp-sitemap.xml` → `/sitemap.xml`) e os links da prévia anterior (`/projetos/*` → `/portfolio/*`). `trailingSlash: true` mantém a barra final, como no WordPress.
- Imagens antigas (`/wp-content/uploads/...`) não são redirecionadas. Se o Google Imagens trouxer tráfego relevante para elas, dá para mapeá-las depois.
