// theme_switcher.js
// Переключение стандартного стиля и версии для слабовидящих
// Проект: "Автомобильный завод"

// имя ключа в localStorage
const THEME_KEY = "site_theme";

// пути к стилям
const THEMES = {
    default: "/static/css/style_default.css",
    accessible: "/static/css/style_accessible.css"
};

// применение темы
function applyTheme(themeName) {
    const link = document.getElementById("theme-style");
    if (!link) return;

    if (THEMES[themeName]) {
        link.setAttribute("href", THEMES[themeName]);
        localStorage.setItem(THEME_KEY, themeName);
    }
}

// переключение темы по кнопке
function toggleTheme() {
    const currentTheme = localStorage.getItem(THEME_KEY) || "default";
    const newTheme = currentTheme === "default" ? "accessible" : "default";
    applyTheme(newTheme);
}

// загрузка сохранённой темы при открытии страницы
document.addEventListener("DOMContentLoaded", function () {
    const savedTheme = localStorage.getItem(THEME_KEY) || "default";
    applyTheme(savedTheme);
});
