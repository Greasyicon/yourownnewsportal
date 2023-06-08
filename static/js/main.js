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
//    window.innerHeight + window.pageYOffset >=
//    document.documentElement.offsetHeight - 500 &&
    window.innerHeight + window.scrollY + 1 >=
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
      loading = false;
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

let debouncedScroll = debounce(function () {
  if (
//    window.innerHeight + window.pageYOffset >=
//    document.documentElement.offsetHeight - 500 &&
    window.innerHeight + window.scrollY + 1 >=
      document.documentElement.scrollHeight &&
    !loading
  ) {
    start += 2;
    end += 2;
    loadMoreSources();
  }
}, 200);

window.addEventListener("scroll", debouncedScroll);

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}
