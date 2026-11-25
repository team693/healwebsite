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

### English and Urdu

Text that exists in both languages is written twice, side by side:

```html
<span data-lang="en">Donate</span><span data-lang="ur">عطیہ کریں</span>
```

The اردو / English button in the header switches between them and remembers the choice. Text without `data-lang` shows in both languages.

### Icons

Icons come from [Phosphor](https://phosphoricons.com) (regular weight), stored in `tools/icons/`. Use them in a page as `{{icon:heart}}`. To add one, copy its SVG from `@phosphor-icons/core` into that folder.

## Hosting

Any static host works. Recommended: **Cloudflare Pages** (free), connected to this repository.

- Framework preset: None
- Build command: `python3 tools/build.py`
- Build output directory: `/`

Every push to `main` then goes live automatically. `404.html` is used for missing pages.

### Pointing the domain

In Namecheap, under Domain List → Manage → Advanced DNS, change only the records for the website (`www` and `@`) to the values the host gives you. **Do not change the MX or TXT records**: they run the team email.
