#!/usr/bin/env python3
"""Builds the static site from src/pages/*.html into the repository root.

Each page in src/pages is an HTML fragment that starts with a meta block:

    <!--meta
    title: About
    description: One sentence for search results.
    nav: about
    -->

Inside a page you can use:
    {{icon:heart}}   inline SVG from tools/icons/heart.svg
    {{url:donate}}   link to another page (handles folders and the preview build)
    {{root}}         relative path to the site root, for assets

Run:  python3 tools/build.py            -> writes the live site (pretty URLs: /about/)
      python3 tools/build.py --preview DIR -> writes a copy with explicit index.html links
"""
import os, re, sys, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src', 'pages')
ICONS = os.path.join(ROOT, 'tools', 'icons')
SITE = 'https://www.healsocialfoundation.com'

# slug -> output folder ('' is the home page). Slugs match the old Google Sites URLs so existing links keep working.
PAGES = ['index', 'about', 'our-work', 'research-cphi', 'joinpartner', 'internship', 'eleven-labs', 'contact-us', 'donate', 'privacy', '404']
NAV = [('index', 'Home'), ('about', 'About'), ('our-work', 'Our work'),
       ('research-cphi', 'Research'), ('joinpartner', 'Get involved'), ('contact-us', 'Contact')]

LOGO = ('<svg viewBox="0 0 200 200" aria-hidden="true"><path d="M100,185 C45,180 8,140 10,92 C68,88 106,126 100,185Z" fill="#d9535f" opacity=".9"/>'
        '<path d="M100,185 C42,152 32,78 60,24 C118,52 136,122 100,185Z" fill="#3cb794" opacity=".8"/>'
        '<path d="M100,185 C162,152 178,72 146,20 C88,46 68,122 100,185Z" fill="#1b8fbd" opacity=".92"/></svg>')


def icon(name):
    with open(os.path.join(ICONS, name + '.svg')) as f:
        svg = f.read().strip()
    return svg.replace('<svg ', '<svg aria-hidden="true" focusable="false" ', 1)


def out_path(slug):
    if slug == 'index':
        return 'index.html'
    if slug == '404':
        return '404.html'
    return os.path.join(slug, 'index.html')


def depth(slug):
    return 0 if slug in ('index', '404') else 1


def make_url(frm, to, preview):
    prefix = '../' * depth(frm)
    if to == 'index':
        target = 'index.html' if preview else ''
    else:
        target = to + ('/index.html' if preview else '/')
    url = prefix + target
    return url or './'


def parse(slug):
    with open(os.path.join(SRC, slug + '.html'), encoding='utf-8') as f:
        text = f.read()
    m = re.match(r'\s*<!--meta\n(.*?)\n-->\n', text, re.S)
    meta = dict(line.split(':', 1) for line in m.group(1).splitlines() if ':' in line)
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    return meta, text[m.end():]


def fill(html, slug, preview):
    root = '../' * depth(slug) if slug != '404' else '/'
    if preview and slug == '404':
        root = ''
    html = re.sub(r'\{\{icon:([\w-]+)\}\}', lambda m: icon(m.group(1)), html)
    html = re.sub(r'\{\{url:([\w-]+)\}\}', lambda m: make_url(slug, m.group(1), preview) if not (slug == '404' and not preview) else ('/' if m.group(1) == 'index' else '/' + m.group(1) + '/'), html)
    art = ('<div class="art" aria-hidden="true"><svg viewBox="0 0 200 200"><path d="M100,185 C45,180 8,140 10,92 C68,88 106,126 100,185Z" fill="#fbeaeb"/>'
           '<path d="M100,185 C42,152 32,78 60,24 C118,52 136,122 100,185Z" fill="#e3f4ee"/><path d="M100,185 C162,152 178,72 146,20 C88,46 68,122 100,185Z" fill="#e3f2f8"/></svg></div>')
    html = html.replace('<section class="page-hero"><div class="wrap">', '<section class="page-hero">' + art + '<div class="wrap">')
    return html.replace('{{root}}', root)


def nav_html(slug):
    items = []
    for s, en in NAV:
        cur = ' aria-current="page"' if s == slug else ''
        items.append(f'<li><a href="{{{{url:{s}}}}}"{cur}>{en}</a></li>')
    mobile = ''
    for s, en in NAV + [('internship', 'Internship')]:
        cur = ' aria-current="page"' if s == slug else ''
        mobile += f'<a href="{{{{url:{s}}}}}"{cur}>{en}</a>'
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="nav-shell"><nav class="nav" aria-label="Main">
  <a class="brand" href="{{{{url:index}}}}"><img src="{{{{root}}}}assets/img/heal-logo.png" alt="Heal Social Foundation, home" width="85" height="32"></a>
  <ul class="nav-links">{''.join(items)}</ul>
  <div class="nav-tools">
    <a class="btn btn-primary btn-sm btn-donate" href="{{{{url:donate}}}}">{{{{icon:heart}}}}<span>Donate</span></a>
    <button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mobile-menu"><i></i><i></i><i></i></button>
  </div>
</nav></div>
<div class="mobile-panel" id="mobile-menu">{mobile}<a class="btn btn-primary" href="{{{{url:donate}}}}">Donate</a></div>'''


FOOTER = '''<footer><div class="wrap">
  <div class="foot">
    <div>
      <a class="brand" href="{{url:index}}" style="margin-bottom:12px"><img src="{{root}}assets/img/heal-logo.png" alt="Heal Social Foundation" width="107" height="40"></a>
      <p class="body-6 muted" style="max-width:340px">Health, Education, Awareness and Love for Humanity. A Section 42 nonprofit in Karachi, Pakistan.</p>
      <div class="social">
        <a href="https://www.facebook.com/HealAidFoundation" aria-label="Facebook" rel="noopener" target="_blank">{{icon:facebook-logo}}</a>
        <a href="https://www.instagram.com/healaidfoundation/" aria-label="Instagram" rel="noopener" target="_blank">{{icon:instagram-logo}}</a>
        <a href="https://www.linkedin.com/company/healsocialfoundation" aria-label="LinkedIn" rel="noopener" target="_blank">{{icon:linkedin-logo}}</a>
      </div>
    </div>
    <div><h2>Organisation</h2><ul>
      <li><a href="{{url:about}}">About us</a></li>
      <li><a href="{{url:our-work}}">Our work</a></li>
      <li><a href="{{url:research-cphi}}">Research &amp; CPHI</a></li>
      <li><a href="{{url:eleven-labs}}">ElevenLabs programme</a></li>
    </ul></div>
    <div><h2>Get involved</h2><ul>
      <li><a href="{{url:donate}}">Donate</a></li>
      <li><a href="{{url:joinpartner}}">Join or partner</a></li>
      <li><a href="{{url:internship}}">Internship</a></li>
    </ul></div>
    <div><h2>Contact</h2><ul>
      <li><a href="mailto:team@healsocialfoundation.com">team@healsocialfoundation.com</a></li>
      <li><a href="tel:+923350338177" dir="ltr">+92 335 0338177</a></li>
      <li><a href="{{url:contact-us}}">All contact details</a></li>
    </ul></div>
  </div>
  <div class="legal"><span>© <span data-year>2026</span> Heal Social Foundation · SECP CUIN 0265422 · NTN E445846</span><a href="{{url:privacy}}" class="foot-a" style="color:inherit">Privacy</a></div>
</div></footer>
<div class="toast" role="status" aria-live="polite"></div>'''


def page(slug, preview):
    meta, body = parse(slug)
    title = meta['title']
    full_title = 'Heal Social Foundation' if slug == 'index' else f'{title} · Heal Social Foundation'
    canonical = SITE + ('/' if slug == 'index' else f'/{slug}/')
    head = f'''<title>{full_title}</title>
<meta name="description" content="{meta['description']}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Heal Social Foundation">
<meta property="og:title" content="{full_title}"><meta property="og:description" content="{meta['description']}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="{{{{root}}}}assets/favicon.png" type="image/png"><link rel="apple-touch-icon" href="{{{{root}}}}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{{{{root}}}}assets/site.css">'''
    if slug == '404':
        head += '\n<meta name="robots" content="noindex">'
    content = f'''{nav_html(meta.get('nav', slug))}
<main id="main">
{body}
</main>
{FOOTER}
<script src="{{{{root}}}}assets/site.js"></script>'''
    if preview and slug == 'index':
        # the artifact host adds its own document wrapper to the entry page
        html = f'<meta name="claude:viewport-fit-sides" content="cover">\n{head}\n{content}'
    else:
        html = f'''<!doctype html>
<html lang="en" dir="ltr" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head}
</head>
<body>
{content}
</body>
</html>'''
    return fill(html, slug, preview)


def build(out, preview=False):
    for slug in PAGES:
        path = os.path.join(out, out_path(slug))
        os.makedirs(os.path.dirname(path) or out, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(page(slug, preview))
    # old Google Sites address /home -> home page
    os.makedirs(os.path.join(out, 'home'), exist_ok=True)
    home = make_url('about', 'index', preview)
    with open(os.path.join(out, 'home', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(f'<!doctype html><meta charset="utf-8"><title>Heal Social Foundation</title><meta http-equiv="refresh" content="0; url={home}"><link rel="canonical" href="{SITE}/"><a href="{home}">Go to the home page</a>')
    # research page embed, served beside the page
    shutil.copy(os.path.join(ROOT, 'src', 'research-embed.html'), os.path.join(out, 'research-cphi', 'embed.html'))
    if out != ROOT:
        shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(out, 'assets'), dirs_exist_ok=True)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--preview':
        build(os.path.abspath(sys.argv[2]), preview=True)
    else:
        build(ROOT)
    print('built')
