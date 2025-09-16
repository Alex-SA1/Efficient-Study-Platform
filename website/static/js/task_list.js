function getCookieCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split(';');

    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

function openDeleteTaskConfirmation(taskTitle, taskId) {
    const fetchURL = document.getElementById("btnOpenDeleteTaskConfirmation").value;
    textTitle = "Are you sure you want to delete the task \"" + taskTitle + "\" ?";

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
            fetch(fetchURL, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookieCSRFToken(),
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
                        });

                        return;
                    }

                    const taskElementId = "task-" + taskId;
                    const taskElement = document.getElementById(taskElementId);

                    if (taskElement) {
                        taskElement.remove();

                        // check if the recently removed task was the last one
                        const taskParentElement = document.getElementById('accordion');
                        if (taskParentElement.querySelectorAll('div').length === 1) {
                            // the only child div is the one hidden which contains the message for empty task list case
                            const noTasksElement = document.getElementById('no-tasks');
                            noTasksElement.style.display = 'block';
                        }
                    }

                    Swal.fire({
                        title: "Deleted",
                        text: "The task has been successfully deleted!",
                        icon: "success",
                        color: '#e4e0f3',
                        background: '#110f16'
                    })
                })
                .catch(
                    Swal.fire({
                        title: "Oops...",
                        text: "There was an error deleting the task!",
                        icon: "error",
                        color: '#e4e0f3',
                        background: '#110f16'
                    })
                )
        }
    });
}