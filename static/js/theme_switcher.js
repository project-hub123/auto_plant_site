const THEME_KEY = "site_theme";

const THEMES = {
    default: "/static/css/style_default.css",
    accessible: "/static/css/style_accessible.css"
};

function applyTheme(themeName) {
    const link = document.getElementById("theme-style");
    if (!link) return;

    if (THEMES[themeName]) {
        link.setAttribute("href", THEMES[themeName]);
        localStorage.setItem(THEME_KEY, themeName);
    }
}

function toggleTheme() {
    const currentTheme = localStorage.getItem(THEME_KEY) || "default";
    const newTheme = currentTheme === "default" ? "accessible" : "default";
    applyTheme(newTheme);
}

document.addEventListener("DOMContentLoaded", function () {
    const savedTheme = localStorage.getItem(THEME_KEY) || "default";
    applyTheme(savedTheme);
});
