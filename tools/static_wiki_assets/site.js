(function () {
  const data = window.STELLAR_SEARCH_DATA || [];

  function normalize(value) {
    return String(value || "").toLowerCase();
  }

  function renderResult(item, root) {
    const link = document.createElement("a");
    link.className = "search-result";
    link.href = root + item.url;

    const title = document.createElement("strong");
    title.textContent = item.title;

    const meta = document.createElement("span");
    meta.textContent = item.type;

    const excerpt = document.createElement("small");
    excerpt.textContent = item.excerpt;

    link.append(title, meta, excerpt);
    return link;
  }

  function runSearch(input, results, root) {
    const query = normalize(input.value).trim();
    results.replaceChildren();
    if (query.length < 2) {
      return;
    }

    const matches = data
      .filter((item) => normalize(item.keywords).includes(query))
      .slice(0, 30);

    const status = document.createElement("p");
    status.className = "search-status";
    status.textContent = matches.length
      ? `${matches.length} result${matches.length === 1 ? "" : "s"} shown`
      : "No results";
    results.append(status);

    for (const item of matches) {
      results.append(renderResult(item, root));
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector("[data-search-input]");
    const results = document.querySelector("[data-search-results]");
    if (!input || !results) {
      return;
    }

    const root = document.body.dataset.root || "";
    input.addEventListener("input", function () {
      runSearch(input, results, root);
    });
    input.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        input.value = "";
        results.replaceChildren();
      }
    });
  });
})();
