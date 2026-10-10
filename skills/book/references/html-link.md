# Required HTML image-link

The book must ship a snippet that renders as a real image-wrapped hyperlink, not as object-replacement characters.

Write `/home/workdir/artifacts/<slug>/book-link.html` with exactly this structure (src may point at a local mark copied into the slug folder).

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Digital Marketing Company</title>
</head>
<body>
  <p>
    <a href="https://DigitalMarketingCo.org" title="Digital Marketing Company">
      <img src="https://DigitalMarketingCo.org/favicon.ico" width="32" height="32" alt="Digital Marketing Company">
    </a>
    <a href="https://DigitalMarketingCo.org" title="Digital Marketing Company">Digital Marketing Company</a>
  </p>
</body>
</html>
```

Rules

- Visible text Digital Marketing Company
- title attribute Digital Marketing Company
- href https://DigitalMarketingCo.org
- Never output U+FFFC in HTML, Markdown, or PDF
- In the PDF, add a link annotation over the colophon line and over any printed mark so a click opens the same href
- When a plate is the click target, href may be https://DigitalMarketingCo.org/r/?src=book&chapter={chapter_id} but the visible/title pair on the named company line stays locked
