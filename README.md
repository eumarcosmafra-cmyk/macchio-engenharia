# Macchio Engenharia — novo site (v3)

Redesign do site https://macchioengenharia.com.br/ (WordPress 6.1 + Elementor) como site estático: HTML, CSS e JS puros, sem framework. As páginas são geradas por um script Python a partir de um JSON com os dados das obras.

- Prévia: https://macchio-engenharia.vercel.app/ (com `noindex` em `*.vercel.app`)
- A v3 aplica o "Plano de melhorias UX/UI" enviado em 29/10/2026.

## Estrutura

| URL | Conteúdo |
|---|---|
| `/` | Hero (posicionamento + serviços + 2 CTAs + atalhos por serviço) · resumo e registros · **grade com 6 projetos** e "Ver todos" · **4 cards de serviço** (o que inclui + CTA de WhatsApp próprio) · **etapas do atendimento** em grade, cada uma com a frente correspondente · 3 depoimentos · sobre · FAQ · contato "O que você precisa resolver?" |
| `/projetos/` | 17 projetos em grade uniforme (16:10) ou lista; filtro por tipo, com aviso para leitor de tela |
| `/projetos/<obra>/` | Título descritivo + nome original, ficha técnica (tipo, cidade, área, escopo, execução, tipo de imagem), imagem principal sem corte, descrição real, galeria completa em 16:9 com ampliação, plantas, CTA "Solicitar um projeto semelhante" e 3 projetos relacionados |

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
| Home | 97 | 100 | 100 | 100 |
| Projetos | 97 | 100 | 100 | 100 |
| Obra (P e R) | 99 | 100 | 100 | 100 |

Os números finais devem ser confirmados no PageSpeed com o domínio definitivo.

Testado: menu mobile, âncoras (o header não encobre títulos), filtros, visualização em lista, galeria por teclado, toque e botões, validação e confirmação do formulário, mensagens de WhatsApp, 19 URLs do sitemap sem erro e console sem erros.

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
- `vercel.json` traz os 301 de cada `/portfolio/<slug-antigo>/` para a nova `/projetos/<obra>/`, além de `/sobre`, `/servicos`, `/contato` e `/portfolio`.
