function sendFriendRequest(receiver_username) {
    const csrfToken = document.getElementById('search-users-page-main-script').dataset.csrfToken;
    const sendFriendRequestUrl = document.getElementById('search-users-page-main-script').dataset.sendFriendRequestUrl;

    fetch(sendFriendRequestUrl, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            'receiver_username': receiver_username
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                Swal.fire({
                    icon: "error",
                    title: "Oops...",
                    text: data.error,
                    color: '#e4e0f3',
                    background: '#110f16',
                    showConfirmButton: false,
                    timer: 2500,
                });

                return;
            }

            Swal.fire({
                icon: "success",
                title: "The friend request was sent successfully!",
                showConfirmButton: false,
                timer: 2200,
                color: '#e4e0f3',
                background: '#110f16'
            });
        })
        .catch(err => {
            Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "There was an error sending the friend request!",
                color: '#e4e0f3',
                background: '#110f16',
                showConfirmButton: false,
                timer: 2500,
            });
        });
}