document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".like-button, .heart-button, .outline-icon-button").forEach(button => {
        button.addEventListener("click", () => {
            const isLiked = button.classList.toggle("liked");
            if ("heart-button" && (button.classList.contains("heart-button") || button.classList.contains("like-button") || button.classList.contains("outline-icon-button"))) {
                button.textContent = isLiked ? "♥" : "♡";
            }
        });
    });

    document.querySelectorAll(".play-button, .row-play").forEach(button => {
        button.addEventListener("click", () => {
            const playing = button.dataset.playing === "true";
            button.dataset.playing = String(!playing);
            if (button.classList.contains("play-button")) {
                button.textContent = playing ? "▶" : "Ⅱ";
            }
        });
    });

    document.querySelectorAll(".filter-chip, .search-category").forEach(button => {
        button.addEventListener("click", () => {
            const group = button.parentElement;
            group.querySelectorAll(".filter-chip, .search-category").forEach(item => item.classList.remove("active"));
            button.classList.add("active");
        });
    });
});