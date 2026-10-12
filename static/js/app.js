document.addEventListener("DOMContentLoaded", () => {
    const audio = new Audio();

    let currentSongSlug = null;
    let playCounted = false;

    const playerTitle = document.querySelector(".player-title");
    const playerArtist = document.querySelector(".player-artist");
    const playerPlayButton = document.querySelector(".player-play-button");
    const playerProgress = document.querySelector(".player-progress");

    function updatePlayer(song) {
        if (playerTitle) {
            playerTitle.textContent = song.title;
        }

        if (playerArtist) {
            playerArtist.textContent = song.artist;
        }
    }

    async function countPlay(slug) {
        if (playCounted) {
            return;
        }

        try {
            const response = await fetch(`/music/songs/${slug}/plays/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            });

            if (response.ok) {
                playCounted = true;
            }
        } catch (error) {
            console.error("Failed to update play count:", error);
        }
    }

    function playSong(button) {
        const audioUrl = button.dataset.audioUrl;
        const title = button.dataset.songTitle;
        const artist = button.dataset.artistName;
        const slug = button.dataset.songSlug;

        if (!audioUrl) {
            return;
        }

        if (currentSongSlug !== slug) {
            audio.src = audioUrl;
            currentSongSlug = slug;
            playCounted = false;

            updatePlayer({
                title: title,
                artist: artist,
            });
        }

        audio.play();

        countPlay(slug);
        updatePlayButtons(button);
    }

    function pauseSong() {
        audio.pause();
        updatePlayButtons(null);
    }

    function updatePlayButtons(activeButton) {
        document.querySelectorAll(".play-button, .row-play").forEach(button => {
            button.dataset.playing = String(button === activeButton);
        });

        if (playerPlayButton) {
            playerPlayButton.textContent = audio.paused ? "▶" : "Ⅱ";
        }
    }

    document.querySelectorAll(".play-button, .row-play").forEach(button => {
        button.addEventListener("click", () => {
            const buttonSlug = button.dataset.songSlug;

            if (currentSongSlug === buttonSlug && !audio.paused) {
                pauseSong();
            } else {
                playSong(button);
            }
        });
    });

    if (playerPlayButton) {
        playerPlayButton.addEventListener("click", () => {
            if (!audio.src) {
                return;
            }

            if (audio.paused) {
                audio.play();
            } else {
                audio.pause();
            }
        });
    }

    audio.addEventListener("play", () => {
        updatePlayButtons(
            document.querySelector(
                `[data-song-slug="${currentSongSlug}"]`
            )
        );
    });

    audio.addEventListener("pause", () => {
        updatePlayButtons(null);
    });

    audio.addEventListener("ended", () => {
        updatePlayButtons(null);
    });

    audio.addEventListener("timeupdate", () => {
        if (!playerProgress || !audio.duration) {
            return;
        }

        playerProgress.value =
            (audio.currentTime / audio.duration) * 100;
    });

    if (playerProgress) {
        playerProgress.addEventListener("input", () => {
            if (!audio.duration) {
                return;
            }

            audio.currentTime =
                (playerProgress.value / 100) * audio.duration;
        });
    }

    function getCookie(name) {
        let cookieValue = null;

        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");

            for (let cookie of cookies) {
                cookie = cookie.trim();

                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
                    break;
                }
            }
        }

        return cookieValue;
    }
});