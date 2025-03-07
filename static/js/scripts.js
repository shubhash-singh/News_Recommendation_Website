document.addEventListener("DOMContentLoaded", function () {
    fetchNews("general"); // Load general news by default
});

// Fetch News from Backend (Replace URL with your Django API)
function fetchNews(category) {
    fetch(`/api/get_news?category=${category}`)
        .then(response => response.json())
        .then(data => {
            displayNews(data.articles);
        })
        .catch(error => console.error("Error fetching news:", error));
}

// Display News on Page
function displayNews(articles) {
    let newsContainer = document.getElementById("newsContainer");
    newsContainer.innerHTML = ""; // Clear previous content

    articles.forEach(article => {
        let newsCard = document.createElement("div");
        newsCard.classList.add("news-card");

        newsCard.innerHTML = `
            <img src="${article.image}" alt="News Image">
            <h3>${article.title}</h3>
            <p>${article.description}</p>
            <a href="${article.url}" target="_blank">Read More</a>
        `;

        newsContainer.appendChild(newsCard);
    });
}

// Search News Articles
function searchNews() {
    let searchInput = document.getElementById("searchInput").value.toLowerCase();
    let newsCards = document.querySelectorAll(".news-card");

    newsCards.forEach(card => {
        let title = card.querySelector("h3").textContent.toLowerCase();
        card.style.display = title.includes(searchInput) ? "block" : "none";
    });
}


async function getNews() {
    const response = await fetch('http://localhost:8080/registerUser', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json'}
    });

    const data = await response.json();
    displayNews(data);
    

}
getNews();