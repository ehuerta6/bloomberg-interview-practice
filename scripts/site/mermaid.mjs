// Generated copy lives in docs/renderer/. Keep diagram source readable on failure.
const diagrams = document.querySelectorAll("pre.mermaid");

if (diagrams.length) {
  try {
    const { default: mermaid } = await import(
      "https://cdn.jsdelivr.net/npm/mermaid@12.2.0/dist/mermaid.esm.min.mjs"
    );
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: "strict",
      htmlLabels: false,
      theme: "base",
      look: "classic",
      themeVariables: {
        fontFamily: "system-ui, sans-serif",
        fontSize: "16px",
        primaryColor: "#ffffff",
        primaryTextColor: "#171717",
        primaryBorderColor: "#737373",
        secondaryColor: "#ffffff",
        tertiaryColor: "#f5f5f5",
        lineColor: "#525252",
        edgeLabelBackground: "#ffffff",
      },
      suppressErrorRendering: true,
      maxTextSize: 50000,
      maxEdges: 500,
      deterministicIds: true,
      deterministicIDSeed: "cic-interview-practice",
      secure: [
        "secure", "securityLevel", "startOnLoad", "htmlLabels",
        "suppressErrorRendering", "maxTextSize", "maxEdges",
      ],
    });
    for (const [index, source] of [...diagrams].entries()) {
      try {
        // Only site configuration is allowed; diagram directives/frontmatter can
        // otherwise override rendering options such as theme CSS.
        const text = source.textContent;
        if (/^\s*---/.test(text) || /%%\s*\{/.test(text)) {
          throw new Error("Diagram configuration belongs in the site renderer");
        }
        const { svg } = await mermaid.render(`cic-diagram-${index}`, text);
        const figure = document.createElement("figure");
        figure.className = "mermaid-diagram";
        figure.tabIndex = 0;
        figure.setAttribute("role", "region");
        figure.setAttribute("aria-label", `Diagram ${index + 1}; scroll to view the complete diagram`);
        // Mermaid's strict renderer sanitizes the generated SVG. Never insert
        // source Markdown or bind diagram click callbacks here.
        figure.innerHTML = svg;
        const graphic = figure.querySelector("svg");
        // Preserve readable native dimensions instead of shrinking labels to the
        // prose column. The focusable figure contains horizontal overflow.
        const { width, height } = graphic.viewBox.baseVal;
        graphic.setAttribute("width", width);
        graphic.setAttribute("height", height);
        graphic.style.maxWidth = "none";
        const caption = document.createElement("figcaption");
        caption.textContent = "Scroll to explore the diagram. Its text source follows.";
        figure.prepend(caption);
        const details = document.createElement("details");
        const summary = document.createElement("summary");
        summary.textContent = "Diagram source";
        details.append(summary);
        source.replaceWith(figure, details);
        details.append(source);
      } catch {
        source.dataset.renderStatus = "unavailable";
      }
    }
  } catch {
    for (const source of diagrams) source.dataset.renderStatus = "unavailable";
  }
}
