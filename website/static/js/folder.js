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