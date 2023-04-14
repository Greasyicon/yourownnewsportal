//let start = 0;
//let end = 5;
//let loading = false;
//
//window.addEventListener('scroll', function () {
//  if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight && !loading) {
//    start += 5;
//    end += 5;
//    loadMoreSources();
//  }
//});
//
//function loadMoreSources() {
//  loading = true;
//  fetch(`/scrape_more_sources?start=${start}&end=${end}`)
//    .then((response) => response.json())
//    .then((data) => {
//      // Iterate over the sources and articles, and add them to the DOM.
//      for (const [source, articles] of Object.entries(data)) {
//        const sourceElement = document.createElement('h2');
//        sourceElement.className = 'source';
//        sourceElement.id = source.replace(' ', '_');
//        sourceElement.textContent = source;
//
//        document.body.appendChild(sourceElement);
//
//        for (const [index, article] of articles.entries()) {
//          const articleElement = document.createElement('div');
//          articleElement.className = 'card h-100';
//          articleElement.id = `article-${source.replace(' ', '_')}-${index + 1}`;
//          articleElement.setAttribute('onclick', 'showArticle(this)');
//
//          const articleTitleElement = document.createElement('h3');
//          articleTitleElement.className = 'card-title';
//          articleTitleElement.textContent = article.title;
//          articleElement.appendChild(articleTitleElement);
//
//          const articleTextElement = document.createElement('p');
//          articleTextElement.className = 'card-text';
//          articleTextElement.textContent = article.text;
//          articleElement.appendChild(articleTextElement);
//
//          document.body.appendChild(articleElement);
//        }
//      }
//    })
//    .catch((error) => {
//      console.error('Error fetching more sources:', error);
//    })
//    .finally(() => {
//      loading = false;
//    });
//}

let start = 0;
let end = 5;
let loading = false;

window.addEventListener("scroll", function () {
  if (
    window.scrollY + window.innerHeight >=
      document.documentElement.scrollHeight &&
    !loading
  ) {
    start += 5;
    end += 5;
    loadMoreSources();
  }
});

function loadMoreSources() {
  loading = true;
  fetch(`/scrape_more_articles?start=${start}&end=${end}`)
    .then((response) => response.json())
    .then((data) => {
//      const articlesContainer = document.getElementById("articles-container");
        const container = document.querySelector(".container");
        container.insertAdjacentHTML("beforeend", data.html);
      loading = false;
    })
    .catch((error) => {
      console.error("Error fetching more articles:", error);
      loading = false;
    });
}
function showArticle(articleElement) {
  const overlayElement = articleElement.querySelector('.article-overlay');
  if (overlayElement) {
    overlayElement.style.display = 'block';
  }
}

function hideArticle(closeButtonElement) {
  const overlayElement = closeButtonElement.parentElement;
  if (overlayElement) {
    overlayElement.style.display = 'none';
  }
}
