function showFlashcardsActions() {
    const buttonElement = document.getElementById('showFlashcardsActionsBtn');
    const updateFlashcardBtns = document.querySelectorAll('.update-flashcard');
    const deleteFlashcardBtns = document.querySelectorAll('.delete-flashcard');

    updateFlashcardBtns.forEach(button => {
        if (button.style.display === 'none')
            button.style.display = 'block';
        else
            button.style.display = 'none';
    })

    deleteFlashcardBtns.forEach(button => {
        if (button.style.display === 'none')
            button.style.display = 'block';
        else
            button.style.display = 'none';
    })

    if (buttonElement.textContent === 'Show Flashcards Actions')
        buttonElement.textContent = 'Hide Flashcards Actions';
    else
        buttonElement.textContent = 'Show Flashcards Actions';
}

function openDeleteFlashcardConfirmation(flashcardId) {
    const buttonId = `deleteFlashcard${flashcardId}Btn`;
    const deleteFlashcardBtn = document.getElementById(buttonId);
    const deleteFlashcardUrl = deleteFlashcardBtn.dataset.deleteFlashcardUrl;
    const csrfToken = document.getElementById('folder-page-main-script').dataset.csrfToken;
    const textTitle = 'Are you sure you want to delete this flashcard?'

    Swal.fire({
        title: textTitle,
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!",
        color: '#e4e0f3',
        background: '#110f16'
    }).then((result) => {
        if (result.isConfirmed) {
            fetch(deleteFlashcardUrl, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({})
            })
                .then(response => response.json())
                .then(data => {
                    const flashcardElementId = "flashcard-" + flashcardId;
                    const flashcardElement = document.getElementById(flashcardElementId);

                    if (flashcardElement) {
                        flashcardElement.remove();

                        const flashcardParentElement = document.getElementById('flashcards-section');
                        if (flashcardParentElement.querySelectorAll('div').length === 1) {
                            const noFlashcardsElement = document.getElementById('no-flashcards');
                            noFlashcardsElement.style.display = 'block';

                            const showFlashcardsButtonSection = document.getElementById('showFlashcardsButtonSection');
                            showFlashcardsButtonSection.remove();
                        }
                    }

                    Swal.fire({
                        title: "Deleted",
                        text: "The flashcard has been successfully deleted!",
                        icon: "success",
                        color: '#e4e0f3',
                        background: '#110f16'
                    })
                })
                .catch(
                    Swal.fire({
                        title: "Oops...",
                        text: "There was an error deleting the flashcard!",
                        icon: "error",
                        color: '#e4e0f3',
                        background: '#110f16'
                    })
                )
        }
    });
}