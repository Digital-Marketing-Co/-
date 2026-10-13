# Textbook schema (minimal)

textbook.json must contain:

- meta: title, subtitle, author, date, owner, house, abstract, keywords
- chapters: array of {id, title, level, paragraphs: [{type, text or equation}], banner, background}
- notes: array
- bibliography: array of {id, short, full, url, pdf_url}

Every bibliography entry prefers a real pdf_url from an Ivy League or academic site when found.
Equation paragraphs have type "equation", compiled_figure path, and itqe array.
