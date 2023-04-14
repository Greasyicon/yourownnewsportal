let start = 0;
let end = 2;
let loading = false;

window.addEventListener("scroll", function () {
  if (
    window.scrollY + window.innerHeight >=
      document.documentElement.scrollHeight &&
    !loading
  ) {
    start += 2;
    end += 2;
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
