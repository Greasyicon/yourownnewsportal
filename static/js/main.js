let start = 0;
let end = 2;
let loading = false;



function toggleLoadingSpinner(visible) {
  const spinner = document.getElementById("loading-spinner");
  if (visible) {
    spinner.style.display = "block";
  } else {
    spinner.style.display = "none";
  }
}

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
  toggleLoadingSpinner(true); // Show the loading spinner
  fetch(`/scrape_more_articles?start=${start}&end=${end}`)
    .then((response) => response.json())
    .then((data) => {
//      const articlesContainer = document.getElementById("articles-container");
        const container = document.querySelector(".container");
        container.insertAdjacentHTML("beforeend", data.html);
        loading = false;
        toggleLoadingSpinner(false); // Hide the loading spinner
    })
    .catch((error) => {
      console.error("Error fetching more articles:", error);
      loading = false;  ``
      toggleLoadingSpinner(false); // Hide the loading spinner
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


document.getElementById("updateButton").addEventListener("click", function () {
  toggleLoadingSpinner(true); // Show the loading spinner
  fetch("/update_content")
    .then((response) => {
      if (response.ok) {
        location.reload(); // Refresh the page
      } else {
        console.error("Error updating content:", response.statusText);
        toggleLoadingSpinner(false); // Hide the loading spinner
      }
    })
    .catch((error) => {
      console.error("Error updating content:", error);
      toggleLoadingSpinner(false); // Hide the loading spinner
    });
});
