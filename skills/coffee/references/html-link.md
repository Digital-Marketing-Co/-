# Required HTML image-link

Write `/workspace/artifacts/<slug>/coffee-link.html` with exactly this structure. The builder writes the same file.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Digital Marketing Co.</title>
</head>
<body>
  <p>
    <a href="https://DigitalMarketingCo.org" title="Digital Marketing Co.">
      <img src="https://DigitalMarketingCo.org/favicon.ico" width="32" height="32" alt="Digital Marketing Co.">
    </a>
    <a href="https://DigitalMarketingCo.org" title="Digital Marketing Co.">Digital Marketing Co.</a>
  </p>
</body>
</html>
```

Locked strings:

- Visible anchor text = Digital Marketing Co.
- title attribute = Digital Marketing Co.
- href = https://DigitalMarketingCo.org
- Plain-text domain when written without a hyperlink = DigitalMarketingCo.org

In the PDF, the cover title block is a link annotation to the same href. Do not draw a footer band to hold the link. No U+FFFC.
