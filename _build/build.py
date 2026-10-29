"""Gera as páginas estáticas do site da Macchio Engenharia.

Uso:  python3 _build/build.py
Lê _build/projetos.json e escreve as mesmas URLs do site atual (WordPress):
  /  ·  /sobre/  ·  /servicos/  ·  /portfolio/  ·  /portfolio/<slug-original>/  ·  /contato/
além de sitemap.xml e das imagens OG dos projetos.
"""
import html
import json
import shutil
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://macchioengenharia.com.br/"
WA_NUMBER = "5547991723557"
PHONE_HREF = "tel:+5547991723557"
PHONE = "(47) 99172-3557"
EMAIL = "contato@macchioengenharia.com.br"
ADDRESS = "R. XV de Novembro, 336, sala 01, Centro, Rio do Sul/SC"
CEP = "89160-033"
MAPS = "https://www.google.com/maps/search/?api=1&query=Rua+XV+de+Novembro%2C+336%2C+Centro%2C+Rio+do+Sul+-+SC%2C+89160-033"
INSTAGRAM = "https://www.instagram.com/macchio.eng"
FACEBOOK = "https://www.facebook.com/macchio.imobi"
CNPJ = "40.033.204/0001-43"
CREA = "CREA/SC 177418-0"
CRECI = "CRECI 6174-J"

PROJECTS = json.loads((ROOT / "_build/projetos.json").read_text(encoding="utf-8"))
BY_SLUG = {p["slug"]: p for p in PROJECTS}
CATS = [("all", "Todos"), ("unifamiliar", "Residências"), ("multifamiliar", "Multifamiliares"), ("interiores", "Interiores e ampliações")]
WORD = (ROOT / "_build/logo-word.path").read_text()

e = html.escape


def wa(msg):
    return f"https://wa.me/{WA_NUMBER}?text={quote(msg)}"


def two(n):
    return f"{n:02d}"


def purl(p):
    """URL da página do projeto: a mesma do site atual (/portfolio/<slug original>/)."""
    return f"portfolio/{p['old_slug']}/"


def city_uf(p):
    return f"{p['city']}/SC" if p["city"] else None


def full_title(p):
    return f"{p['title']} em {p['city']}" if p["city"] else p["title"]


def meta_line(p):
    return " · ".join(x for x in (p["type"], city_uf(p), p["area"]) if x)


def scope_line(p):
    return p["scope"] + (" · execução prevista pela Macchio" if p["exec"] else "")


# ---------- imagens ----------
def img_src(slug, file, prefix):
    folder = ROOT / "assets/img/projetos" / slug
    widths = [w for w in (800, 1280, 1600, 1920, 2400) if (folder / f"{file}-{w}.webp").exists()]
    base = f"{prefix}assets/img/projetos/{slug}/{file}"
    return f"{base}-800.webp", ", ".join(f"{base}-{w}.webp {w}w" for w in widths), f"{base}-{widths[-1]}.webp"


def img_tag(slug, file, prefix, alt, sizes, eager=False, vt=None, w=800, h=450):
    src, srcset, _ = img_src(slug, file, prefix)
    style = f' style="view-transition-name: {vt}"' if vt else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{src}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" {load} decoding="async" alt="{e(alt)}"{style}>'


def cover_alt(p):
    return f"Perspectiva 3D do projeto {p['name']}: {p['cover_alt'][0].lower()}{p['cover_alt'][1:]}"


def cover_tag(p, prefix, sizes, eager=False, vt=True):
    c = p["renders"][0]
    return img_tag(p["slug"], c["file"], prefix, cover_alt(p), sizes, eager=eager, vt=f"p-{p['slug']}" if vt else None, w=c["w"], h=c["h"])


# ---------- ícones ----------
ICONS = """
  <svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
    <symbol id="logo" viewBox="5 1.5 143 31"><path fill="currentColor" fill-rule="evenodd" d="{WORD}"/><text x="5" y="31.6" textLength="143" lengthAdjust="spacingAndGlyphs" font-size="5.4" font-weight="500" fill="currentColor">ENGENHARIA E NEGÓCIOS IMOBILIÁRIOS</text></symbol>
    <symbol id="i-arrow" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h16M14 6l6 6-6 6"/></g></symbol>
    <symbol id="i-prev" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12H4M10 6l-6 6 6 6"/></g></symbol>
    <symbol id="i-close" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></g></symbol>
    <symbol id="i-check" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></g></symbol>
    <symbol id="i-wa" viewBox="0 0 24 24"><path fill="currentColor" d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.47-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.42.25-.69.25-1.29.18-1.41-.08-.13-.27-.2-.57-.35M12.05 21.8h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.82 9.82 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.69 1.45c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.16-3.48-8.41Z"/></symbol>
  </svg>"""


def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} aria-hidden="true"><use href="#{name}"/></svg>'


def pill(label, href, cls="", track=None, whatsapp=False):
    icon = "i-wa" if whatsapp else "i-arrow"
    attrs = ' target="_blank" rel="noopener"' if whatsapp else ""
    tr = f' data-track="{track}"' if track else ""
    sr = '<span class="vh"> (abre o WhatsApp)</span>' if whatsapp else ""
    return (f'<a class="pill {cls}" href="{href}"{attrs}{tr}>{label}{sr}'
            f'<span class="pill-ic" aria-hidden="true">{ic(icon)}{ic(icon)}</span></a>')


def wa_link(label, msg, track, cls="link-u"):
    return (f'<a class="{cls}" href="{wa(msg)}" target="_blank" rel="noopener" data-track="{track}">'
            f'{ic("i-wa", "ic-wa")}{label}<span class="vh"> (abre o WhatsApp)</span></a>')


# ---------- layout ----------
def head(prefix, title, desc, path, og_image, jsonld, preload=""):
    return f"""<!doctype html>
<html lang="pt-BR" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <link rel="canonical" href="{SITE}{path}">
  <meta name="theme-color" content="#0a0a0a">
  <link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{prefix}favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="Macchio Engenharia e Negócios Imobiliários">
  <meta property="og:url" content="{SITE}{path}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:image" content="{SITE}{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <script>document.documentElement.classList.replace("no-js", "js")</script>
  <link rel="preload" href="{prefix}assets/fonts/geist-latin.woff2" as="font" type="font/woff2" crossorigin>
{preload}  <link rel="stylesheet" href="{prefix}assets/css/site.css">
  <script src="{prefix}assets/js/site.js" defer></script>
  <!-- Google Tag Manager / GA4: inserir o snippet aqui. Os cliques de CTA já vão para o dataLayer (evento "cta_click"). -->
  <script type="application/ld+json">
{json.dumps(jsonld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>"""


# Menu igual ao do site atual: Início · Sobre a Empresa · Serviços · Portfólio · Contato · Orçamento
NAV = [("inicio", "", "Início"), ("sobre", "sobre/", "Sobre a empresa"), ("servicos", "servicos/", "Serviços"),
       ("portfolio", "portfolio/", "Portfólio"), ("contato", "contato/", "Contato")]


def header(prefix, current="", solid=True):
    home = prefix or "./"
    nav = "\n        ".join(f'<a href="{(prefix + h) if h else home}"{" aria-current=\"page\"" if k == current else ""}>{t}</a>' for k, h, t in NAV)
    menu_links = "\n      ".join(f'<a href="{(prefix + h) if h else home}"{" aria-current=\"page\"" if k == current else ""}><span>{two(i)}</span>{t}</a>'
                                 for i, (k, h, t) in enumerate(NAV, 1))
    return f"""{ICONS}
  <a class="skip" href="#conteudo">Pular para o conteúdo</a>
  <header class="hd" data-header{" data-solid" if solid else ""}>
    <div class="wrap hd-in">
      <a class="hd-logo" href="{home}" aria-label="Macchio Engenharia e Negócios Imobiliários, página inicial"><svg aria-hidden="true"><use href="#logo"/></svg></a>
      <nav class="hd-nav" aria-label="Principal">
        {nav}
      </nav>
      {pill("Orçamento", f"{prefix}contato/", "pill--light pill--sm hd-cta", "header_orcamento")}
      <button class="hd-menu" type="button" data-menu-open aria-expanded="false" aria-haspopup="dialog">Menu <i aria-hidden="true"></i></button>
    </div>
  </header>
  <dialog class="menu" data-menu aria-label="Menu">
    <div class="wrap menu-top">
      <a class="hd-logo" href="{home}" aria-label="Página inicial"><svg aria-hidden="true"><use href="#logo"/></svg></a>
      <button class="hd-menu" type="button" data-menu-close>Fechar</button>
    </div>
    <nav class="wrap menu-nav" aria-label="Menu principal">
      {menu_links}
    </nav>
    <div class="wrap menu-foot">
      {pill("Pedir orçamento", f"{prefix}contato/", "pill--light", "menu_orcamento")}
      <p>{PHONE} · {EMAIL}<br>{ADDRESS}</p>
    </div>
  </dialog>"""


def footer(prefix):
    home = prefix or "./"
    return f"""
  <footer class="ft" data-footer>
    <div class="wrap">
      <div class="ft-cols">
        <div>
          <h2 class="label label--light">Macchio</h2>
          <p class="muted">Engenharia e imobiliária em Rio do Sul/SC.<br>Projetos, obras, financiamento e imóveis.</p>
        </div>
        <div>
          <h2 class="label label--light">Navegação</h2>
          <ul>
            <li><a href="{home}">Início</a></li>
            <li><a href="{prefix}sobre/">Sobre a empresa</a></li>
            <li><a href="{prefix}servicos/">Serviços</a></li>
            <li><a href="{prefix}portfolio/">Portfólio</a></li>
            <li><a href="{prefix}contato/">Contato</a></li>
          </ul>
        </div>
        <div>
          <h2 class="label label--light">Contato</h2>
          <ul>
            <li><a href="{PHONE_HREF}">{PHONE}</a></li>
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><a href="{MAPS}" target="_blank" rel="noopener">R. XV de Novembro, 336, sala 01<br>Centro, Rio do Sul/SC, {CEP}</a></li>
          </ul>
        </div>
        <div>
          <h2 class="label label--light">Redes</h2>
          <ul>
            <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li>
            <li><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a></li>
          </ul>
        </div>
      </div>
      <svg class="ft-logo" aria-hidden="true"><use href="#logo"/></svg>
      <div class="ft-legal mono">
        <span>© <span data-year>2026</span> Macchio Engenharia e Negócios Imobiliários Ltda</span>
        <span>CNPJ {CNPJ} · {CREA} · {CRECI}</span>
      </div>
    </div>
  </footer>
  <a class="fab" href="{wa('Olá! Gostaria de conversar com a equipe da Macchio.')}" target="_blank" rel="noopener" data-fab data-track="whatsapp_flutuante">{ic("i-wa")} WhatsApp<span class="vh"> (abre o WhatsApp)</span></a>"""


def write_page(path, prefix, title, desc, og_image, jsonld, body, current="", solid=True, preload=""):
    out = head(prefix, title, desc, path, og_image, jsonld, preload) + header(prefix, current, solid) + body + footer(prefix) + "\n</body>\n</html>\n"
    target = ROOT / path / "index.html" if path else ROOT / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out.replace("{WORD}", WORD), encoding="utf-8")


def crumbs(prefix, items):
    """items: lista de (rótulo, href ou None para a página atual)."""
    parts = [f'<a href="{prefix or "./"}">Início</a>']
    for label, href in items:
        parts.append('<span aria-hidden="true">/</span>')
        parts.append(f'<a href="{href}">{e(label)}</a>' if href else f'<span aria-current="page">{e(label)}</span>')
    return f'<nav class="crumbs mono" aria-label="Você está em">{"".join(parts)}</nav>'


def pagehead(prefix, label, h1, lead, crumb_items):
    return f"""
    <section class="pagehead dark" aria-labelledby="page-title">
      <div class="wrap">
        {crumbs(prefix, crumb_items)}
        <span class="label">{label}</span>
        <h1 class="h1" id="page-title">{h1}</h1>
        <p class="pagehead-lead">{lead}</p>
      </div>
    </section>"""


def cta_band(prefix, title="O que você precisa resolver?", text="Fale com a nossa equipe sobre projeto, obra, financiamento ou compra e venda de imóvel."):
    bg = img_tag("residencia-n-e-a", "06", prefix, "", "100vw")
    return f"""
    <section class="cta dark" aria-labelledby="band-title">
      <div class="cta-bg" aria-hidden="true">{bg}</div>
      <div class="wrap cta-in">
        <span class="label">Orçamento</span>
        <h2 class="h1" id="band-title">{title}</h2>
        <p class="cta-lead">{text}</p>
        <div class="band-actions">
          {pill("Pedir orçamento", f"{prefix}contato/", "pill--light", "band_orcamento")}
          {wa_link("Conversar no WhatsApp", MSG["outro"], "whatsapp_band")}
        </div>
      </div>
    </section>"""


# ---------- componentes ----------
def project_card(p, prefix, sizes, heading="h3", eager=False):
    return f"""        <li class="card" data-cat="{p["cat"]}">
          <a class="card-link" href="{prefix}{purl(p)}" data-cursor="Ver projeto">
            <div class="card-media">{cover_tag(p, prefix, sizes, eager=eager)}<span class="badge mono">Perspectiva 3D</span></div>
            <div class="card-body">
              <{heading} class="card-title">{e(p["title"])}</{heading}>
              <p class="card-name">{e(p["name"])}</p>
              <p class="card-meta mono">{e(meta_line(p))}</p>
              <p class="card-scope mono">{e(scope_line(p))}</p>
            </div>
          </a>
        </li>"""


CARD_SIZES = "(min-width: 1024px) 31vw, (min-width: 640px) 46vw, 100vw"

# ---------- conteúdo compartilhado ----------
ORG_ID = SITE + "#empresa"
INTERESTS = [
    ("projetos", "Projetos de engenharia e interiores", "Olá! Gostaria de entender melhor os serviços de projetos de engenharia e interiores e solicitar um orçamento."),
    ("obras", "Execução ou gerenciamento de obra", "Olá! Gostaria de conversar sobre execução ou gerenciamento de uma obra."),
    ("financiamento", "Financiamento imobiliário", "Olá! Gostaria de entender melhor o apoio oferecido pela Macchio no processo de financiamento imobiliário."),
    ("imoveis", "Compra ou venda de imóvel", "Olá! Gostaria de conversar sobre compra ou venda de um imóvel."),
    ("regularizacao", "Regularização de obra", "Olá! Gostaria de conversar sobre a regularização de uma obra."),
    ("outro", "Outro assunto", "Olá! Gostaria de conversar com a equipe da Macchio."),
]
MSG = {k: m for k, _, m in INTERESTS}
SERVICES = [
    ("projetos", "Projetos de engenharia e interiores",
     "Projetos para obras residenciais, comerciais e industriais e design de interiores, elaborados conforme as normas e os requisitos exigidos.",
     ["Projetos residenciais e comerciais", "Projetos para obras industriais", "Projetos de ampliação", "Design de interiores", "Regularização de obras"],
     "Solicitar orçamento de projeto", None),
    ("obras", "Execução e gerenciamento de obras",
     "Duas modalidades: a execução da obra ou o gerenciamento, em que você deixa a obra por nossa conta.",
     ["Execução com mão de obra qualificada e material de primeira linha", "Gerenciamento: a Macchio cuida da obra por você",
      "Acompanhamento de todas as etapas", "Reuniões periódicas de acompanhamento"],
     "Conversar sobre minha obra", None),
    ("financiamento", "Financiamento imobiliário",
     "Orientação e acompanhamento do processo de financiamento imobiliário junto às instituições financeiras.",
     ["Orientação sobre as etapas do financiamento", "Acompanhamento do trâmite com a instituição financeira", "Apoio na organização do processo para reduzir a burocracia"],
     "Entender o processo de financiamento", "A aprovação do crédito, as condições e os prazos são definidos pela instituição financeira."),
    ("imoveis", "Compra e venda de imóveis",
     f"Intermediação imobiliária ({CRECI}) para quem quer comprar bem ou precisa vender o seu imóvel.",
     ["Intermediação na compra e na venda", "Pesquisa e apresentação de terrenos e imóveis", "Apoio na parte burocrática da negociação"],
     "Conversar sobre um imóvel", None),
]
STEPS = [
    ("Conversa inicial", "Entendemos o que você precisa resolver e o orçamento disponível. Sem compromisso.", "Todos os serviços"),
    ("Terreno ou imóvel", "Se você ainda não tem, pesquisamos e apresentamos opções de terrenos e imóveis.", "Compra e venda"),
    ("Projeto", "Projeto arquitetônico e de engenharia, da planta à escolha de cores e pisos, já pensando em ampliações futuras.", "Projetos"),
    ("Financiamento", "Orientamos e acompanhamos o trâmite junto à instituição financeira.", "Financiamento"),
    ("Obra", "Execução ou gerenciamento, com reuniões frequentes e acompanhamento das compras dentro do orçamento.", "Execução e gerenciamento"),
    ("Entrega e pós-obra", "Depois das chaves, a equipe segue disponível para tirar dúvidas.", "Execução e gerenciamento"),
]
TESTIMONIALS = [
    ("Adriano Rengel", "Projeto e construção da casa", None,
     "Desde o início, a Macchio esteve ao nosso lado em cada detalhe: do projeto arquitetônico à escolha de cores e pisos, inclusive, planejando o futuro e expansão da casa. […] As reuniões constantes nos ajudaram a entender cada etapa do processo, trazendo transparência e segurança.",
     ["Construir nossa casa sempre foi um grande sonho, mas, como muitos dizem, o processo pode ser desafiador e cheio de incertezas. No entanto, com a Macchio e a empreiteira MA3, tudo correu de maneira surpreendentemente tranquila e organizada. Desde o início, a Macchio esteve ao nosso lado em cada detalhe: do projeto arquitetônico à escolha de cores e pisos, inclusive, planejando o futuro e expansão da casa. Eles nos acompanharam até mesmo nas compras, garantindo que tudo se encaixasse perfeitamente dentro do orçamento planejado. Como éramos muito leigos no processo, as reuniões constantes nos ajudaram a entender cada etapa do processo, trazendo transparência e segurança.",
      "Claro, tivemos momentos de ansiedade e dúvidas, mas a equipe sempre esteve pronta para nos orientar e hoje estamos imensamente felizes com nossa casa pronta.",
      "Além disso, mesmo após a entrega, o suporte da equipe continua excelente. Sempre que surge alguma dúvida ou necessidade, eles estão disponíveis para ajudar. Essa qualidade no atendimento faz toda a diferença!",
      "Sem dúvida, recomendamos a Macchio e a MA3 para quem busca um trabalho sério, transparente e de alta qualidade. E se um dia decidirmos construir novamente, já sabemos a quem recorrer. Muito obrigado por tornarem nosso sonho realidade!"]),
    ("Susana Carvalho Eyng", "Venda, projeto e construção", "susana",
     "Para executar esse longo processo que costuma ser bastante complicado e cansativo, escolhi e confiei no trabalho do corretor Djonas, da Macchio, que se mostrou sempre muito atencioso e prestativo, sem medir esforços para rapidamente vender minha antiga casa e projetar e construir com excelência minha atual morada.", None),
    ("Neiva Fátima Sacon", "Venda e compra de imóvel", "neiva",
     "A venda da casa e compra do apartamento foi rápida e dentro do prazo previsto. Destaco a agilidade, preocupação e responsabilidade com toda parte burocrática. Minha expectativa e planejamento foram atendidos.", None),
]
FAQ = [
    ("A Macchio é imobiliária ou construtora?",
     f"As duas. Somos imobiliária ({CRECI}) e empresa de engenharia ({CREA}): elaboramos projetos, executamos ou gerenciamos obras, orientamos o financiamento e intermediamos a compra e venda de imóveis. Você pode contratar um serviço isolado ou o processo completo."),
    ("As imagens do portfólio são fotos de obras prontas?",
     "Não. As imagens do portfólio são perspectivas 3D (renderizações) dos projetos desenvolvidos pela Macchio. Quando a execução também é prevista pela Macchio, isso está indicado na página do projeto."),
    ("Vocês ajudam a conseguir o financiamento imobiliário?",
     "Orientamos e acompanhamos o processo de financiamento junto às instituições financeiras, para que ele seja mais ágil e menos burocrático. A aprovação do crédito e as condições são definidas pela instituição financeira."),
    ("Qual a diferença entre execução e gerenciamento de obra?",
     "Na execução, a obra é construída com mão de obra qualificada e material de primeira linha, com acompanhamento de todas as etapas. No gerenciamento, você deixa tudo por nossa conta e não precisa se preocupar com o dia a dia da obra."),
    ("Vocês fazem regularização de obras?",
     "Sim. Elaboramos os projetos necessários para regularizar obras residenciais e comerciais, seguindo as normas e os requisitos exigidos."),
    ("Onde fica o escritório da Macchio?",
     f"Na Rua XV de Novembro, 336, sala 01, Centro, Rio do Sul/SC, CEP {CEP}. Também atendemos pelo WhatsApp {PHONE} e pelo e-mail {EMAIL}."),
]
ORG = {
    "@type": ["GeneralContractor", "RealEstateAgent"],
    "@id": ORG_ID,
    "name": "Macchio Engenharia e Negócios Imobiliários",
    "alternateName": "Macchio Engenharia",
    "legalName": "Macchio Engenharia e Negócios Imobiliários Ltda",
    "taxID": CNPJ,
    "url": SITE,
    "logo": SITE + "assets/img/logo-macchio.png",
    "image": SITE + "assets/img/og-macchio.jpg",
    "description": "Engenharia e imobiliária em Rio do Sul/SC: projetos de engenharia e interiores, regularização, execução e gerenciamento de obras, orientação em financiamento imobiliário e compra e venda de imóveis.",
    "telephone": "+55 47 99172-3557",
    "email": EMAIL,
    "address": {"@type": "PostalAddress", "streetAddress": "Rua XV de Novembro, 336, sala 01", "addressLocality": "Rio do Sul",
                "addressRegion": "SC", "postalCode": CEP, "addressCountry": "BR"},
    "areaServed": {"@type": "City", "name": "Rio do Sul"},
    "founder": {"@type": "Person", "name": "Djonas Roberto Matias", "jobTitle": "Engenheiro civil e corretor de imóveis"},
    "sameAs": [INSTAGRAM, FACEBOOK],
    "knowsAbout": ["Projetos de engenharia civil", "Design de interiores", "Regularização de obras", "Execução de obras",
                   "Gerenciamento de obras", "Financiamento imobiliário", "Compra e venda de imóveis"],
}
ORG_REF = {"@id": ORG_ID}


def breadcrumb(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items, 1)]}


def graph(*nodes):
    return {"@context": "https://schema.org", "@graph": list(nodes)}


def testimonials_html(prefix):
    out = []
    for name, tag, photo, quote_, full in TESTIMONIALS:
        avatar = (f'<img src="{prefix}assets/img/depoimentos/{photo}.webp" width="48" height="48" loading="lazy" decoding="async" alt="">' if photo
                  else f'<span class="ini" aria-hidden="true">{"".join(w[0] for w in name.split()[:2])}</span>')
        more = ""
        if full:
            more = '<details class="tst-more"><summary>Ler depoimento completo</summary><div>' + "".join(f"<p>{x}</p>" for x in full) + "</div></details>"
        out.append(f"""          <figure class="tst">
            <span class="tst-tag mono">{tag}</span>
            <blockquote><p>“{quote_}”</p></blockquote>
            {more}
            <figcaption>{avatar}<strong>{name}</strong></figcaption>
          </figure>""")
    return "\n".join(out)


# ---------- / ----------
HERO = ("residencia-a-e-d", "01")
FEATURED = ["residencia-f-e-m", "residencia-p-e-r", "residencia-l-e-g", "residencia-l-e-d", "multifamiliar-03", "interiores-j-e-j"]


def build_home():
    pre = ""
    hp = BY_SLUG[HERO[0]]
    _, hero_srcset, _ = img_src(*HERO, pre)
    hero_img = img_tag(*HERO, pre, cover_alt(hp), "100vw", eager=True)
    preload = f'  <link rel="preload" as="image" imagesrcset="{hero_srcset}" imagesizes="100vw" fetchpriority="high">\n'
    intents = "".join(f'<li><a href="servicos/#servico-{k}">{t}</a></li>' for k, t in
                      [("projetos", "Projetos e interiores"), ("obras", "Obras"), ("financiamento", "Financiamento"), ("imoveis", "Compra e venda")])
    cards = "\n".join(project_card(BY_SLUG[s], pre, CARD_SIZES) for s in FEATURED)
    svc = "\n".join(f"""          <li class="svc-mini">
            <a href="servicos/#servico-{k}">
              <span class="mono">{two(i)}</span>
              <h3>{title}</h3>
              <p>{text}</p>
              <span class="svc-mini-more">Ver o que inclui {ic("i-arrow")}</span>
            </a>
          </li>""" for i, (k, title, text, *_rest) in enumerate(SERVICES, 1))
    body = f"""
  <main id="conteudo">
    <section class="hero" data-hero aria-labelledby="hero-title">
      <figure class="hero-media">{hero_img}<figcaption class="mono"><a href="{purl(hp)}">{e(hp["name"])} · perspectiva 3D</a></figcaption></figure>
      <div class="wrap hero-content">
        <h1 class="hero-title" id="hero-title"><span class="label">Engenharia e imobiliária · Rio do Sul/SC</span><span class="hero-h">Do terreno à chave,</span> <span class="hero-h hero-h--soft">com uma equipe em cada etapa.</span></h1>
        <p class="hero-sub">Projetos de engenharia e interiores, execução e gerenciamento de obras, financiamento e compra e venda de imóveis. Conte com a Macchio para o processo completo ou para a etapa em que você precisa de apoio.</p>
        <div class="hero-ctas">
          {pill("Planejar minha construção", "servicos/", "pill--light", "hero_planejar")}
          <a class="link-u" href="portfolio/" data-track="hero_portfolio">Explorar projetos {ic("i-arrow")}</a>
        </div>
        <nav class="hero-intents" aria-label="Encontre o serviço">
          <span class="mono">Encontre o serviço</span>
          <ul>{intents}</ul>
        </nav>
      </div>
    </section>

    <section class="wrap intro" aria-labelledby="intro-title">
      <span class="label">Nós somos a Macchio</span>
      <h2 class="vh" id="intro-title">Nós somos a Macchio</h2>
      <p class="intro-text">Não somos só imobiliária nem só construtora. A Macchio reúne <strong>engenharia e negócios imobiliários</strong> para acompanhar o processo completo ou apenas a etapa em que você precisa de apoio.</p>
      <a class="link-u intro-link" href="sobre/">Saiba sobre nós {ic("i-arrow")}</a>
      <dl class="facts">
        <div><dt class="label">Engenharia</dt><dd>{CREA}</dd></div>
        <div><dt class="label">Imobiliária</dt><dd>{CRECI}</dd></div>
        <div><dt class="label">Portfólio</dt><dd>{len(PROJECTS)} projetos publicados</dd></div>
        <div><dt class="label">Escritório</dt><dd>Centro, Rio do Sul/SC</dd></div>
      </dl>
    </section>

    <section class="sec dark" aria-labelledby="work-title">
      <div class="wrap">
        <div class="sec-head">
          <span class="label">Portfólio</span>
          <h2 class="h2" id="work-title">Projetos desenvolvidos</h2>
          <div class="sec-aside">
            <p class="muted">Residências, sobrados geminados, interiores e ampliações projetados pela Macchio. As imagens são perspectivas 3D (renderizações) dos projetos, não fotos de obras concluídas.</p>
          </div>
        </div>
        <ul class="cards">
{cards}
        </ul>
        <div class="sec-foot">{pill(f"Ver o portfólio completo ({len(PROJECTS)} projetos)", "portfolio/", "pill--light", "home_portfolio")}</div>
      </div>
    </section>

    <section class="wrap sec" aria-labelledby="svc-title">
      <div class="sec-head">
        <span class="label">Serviços</span>
        <h2 class="h2" id="svc-title">O que a Macchio faz por você</h2>
        <div class="sec-aside"><p class="muted">Quatro frentes de atuação. Contrate só a que você precisa ou combine várias com a mesma equipe.</p></div>
      </div>
      <ul class="svc-minis">
{svc}
      </ul>
      <div class="sec-foot sec-foot--start">{pill("Ver todos os serviços", "servicos/", "", "home_servicos")}</div>
    </section>

    <section class="wrap sec sec--tight" aria-labelledby="tst-title">
      <div class="sec-head">
        <span class="label">Depoimentos</span>
        <h2 class="h2" id="tst-title">Quem já trabalhou com a Macchio</h2>
      </div>
      <div class="tst-grid">
{testimonials_html(pre)}
      </div>
    </section>
{cta_band(pre)}
  </main>"""
    jsonld = graph(
        {**ORG, "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Serviços Macchio", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1], "description": s[2], "url": f"{SITE}servicos/#servico-{s[0]}"}} for s in SERVICES]}},
        {"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": "Macchio Engenharia e Negócios Imobiliários", "inLanguage": "pt-BR", "publisher": ORG_REF},
    )
    write_page("", pre, "Macchio Engenharia | Projetos, obras e imóveis em Rio do Sul/SC",
               "Engenharia e imobiliária em Rio do Sul/SC: projetos de engenharia e interiores, execução e gerenciamento de obras, financiamento e compra e venda de imóveis.",
               "assets/img/og-macchio.jpg", jsonld, body, current="inicio", solid=False, preload=preload)


# ---------- /sobre/ ----------
def build_sobre():
    pre = "../"
    about_img = img_tag("residencia-l-e-d", "06", pre, "Perspectiva 3D da área gourmet integrada à cozinha, projeto Residência L e D", "(min-width: 1024px) 40vw, 100vw")
    body = f"""
  <main id="conteudo">{pagehead(pre, "Sobre a empresa", "Nós somos a Macchio", "Nascemos da vontade de fazer diferente e tornar leve e compreensível um processo conhecido pela dificuldade e pela burocracia.", [("Sobre a empresa", None)])}

    <section class="wrap sec" aria-labelledby="story-title">
      <div class="about-grid about-grid--light">
        <figure class="about-media">{about_img}<figcaption class="mono">Residência L e D · perspectiva 3D</figcaption></figure>
        <div class="about-copy">
          <span class="label">Nossa história</span>
          <h2 class="h2" id="story-title">Engenheiro e corretor na mesma mesa.</h2>
          <p class="lead">Fundada por Djonas Roberto Matias, corretor de imóveis e engenheiro civil formado em 2017, com experiência em venda de imóveis, projetos, gerenciamento e execução de obras e financiamentos imobiliários.</p>
          <p>Atendemos as quatro frentes (venda de imóveis, financiamento, projetos e execução de obras) porque acreditamos na facilidade e no diferencial de iniciar e finalizar o processo com a mesma equipe, gerando ainda mais confiança e credibilidade.</p>
          <p>Prezamos por inovação no processo, qualidade nos materiais e na mão de obra, e acreditamos que somente conhecendo a fundo a necessidade de cada cliente conseguimos atender o que ele espera.</p>
          <p>{pill("Conheça os serviços", "../servicos/", "", "sobre_servicos")}</p>
        </div>
      </div>
    </section>

    <section class="sec proc" aria-labelledby="mvv-title">
      <div class="wrap">
        <div class="sec-head"><span class="label">Missão, visão e valores</span><h2 class="h2" id="mvv-title">No que acreditamos</h2></div>
        <ul class="mvv">
          <li><span class="mono">Missão</span><p>Auxiliar nossos clientes e simplificar todos os processos da construção do seu sonho. Comprando com prudência, projetando com conhecimento e construindo com segurança.</p></li>
          <li><span class="mono">Visão</span><p>Ser referência de qualidade no mercado em todos os serviços prestados, prezando pelo ótimo relacionamento com nossos clientes, criando um legado de respeito e compromisso.</p></li>
          <li><span class="mono">Valores</span><p>Inovação no processo, ética, respeito e comprometimento.</p></li>
        </ul>
      </div>
    </section>

    <section class="wrap sec" aria-labelledby="data-title">
      <div class="faq-grid">
        <div class="faq-head"><span class="label">Dados da empresa</span><h2 class="h2" id="data-title">Registros e endereço</h2></div>
        <dl class="datalist">
          <div><dt class="mono">Razão social</dt><dd>Macchio Engenharia e Negócios Imobiliários Ltda</dd></div>
          <div><dt class="mono">CNPJ</dt><dd>{CNPJ}</dd></div>
          <div><dt class="mono">Registro de engenharia</dt><dd>{CREA}</dd></div>
          <div><dt class="mono">Registro imobiliário</dt><dd>{CRECI}</dd></div>
          <div><dt class="mono">Fundador</dt><dd>Djonas Roberto Matias, engenheiro civil e corretor de imóveis</dd></div>
          <div><dt class="mono">Escritório</dt><dd><a class="inline-link" href="{MAPS}" target="_blank" rel="noopener">{ADDRESS}, {CEP}</a></dd></div>
        </dl>
      </div>
    </section>
{cta_band(pre)}
  </main>"""
    jsonld = graph(
        {"@type": "AboutPage", "@id": SITE + "sobre/", "url": SITE + "sobre/", "name": "Sobre a Macchio", "about": ORG_REF, "isPartOf": {"@id": SITE + "#site"}},
        ORG,
        breadcrumb([("Início", ""), ("Sobre a empresa", "sobre/")]),
    )
    write_page("sobre/", pre, "Sobre a Macchio | Engenharia e imobiliária em Rio do Sul/SC",
               "Conheça a Macchio Engenharia e Negócios Imobiliários: fundada pelo engenheiro civil e corretor Djonas Roberto Matias, atua em projetos, obras, financiamento e imóveis em Rio do Sul/SC.",
               "assets/img/og-macchio.jpg", jsonld, body, current="sobre")


# ---------- /servicos/ ----------
def build_servicos():
    pre = "../"
    svc = []
    for k, title, text, items, cta, note in SERVICES:
        lis = "".join(f"<li>{ic('i-check')}<span>{x}</span></li>" for x in items)
        note_html = f'<p class="svc-note">{note}</p>' if note else ""
        svc.append(f"""          <article class="svc-card" id="servico-{k}" aria-labelledby="svc-{k}">
            <h2 class="svc-title" id="svc-{k}">{title}</h2>
            <p class="svc-desc">{text}</p>
            <h3 class="label">O que inclui</h3>
            <ul class="svc-list">{lis}</ul>
            {note_html}
            <div class="svc-cta">{wa_link(cta, MSG[k], f"whatsapp_servico_{k}", "btn-line")}<a class="svc-form" href="../contato/?interesse={k}">ou envie pelo formulário</a></div>
          </article>""")
    steps = "\n".join(f'          <li class="step"><span class="step-n mono">{two(i)}</span><h3>{t}</h3><p>{d}</p><span class="step-tag mono">{tag}</span></li>'
                      for i, (t, d, tag) in enumerate(STEPS, 1))
    faq = "\n".join(f"""          <details class="faq-item"{" open" if i == 0 else ""}>
            <summary>{q}<span class="plus" aria-hidden="true"></span></summary>
            <div class="faq-a"><p>{a}</p></div>
          </details>""" for i, (q, a) in enumerate(FAQ))
    body = f"""
  <main id="conteudo">{pagehead(pre, "Serviços", "Nossos serviços", "Não somos apenas uma imobiliária ou só uma construtora: somos a junção de ambas. Contrate uma frente isolada ou o processo completo, com a mesma equipe.", [("Serviços", None)])}

    <section class="wrap sec" aria-label="Serviços">
      <div class="svc-grid">
{chr(10).join(svc)}
      </div>
    </section>

    <section class="sec proc" id="como-funciona" aria-labelledby="proc-title">
      <div class="wrap">
        <div class="sec-head">
          <span class="label">Como funciona</span>
          <h2 class="h2" id="proc-title">Etapas do atendimento</h2>
          <div class="sec-aside"><p class="muted">As etapas variam conforme o serviço contratado. Cada uma indica a frente a que se refere: você pode seguir o caminho completo ou começar por qualquer uma.</p></div>
        </div>
        <ol class="steps">
{steps}
        </ol>
      </div>
    </section>

    <section class="wrap sec" id="perguntas" aria-labelledby="faq-title">
      <div class="faq-grid">
        <div class="faq-head">
          <span class="label">Perguntas frequentes</span>
          <h2 class="h2" id="faq-title">Dúvidas comuns</h2>
          <p>Não encontrou sua dúvida? {wa_link("Pergunte no WhatsApp", "Olá! Tenho uma dúvida sobre os serviços da Macchio.", "whatsapp_faq", "inline-link")}.</p>
        </div>
        <div class="faq-list">
{faq}
        </div>
      </div>
    </section>
{cta_band(pre)}
  </main>"""
    jsonld = graph(
        {"@type": "WebPage", "@id": SITE + "servicos/", "url": SITE + "servicos/", "name": "Serviços | Macchio Engenharia", "isPartOf": {"@id": SITE + "#site"}, "about": ORG_REF},
        *[{"@type": "Service", "@id": f"{SITE}servicos/#servico-{s[0]}", "name": s[1], "description": s[2], "provider": ORG_REF, "areaServed": {"@type": "City", "name": "Rio do Sul"}} for s in SERVICES],
        {"@type": "FAQPage", "@id": SITE + "servicos/#perguntas", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        breadcrumb([("Início", ""), ("Serviços", "servicos/")]),
    )
    write_page("servicos/", pre, "Serviços | Projetos, obras, financiamento e imóveis em Rio do Sul/SC | Macchio",
               "Projetos de engenharia e interiores, execução e gerenciamento de obras, orientação em financiamento imobiliário e compra e venda de imóveis em Rio do Sul/SC.",
               "assets/img/og-macchio.jpg", jsonld, body, current="servicos")


# ---------- /portfolio/ ----------
def build_portfolio():
    pre = "../"
    counts = {c: (len(PROJECTS) if c == "all" else sum(p["cat"] == c for p in PROJECTS)) for c, _ in CATS}
    filters = "".join(f'<button type="button" data-filter="{c}" aria-pressed="{"true" if c == "all" else "false"}">{t}<sup>{counts[c]}</sup></button>' for c, t in CATS)
    cards = "\n".join(project_card(p, pre, CARD_SIZES, heading="h2", eager=(i < 3)) for i, p in enumerate(PROJECTS))
    rows = []
    for i, p in enumerate(PROJECTS):
        src, _, _ = img_src(p["slug"], p["renders"][0]["file"], pre)
        rows.append(f"""        <li class="prow" data-cat="{p["cat"]}" data-preview="{src}">
          <a href="{pre}{purl(p)}"><span class="mono">{two(i + 1)}</span><span class="prow-t"><strong>{e(p["title"])}</strong><span class="mono">{e(p["name"])}</span></span><span class="mono c-type">{e(p["type"])}</span><span class="mono c-city">{e(city_uf(p) or "")}</span><span class="mono c-area">{e(p["area"] or "—")}</span></a>
        </li>""")
    body = f"""
  <main id="conteudo" class="dark pidx" data-pidx>
    <div class="wrap pidx-head">
      {crumbs(pre, [("Portfólio", None)])}
      <span class="label">Portfólio</span>
      <h1 class="h1">Portfólio<sup>{len(PROJECTS)}</sup></h1>
      <p>A Macchio elabora projetos técnicos residenciais, comerciais e industriais, conforme as normas e os requisitos exigidos. Aqui estão residências, sobrados geminados, interiores e ampliações projetados em Rio do Sul e Aurora/SC. As imagens são perspectivas 3D (renderizações) dos projetos.</p>
    </div>
    <div class="pidx-bar">
      <div class="wrap pidx-bar-in">
        <div class="filters" role="group" aria-label="Filtrar projetos por tipo">{filters}</div>
        <div class="views" role="group" aria-label="Visualização"><button type="button" data-view="grid" aria-pressed="true">Grade</button><button type="button" data-view="list" aria-pressed="false">Lista</button></div>
      </div>
    </div>
    <div class="wrap">
      <p class="vh" aria-live="polite" data-filter-status></p>
      <ul class="cards cards--index" data-pgrid>
{cards}
      </ul>
      <ul class="plist" data-plist hidden>
{chr(10).join(rows)}
      </ul>
    </div>
  </main>"""
    jsonld = graph(
        {"@type": "CollectionPage", "@id": SITE + "portfolio/", "url": SITE + "portfolio/", "name": "Portfólio | Macchio Engenharia",
         "isPartOf": {"@id": SITE + "#site"}, "about": ORG_REF,
         "hasPart": [{"@type": "CreativeWork", "name": full_title(p), "alternateName": p["name"], "url": SITE + purl(p)} for p in PROJECTS]},
        breadcrumb([("Início", ""), ("Portfólio", "portfolio/")]),
    )
    write_page("portfolio/", pre, "Portfólio | Projetos de casas, sobrados e interiores em Rio do Sul/SC | Macchio",
               f"Portfólio Macchio: {len(PROJECTS)} projetos de residências, sobrados geminados, interiores e ampliações em Rio do Sul e Aurora/SC, com perspectivas 3D, área e programa de cada projeto.",
               "assets/img/og-macchio.jpg", jsonld, body, current="portfolio")


# ---------- /portfolio/<slug>/ ----------
def related(p, n=3):
    same = [x for x in PROJECTS if x["cat"] == p["cat"] and x["slug"] != p["slug"]]
    others = [x for x in PROJECTS if x["cat"] != p["cat"]]
    i = PROJECTS.index(p)
    same = same[i % len(same):] + same[:i % len(same)] if same else []
    return (same + others)[:n]


def build_project(p):
    pre = "../../"
    slug = p["slug"]
    total = len(p["renders"])
    cover = p["renders"][0]
    _, _, cover_full = img_src(slug, cover["file"], pre)
    gal = []
    rest = p["renders"][1:]
    for j, r in enumerate(rest, 2):
        src, srcset, full = img_src(slug, r["file"], pre)
        wide = " is-wide" if (len(rest) % 2 == 1 and j == 2) else ""
        gal.append(f'        <li><button class="gal-item{wide}" type="button" data-lb-item data-full="{full}" aria-label="Ampliar perspectiva 3D {j} de {total}"><img src="{src}" srcset="{srcset}" sizes="(min-width: 900px) {"96vw" if wide else "48vw"}, 100vw" width="{r["w"]}" height="{r["h"]}" loading="lazy" decoding="async" alt="{e(p["name"])}: perspectiva 3D {j} de {total}"></button></li>')
    plans = []
    for j, r in enumerate(p["plans"], 1):
        src, srcset, full = img_src(slug, r["file"], pre)
        plans.append(f'        <li><button class="gal-item is-plan" type="button" data-lb-item data-full="{full}" aria-label="Ampliar planta humanizada {j}"><img src="{src}" srcset="{srcset}" sizes="(min-width: 900px) 48vw, 100vw" width="{r["w"]}" height="{r["h"]}" loading="lazy" decoding="async" alt="{e(p["name"])}: planta humanizada {j}"></button></li>')
    n_pl = len(p["plans"])
    dl = [("Tipo", p["type"]), ("Cidade", city_uf(p)), ("Área total", p["area"]), ("Escopo da Macchio", p["scope"]), ("Execução", p["exec"]),
          ("Imagens", f"{total} perspectivas 3D" + (f" e {n_pl} planta{'s' if n_pl > 1 else ''} humanizada{'s' if n_pl > 1 else ''}" if n_pl else ""))]
    dl_html = "".join(f'<div><dt class="mono">{k}</dt><dd>{e(v)}</dd></div>' for k, v in dl if v)
    desc = p["desc"]
    paras = "".join(f"<p>{e(x)}</p>" for x in desc)
    _, srcset0, _ = img_src(slug, cover["file"], pre)
    preload = f'  <link rel="preload" as="image" imagesrcset="{srcset0}" imagesizes="100vw" fetchpriority="high">\n'
    msg = f"Olá! Vi o projeto {p['name']} ({p['title']}) no site da Macchio e gostaria de solicitar um projeto semelhante."
    rel = "\n".join(project_card(x, pre, CARD_SIZES) for x in related(p))
    gal_html = (f'\n      <h2 class="label gal-h">Galeria · perspectivas 3D</h2>\n      <ul class="gal">\n{chr(10).join(gal)}\n      </ul>' if gal else "")
    plans_html = (f'\n      <h2 class="label gal-h">Plantas humanizadas</h2>\n      <ul class="gal gal--plans">\n{chr(10).join(plans)}\n      </ul>' if plans else "")
    body = f"""
  <main id="conteudo">
    <section class="phead dark" aria-labelledby="p-title">
      <div class="wrap">
        {crumbs(pre, [("Portfólio", "../"), (p["name"], None)])}
        <p class="label">{e(p["name"])} · {e(p["type"])}</p>
        <h1 class="h1" id="p-title">{e(full_title(p))}</h1>
        <dl class="phead-meta">{dl_html}</dl>
      </div>
      <figure class="wrap phero">
        <button class="phero-btn" type="button" data-lb-item data-full="{cover_full}" aria-label="Ampliar perspectiva 3D 1 de {total}">{cover_tag(p, pre, "100vw", eager=True)}</button>
        <figcaption class="mono">Perspectiva 3D · imagem 1 de {total}. As imagens deste projeto são renderizações, não fotos da obra.</figcaption>
      </figure>
    </section>
    <section class="wrap pinfo" aria-labelledby="p-about">
      <h2 class="label" id="p-about">Descrição do projeto</h2>
      <div class="pinfo-text">{paras}</div>
    </section>
    <section class="wrap pgal" aria-label="Imagens do projeto">{gal_html}{plans_html}
    </section>
    <section class="wrap pcta" aria-labelledby="pcta-title">
      <h2 class="h2" id="pcta-title">Quer um projeto semelhante?</h2>
      <div class="pcta-actions">
        {pill("Solicitar um projeto semelhante", wa(msg), "", "whatsapp_projeto_semelhante", whatsapp=True)}
        <a class="link-u" href="../">Ver todo o portfólio {ic("i-arrow")}</a>
      </div>
    </section>
    <section class="sec dark related" aria-labelledby="rel-title">
      <div class="wrap">
        <div class="sec-head sec-head--row"><h2 class="h2" id="rel-title">Projetos relacionados</h2><a class="link-u" href="../">Ver todo o portfólio {ic("i-arrow")}</a></div>
        <ul class="cards">
{rel}
        </ul>
      </div>
    </section>
  </main>
  <dialog class="lb" data-lb aria-label="Imagem ampliada">
    <div class="lb-top"><span class="mono">{e(p["name"])} · perspectiva 3D</span><button class="circ" type="button" data-lb-close aria-label="Fechar">{ic("i-close")}</button></div>
    <figure class="lb-fig"><img alt=""></figure>
    <div class="lb-bot"><span class="mono" data-lb-count aria-live="polite"></span><div class="lb-nav"><button class="circ" type="button" data-lb-prev aria-label="Imagem anterior">{ic("i-prev")}</button><button class="circ" type="button" data-lb-next aria-label="Próxima imagem">{ic("i-arrow")}</button></div></div>
  </dialog>"""
    url = purl(p)
    jsonld = graph(
        {"@type": "CreativeWork", "@id": SITE + url, "url": SITE + url, "name": full_title(p), "alternateName": p["name"], "genre": p["type"],
         "description": " ".join(desc), "image": [SITE + img_src(slug, cover["file"], "")[2]], "inLanguage": "pt-BR", "creator": ORG_REF,
         **({"locationCreated": {"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": p["city"], "addressRegion": "SC", "addressCountry": "BR"}}} if p["city"] else {})},
        breadcrumb([("Início", ""), ("Portfólio", "portfolio/"), (p["name"], url)]),
    )
    meta_desc = (f"{full_title(p)}/SC" + (f", {p['area']}" if p["area"] else "") + f". {p['type']} projetada pela Macchio Engenharia ({p['name']}), com {total} perspectivas 3D"
                 + (" e plantas humanizadas" if p["plans"] else "") + ".")
    make_og(slug, cover["file"])
    write_page(url, pre, f"{full_title(p)}/SC · {p['name']} | Macchio Engenharia", meta_desc,
               f"assets/img/projetos/{slug}/og.jpg", jsonld, body, current="portfolio", preload=preload)


# ---------- /contato/ ----------
def build_contato():
    pre = "../"
    options = "".join(f'<option value="{k}" data-msg="{e(m)}">{t}</option>' for k, t, m in INTERESTS)
    bg = img_tag("residencia-n-e-a", "06", pre, "", "100vw")
    body = f"""
  <main id="conteudo">
    <section class="cta dark cta--page" aria-labelledby="page-title">
      <div class="cta-bg" aria-hidden="true">{bg}</div>
      <div class="wrap cta-in">
        {crumbs(pre, [("Contato", None)])}
        <span class="label">Contato</span>
        <h1 class="h1" id="page-title">O que você precisa resolver?</h1>
        <p class="cta-lead">Ficou com dúvida ou quer saber como podemos te ajudar? Escolha a área de interesse e, se quiser, descreva sua necessidade. Ao enviar, o WhatsApp abre com a mensagem pronta: você revisa e envia para a nossa equipe.</p>
        <div class="cta-grid">
          <form class="cta-form" data-lead-form novalidate>
            <div class="field"><label class="mono" for="f-int">Área de interesse</label>
              <select id="f-int" name="interesse" required><option value="">Selecione</option>{options}</select>
            </div>
            <div class="field"><label class="mono" for="f-nome">Seu nome</label><input id="f-nome" name="nome" type="text" autocomplete="name" required></div>
            <div class="field"><label class="mono" for="f-msg">Sua necessidade (opcional)</label><textarea id="f-msg" name="mensagem" rows="3"></textarea></div>
            <p class="form-err" data-form-err role="alert"></p>
            <div><button class="pill pill--light" type="submit">Continuar no WhatsApp<span class="pill-ic" aria-hidden="true">{ic("i-wa")}{ic("i-wa")}</span></button></div>
            <p class="form-ok" data-form-ok role="status" hidden>Abrimos o WhatsApp com a sua mensagem em uma nova aba. Se ele não abriu, <a data-form-link href="#" target="_blank" rel="noopener">clique aqui</a>.</p>
          </form>
          <ul class="cta-info">
            <li><a href="{wa(MSG["outro"])}" target="_blank" rel="noopener" data-track="whatsapp_contato"><span class="mono">WhatsApp</span><span>{PHONE}</span>{ic("i-wa")}</a></li>
            <li><a href="{PHONE_HREF}" data-track="telefone_contato"><span class="mono">Telefone</span><span>{PHONE}</span>{ic("i-arrow")}</a></li>
            <li><a href="mailto:{EMAIL}" data-track="email_contato"><span class="mono">E-mail</span><span>{EMAIL}</span>{ic("i-arrow")}</a></li>
            <li><a href="{MAPS}" target="_blank" rel="noopener" data-track="mapa_contato"><span class="mono">Escritório · ver no mapa</span><span>{ADDRESS}, {CEP}</span>{ic("i-arrow")}</a></li>
          </ul>
        </div>
      </div>
    </section>
  </main>"""
    jsonld = graph(
        {"@type": "ContactPage", "@id": SITE + "contato/", "url": SITE + "contato/", "name": "Contato | Macchio Engenharia", "isPartOf": {"@id": SITE + "#site"}, "about": ORG_REF},
        ORG,
        breadcrumb([("Início", ""), ("Contato", "contato/")]),
    )
    write_page("contato/", pre, "Contato e orçamento | Macchio Engenharia em Rio do Sul/SC",
               f"Fale com a Macchio sobre projeto, obra, financiamento ou compra e venda de imóvel. WhatsApp {PHONE}, {EMAIL}. Escritório no Centro de Rio do Sul/SC.",
               "assets/img/og-macchio.jpg", jsonld, body, current="contato")


def make_og(slug, file):
    folder = ROOT / "assets/img/projetos" / slug
    target = folder / "og.jpg"
    if target.exists():
        return
    src = next(folder / f"{file}-{w}.webp" for w in (1600, 1280, 800) if (folder / f"{file}-{w}.webp").exists())
    im = Image.open(src).convert("RGB")
    ImageOps.fit(im, (1200, 630), Image.LANCZOS).save(target, "JPEG", quality=80, optimize=True, progressive=True)


def build_sitemap():
    urls = [SITE] + [SITE + u for u in ("sobre/", "servicos/", "portfolio/")] + [SITE + purl(p) for p in PROJECTS] + [SITE + "contato/"]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")


if __name__ == "__main__":
    # páginas de uma estrutura anterior (/projetos/) não fazem parte do site atual
    if (ROOT / "projetos").exists():
        shutil.rmtree(ROOT / "projetos")
    build_home()
    build_sobre()
    build_servicos()
    build_portfolio()
    for p in PROJECTS:
        build_project(p)
    build_contato()
    build_sitemap()
    print(f"ok: 5 páginas + {len(PROJECTS)} projetos em /portfolio/")
