document.addEventListener("DOMContentLoaded", () => {
    const audio = new Audio();

    let currentSongSlug = null;
    let playCounted = false;

    const player = document.querySelector("#music-player");
    const playerTitle = document.querySelector(".player-title");
    const playerArtist = document.querySelector(".player-artist");
    const playerCover = document.querySelector(".player-cover");
    const playerPlayButton = document.querySelector(".player-play-button");
    const playerProgress = document.querySelector(".player-progress");
    const currentTime = document.querySelector(".player-current-time");
    const durationDisplay = document.querySelector(".player-duration");
    const playerStatus = document.querySelector(".player-status");

    if (!player) {
        return;
    }

    function formatTime(seconds) {
        if (!Number.isFinite(seconds) || seconds < 0) {
            return "0:00";
        }

        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);

        return `${minutes}:${String(remainingSeconds).padStart(2, "0")}`;
    }

    function setStatus(message) {
        if (playerStatus) {
            playerStatus.textContent = message;
        }
    }

    function updatePlayButtons() {
        const isPlaying = !audio.paused;

        document.querySelectorAll(".play-button, .row-play").forEach(button => {
            const isCurrentSong =
                button.dataset.songSlug === currentSongSlug;

            button.dataset.playing = String(isPlaying && isCurrentSong);

            if (button.classList.contains("play-button")) {
                button.textContent =
                    isPlaying && isCurrentSong ? "Ⅱ" : "▶";
            }
        });

        if (playerPlayButton) {
            playerPlayButton.textContent = isPlaying ? "Ⅱ" : "▶";
            playerPlayButton.setAttribute(
                "aria-label",
                isPlaying ? "Pause" : "Play"
            );
        }
    }

    function updatePlayer(button) {
        if (playerTitle) {
            playerTitle.textContent = button.dataset.songTitle || "Unknown song";
        }

        if (playerArtist) {
            playerArtist.textContent = button.dataset.artistName || "Unknown artist";
        }

        if (playerCover) {
            playerCover.src =
                button.dataset.songCover ||
                button.dataset.albumCover ||
                playerCover.dataset.placeholder ||
                playerCover.src;
        }

        if (playerProgress) {
            playerProgress.value = 0;
        }

        if (currentTime) {
            currentTime.textContent = "0:00";
        }

        if (durationDisplay) {
            durationDisplay.textContent = "0:00";
        }
    }

    async function countPlay(slug) {
        if (playCounted || !slug) {
            return;
        }

        const csrfToken = document.querySelector(
            "[name=csrfmiddlewaretoken]"
        )?.value;

        try {
            const response = await fetch(
                `/music/songs/${encodeURIComponent(slug)}/plays/`,
                {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken || getCookie("csrftoken"),
                        "X-Requested-With": "XMLHttpRequest"
                    }
                }
            );

            if (!response.ok) {
                throw new Error(`Play counter request failed: ${response.status}`);
            }

            playCounted = true;
        } catch (error) {
            console.error("Could not update song plays:", error);
        }
    }

    async function playSong(button) {
        const audioUrl = button.dataset.audioUrl;
        const slug = button.dataset.songSlug;

        if (!audioUrl || !slug) {
            setStatus("Song audio is unavailable");
            console.error("Missing audio URL or song slug", button);
            return;
        }

        if (currentSongSlug !== slug) {
            audio.pause();

            currentSongSlug = slug;
            playCounted = false;

            audio.src = audioUrl;
            audio.load();

            updatePlayer(button);
        }

        try {
            await audio.play();
            setStatus("Now playing");
            updatePlayButtons();
        } catch (error) {
            setStatus("Unable to play this audio");
            console.error("Audio playback failed:", error);
        }
    }

    document.querySelectorAll(".row-play, .play-button").forEach(button => {
        button.addEventListener("click", () => {
            const isCurrentSong =
                button.dataset.songSlug === currentSongSlug;

            if (isCurrentSong && !audio.paused) {
                audio.pause();
            } else {
                playSong(button);
            }
        });
    });

    playerPlayButton?.addEventListener("click", async () => {
        if (!audio.src) {
            setStatus("Choose a song first");
            return;
        }

        if (audio.paused) {
            try {
                await audio.play();
            } catch (error) {
                setStatus("Unable to play this audio");
                console.error("Audio playback failed:", error);
            }
        } else {
            audio.pause();
        }
    });

    audio.addEventListener("playing", () => {
        setStatus("Now playing");
        updatePlayButtons();
        countPlay(currentSongSlug);
    });

    audio.addEventListener("pause", () => {
        updatePlayButtons();

        if (audio.currentTime > 0 && !audio.ended) {
            setStatus("Paused");
        }
    });

    audio.addEventListener("loadedmetadata", () => {
        if (durationDisplay) {
            durationDisplay.textContent = formatTime(audio.duration);
        }
    });

    audio.addEventListener("timeupdate", () => {
        if (playerProgress && audio.duration) {
            playerProgress.value =
                (audio.currentTime / audio.duration) * 100;
        }

        if (currentTime) {
            currentTime.textContent = formatTime(audio.currentTime);
        }
    });

    playerProgress?.addEventListener("input", () => {
        if (audio.duration) {
            audio.currentTime =
                (Number(playerProgress.value) / 100) * audio.duration;
        }
    });

    audio.addEventListener("ended", () => {
        updatePlayButtons();
        setStatus("Finished");
    });

    audio.addEventListener("error", () => {
        setStatus("Audio file could not be loaded");
        console.error("Audio element error:", audio.error, audio.src);
    });

    function getCookie(name) {
        const cookie = document.cookie
            .split("; ")
            .find(item => item.startsWith(`${name}=`));

        return cookie
            ? decodeURIComponent(cookie.substring(name.length + 1))
            : null;
    }
});


document.addEventListener("click", async (event) => {
    const favoriteButton = event.target.closest(".row-favorite");

    if (!favoriteButton) {
        return;
    }

    event.preventDefault();

    const slug = favoriteButton.dataset.songSlug;

    if (!slug) {
        return;
    }

    if (favoriteButton.dataset.loading === "true") {
        return;
    }

    favoriteButton.dataset.loading = "true";

    try {
        const response = await fetch(
            `/music/songs/${slug}/favorite/`,
            {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest",
                },
            }
        );

        if (!response.ok) {
            throw new Error("Failed to update favorite.");
        }

        const data = await response.json();

        if (data.is_favorite) {
            favoriteButton.classList.add("is-favorite");

            favoriteButton.querySelector(
                ".favorite-icon"
            ).textContent = "♥";

            favoriteButton.setAttribute(
                "aria-label",
                "Remove from favorites"
            );

            favoriteButton.setAttribute(
                "aria-pressed",
                "true"
            );
        } else {
            favoriteButton.classList.remove("is-favorite");

            favoriteButton.querySelector(
                ".favorite-icon"
            ).textContent = "♡";

            favoriteButton.setAttribute(
                "aria-label",
                "Add to favorites"
            );

            favoriteButton.setAttribute(
                "aria-pressed",
                "false"
            );
        }
    } catch (error) {
        console.error("Favorite error:", error);
    } finally {
        favoriteButton.dataset.loading = "false";
    }
});