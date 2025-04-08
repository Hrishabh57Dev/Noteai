document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file-input");
    const uploadButton = document.getElementById("upload-button");
    const transcriptionOutput = document.getElementById("transcription-output");
    const summaryOutput = document.getElementById("summary-output");
    const keywordsOutput = document.getElementById("keywords-output");
    const searchNotesInput = document.getElementById("search-notes");
    const notesList = document.getElementById("notes-list");
    const darkModeToggle = document.getElementById("dark-mode-toggle");

    let notes = []; // Store notes locally for dynamic UI updates

    // Toggle dark mode
    darkModeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
    });

    // Upload file and process transcription
    uploadButton.addEventListener("click", async () => {
        const file = fileInput.files[0];
        if (!file) {
            alert("Please select a file to upload.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("http://localhost:5000/transcribe", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            if (response.ok) {
                transcriptionOutput.value = data.transcription;
                alert("Transcription completed!");
            } else {
                alert(data.error || "Failed to transcribe the file.");
            }
        } catch (error) {
            console.error("Error during transcription:", error);
            alert("An error occurred while processing the file.");
        }
    });

    // Summarize transcription
    transcriptionOutput.addEventListener("input", async () => {
        const transcription = transcriptionOutput.value;
        if (!transcription) return;

        try {
            const response = await fetch("http://localhost:5000/summarize", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ transcription }),
            });
            const data = await response.json();
            if (response.ok) {
                summaryOutput.value = data.summary;
            } else {
                alert(data.error || "Failed to summarize the text.");
            }
        } catch (error) {
            console.error("Error during summarization:", error);
            alert("An error occurred while summarizing the text.");
        }
    });

    // Extract keywords
    summaryOutput.addEventListener("input", async () => {
        const text = summaryOutput.value;
        if (!text) return;

        try {
            const response = await fetch("http://localhost:5000/extract_keywords", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text, method: "spacy" }),
            });
            const data = await response.json();
            if (response.ok) {
                keywordsOutput.innerHTML = "";
                data.keywords.forEach((keyword) => {
                    const li = document.createElement("li");
                    li.textContent = `${keyword.keyword} (Score: ${keyword.score.toFixed(2)})`;
                    keywordsOutput.appendChild(li);
                });
            } else {
                alert(data.error || "Failed to extract keywords.");
            }
        } catch (error) {
            console.error("Error during keyword extraction:", error);
            alert("An error occurred while extracting keywords.");
        }
    });

    // Fetch and display notes
    async function fetchNotes() {
        try {
            const response = await fetch("http://localhost:5000/notes");
            const data = await response.json();
            if (response.ok) {
                notes = data.notes;
                renderNotes();
            } else {
                alert(data.error || "Failed to fetch notes.");
            }
        } catch (error) {
            console.error("Error fetching notes:", error);
            alert("An error occurred while fetching notes.");
        }
    }

    // Render notes dynamically
    function renderNotes() {
        notesList.innerHTML = "";
        const searchQuery = searchNotesInput.value.toLowerCase();
        const filteredNotes = notes.filter((note) =>
            note.title.toLowerCase().includes(searchQuery)
        );

        filteredNotes.forEach((note) => {
            const noteDiv = document.createElement("div");
            noteDiv.classList.add("note");

            const title = document.createElement("h3");
            title.textContent = note.title;

            const deleteButton = document.createElement("button");
            deleteButton.textContent = "Delete";
            deleteButton.addEventListener("click", async () => {
                try {
                    const response = await fetch(`http://localhost:5000/notes/${note.id}`, {
                        method: "DELETE",
                    });
                    if (response.ok) {
                        notes = notes.filter((n) => n.id !== note.id);
                        renderNotes();
                        alert("Note deleted successfully!");
                    } else {
                        alert("Failed to delete the note.");
                    }
                } catch (error) {
                    console.error("Error deleting note:", error);
                    alert("An error occurred while deleting the note.");
                }
            });

            noteDiv.appendChild(title);
            noteDiv.appendChild(deleteButton);
            notesList.appendChild(noteDiv);
        });
    }

    // Search notes
    searchNotesInput.addEventListener("input", renderNotes);

    // Initial fetch of notes
    fetchNotes();
});
