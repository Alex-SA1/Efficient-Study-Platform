function openDeleteFolderConfirmation(folderId) {
    const buttonId = `deleteFolder${folderId}Btn`;
    const deleteFolderBtn = document.getElementById(buttonId);
    const deleteFolderUrl = deleteFolderBtn.dataset.deleteFolderUrl;
    const csrfToken = document.getElementById('flashcards-page-main-script').dataset.csrfToken;
    const textTitle = 'Are you sure you want to delete this folder?'

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
            fetch(deleteFolderUrl, {
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
                    if (data.error) {
                        Swal.fire({
                            title: "Oops...",
                            text: data.error,
                            icon: "error",
                            color: '#e4e0f3',
                            background: '#110f16'
                        })

                        return;
                    }

                    const folderElementId = "folder-" + folderId;
                    const folderElement = document.getElementById(folderElementId);

                    if (folderElement) {
                        folderElement.remove();

                        const folderParentElement = document.getElementById('folders-section');
                        if (folderParentElement.querySelectorAll('div').length === 1) {
                            const noFoldersElement = document.getElementById('no-folders');
                            noFoldersElement.style.display = 'block';
                        }
                    }

                    Swal.fire({
                        title: "Deleted",
                        text: "The folder has been successfully deleted!",
                        icon: "success",
                        color: '#e4e0f3',
                        background: '#110f16'
                    })
                })
                .catch(
                    Swal.fire({
                        title: "Oops...",
                        text: "There was an error deleting the folder!",
                        icon: "error",
                        color: '#e4e0f3',
                        background: '#110f16'
                    })
                )
        }
    });
}