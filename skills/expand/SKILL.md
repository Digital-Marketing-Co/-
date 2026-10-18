---
name: expand
description: Exhaustively expand a research topic or existing document into a citation-grounded, logically ordered, cross-linked multi-volume hierarchy with subsection-specific visualizations, banners, images, iterative research and QA.
metadata:
  type: workflow
  version: "1.0.0"
  flag: /expand
---

# /expand — Research Hierarchy Expansion Engine

## Invocation
/expand <topic or document> [optional /atlas /deep /iterate /banner /images /latex /copyright /wca-ivy-biblio /itqe]

## Governing principles
Expand to the limits of relevant verifiable evidence, not arbitrary chapter, word, page, image or citation quotas. If the output is too large for one artifact, partition it into linked volumes and maintain a master index. Never pad or repeat material to increase length. Do not claim to have researched, generated, tested, or verified unperformed work.

## 1. Extract root concepts and build a knowledge graph
Identify primary keywords, aliases, definitions, dates, people, methods, controversies, quantitative measures, related disciplines, and historical predecessors. Build nodes with stable IDs and typed edges: prerequisite, chronology, causal hypothesis, contrast, application, evidence, criticism, and broader/narrower topic. Use Wikipedia.org article links and category pages for discovery and cross-navigation, not as the sole authority for contested claims. Follow article references to primary papers, scholarly books, archival documents, standards and official statistics. Preserve canonical article URLs, retrieved dates, stable identifiers (DOI/ISBN/archival reference) and provenance.

## 2. Plan the exhaustive hierarchy before prose
Order volumes > parts > chapters > sections > subsections > research questions > evidence/figures. Prerequisites before advanced material, chronology where appropriate, and thematic cross-links for non-linear connections. Generate a coverage matrix for every root keyword and missing or underrepresented branches. Every node stores id, parent_id, title, abstract, keywords, cross_links, wikipedia_links, source_ids, figures, banner, research_status, confidence and outstanding_questions. Use a deterministic table of contents and stable anchors. Expand recursively until remaining subtopics are redundant, unsupported, or outside scope; document exclusions.

## 3. Deep research and exposition
For each node: explain origins, mechanisms, technical details, representative cases, empirical findings, quantitative statistics with units and denominators, limitations, rival explanations, and open problems. Distinguish established fact, derived calculation, interpretation, conjecture, and falsifiable hypothesis. Trace every material assertion to a source, flag source disagreement and dates, and never invent data or citations. Include mathematical derivations and correctly rendered LaTeX where appropriate; validate subscripts, underscores, symbols, equation references and units. Apply /itqe only where a genuine economic modeling connection exists, and label modeled assumptions.

## 4. Visual evidence specification
Each chapter, section and subsection gets a unique /banner derived from its own text, plus contextually relevant /images integrated beside the corresponding passage. Every subsection gets at least one *planned* visual evidence slot; render an actual chart only when sourced numeric data supports it. Prefer reproducible programmatic plots for precise data, equations, timelines, networks and tables. AI-generated futuristic visualizations may enhance the design, but cannot substitute for faithful quantitative charts or fabricate statistics. Put labels, values, sources and uncertainty in editable typography rather than unreliable image-baked text. Each figure stores node_id, caption, claim_ids, source_ids, alt_text, data provenance, generation prompt, placement anchor and QA status. For imagery, require literal semantic correspondence to the subsection's named subjects; reject generic futuristic imagery, mismatched chronology, invented devices, misleading portraits, false agency markings, duplicates and irrelevant decorative scenes. Validate aspect ratio, legibility, accessible contrast, source attribution and contextual placement.

## 5. Iteration and quality gates
Run /deep and /iterate cycles: discover gaps -> expand outline -> retrieve sources -> write -> check factual claims -> calculate -> render visuals -> inspect -> cross-link -> repeat. QA gates: orphan headings, dangling links, unsourced statistics, fabricated citations, unsupported hypotheses, repeated prose, irrelevant images, duplicate images, unreadable figures, overflowing text, broken LaTeX, missing alt text, and absent chapter/subsection banners. Produce a coverage report with completed/pending nodes and evidence confidence. Stop only at a real capability or source boundary; mark unfinished work explicitly.

## 6. Outputs
Write an outline/knowledge graph, evidence ledger, bibliography, cross-reference index, visual manifest, volume files, and QA report. Integrate /atlas, /wca-ivy-biblio, /copyright and existing document builder conventions. Use Chicago-style notes/bibliography if no other style is specified. Cite Wikipedia as navigation/context and stronger original sources for material factual claims. Deliver only artifacts actually generated and verified.
