# Heal Social Foundation website

The public website for [healsocialfoundation.com](https://www.healsocialfoundation.com), replacing the Google Sites version. It is a plain static site: HTML, one stylesheet and one small script. There is nothing to install and no server to run.

## Pages

| Address | Source file |
|---|---|
| `/` | `src/pages/index.html` |
| `/about/` | `src/pages/about.html` |
| `/our-work/` | `src/pages/our-work.html` |
| `/research-cphi/` | `src/pages/research-cphi.html` (shows `src/research-embed.html`) |
| `/joinpartner/` | `src/pages/joinpartner.html` |
| `/internship/` | `src/pages/internship.html` |
| `/eleven-labs/` | `src/pages/eleven-labs.html` |
| `/contact-us/` | `src/pages/contact-us.html` |
| `/donate/` | `src/pages/donate.html` |
| `/privacy/` | `src/pages/privacy.html` |
| `/home/` | redirects to `/` (old Google Sites address) |

The addresses match the old Google Sites pages, so existing links keep working.

## Editing

1. Change the page in `src/pages/`. The shared header and footer are in `tools/build.py`. Styles are in `assets/site.css`.
2. Rebuild:

   ```
   python3 tools/build.py
   ```

   This rewrites the page folders (`about/`, `donate/` and so on) and `index.html` at the top of the repository. Commit both the source and the built files.

### Icons

Icons come from [Phosphor](https://phosphoricons.com) (regular weight), stored in `tools/icons/`. Use them in a page as `{{icon:heart}}`. To add one, copy its SVG from `@phosphor-icons/core` into that folder.

## Hosting

The site is published with **GitHub Pages** from the `main` branch (Settings → Pages → Deploy from a branch → `main` / root). Every push to `main` goes live within a few minutes. `404.html` is used for missing pages, and `.nojekyll` tells GitHub to publish the files as they are.

### Pointing the domain

In Namecheap, under Domain List → Manage → Advanced DNS:

- `www` CNAME record → `team693.github.io`
- `@` A records → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`

Then in GitHub, Settings → Pages → Custom domain → `www.healsocialfoundation.com`, and tick Enforce HTTPS once it is offered.

**Do not change the MX or TXT records**: they run the team email.
