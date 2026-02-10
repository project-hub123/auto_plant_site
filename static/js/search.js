// search.js
// Клиентская логика поиска по сайту
// Проект: "Автомобильный завод"

// минимальная длина поискового запроса
const MIN_QUERY_LENGTH = 2;

// инициализация поиска
document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("search-form");
    const searchInput = document.getElementById("search-input");

    if (!searchForm || !searchInput) return;

    // проверка перед отправкой формы
    searchForm.addEventListener("submit", function (event) {
        const query = searchInput.value.trim();

        if (query.length < MIN_QUERY_LENGTH) {
            event.preventDefault();
            alert("Введите не менее двух символов для поиска");
            searchInput.focus();
        }
    });
});

// подсветка найденного текста на странице результатов
function highlightResults(query) {
    if (!query) return;

    const contentBlocks = document.querySelectorAll(".card, article, main");

    contentBlocks.forEach(block => {
        const html = block.innerHTML;
        const regex = new RegExp(`(${query})`, "gi");
        block.innerHTML = html.replace(
            regex,
            `<span style="background-color: yellow; color: black;">$1</span>`
        );
    });
}
