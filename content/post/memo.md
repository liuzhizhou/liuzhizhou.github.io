---
title:  "Memorandum for the Configuration of This Site"
date:   2023-06-02T12:13:38+08:00
draft:  false
summary: Just a memorandum for the configuration of this Site in case I forget in the future.
---

- View the page by `hugo server`.
- Adjust several parameters in `config.toml` [^1] to make it look like you personal website.
- The file controlling the header is `themes/brutalist-minimalist/layouts/partials/nav-link.html`.
- The file controlling the copyright notice and footer is `themes/brutalist-minimalist/layouts/partials/copyright-notice.html` and `obligatory-links.html` in the same path.
- All URL links to be converted by Hugo should be in `contents`; add `_index.md` document if necessary to generate a URL link of a folder.
- Use latexml to convert a `.tex` file to a `.html` file directly:

[^1]: This has been changed to `hugo.toml` recently.

```shell
latexml ref.bib --dest=ref.bib.xml
latexmlc main.tex --dest=mltest.html ref.bib.xml
```

- Add "head" to the html file:

```html
+++ 
title = "Solutions and Numerical Solutions of Stochastic Differential Equations"
date = 2023-06-02
summary = "A simple introduction"
tags = ["hugo", "html"]
+++
```

- the value of parameter `summary` would be presented after title.
- If you want to adjust the style of fonts, for example, delete the bold purpule font at the first letter, then you should adjust `themes/brutalist-minimalist/static/css/beyond-minimalism.css`.