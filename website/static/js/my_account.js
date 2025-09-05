function acceptFriendRequest(sender_username) {
    const manageFriendRequestUrl = document.getElementById('my-account-page-main-script').dataset.manageFriendRequestUrl;
    const csrfToken = document.getElementById('my-account-page-main-script').dataset.csrfToken;

    fetch(manageFriendRequestUrl, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            'action': 'accept',
            'sender_username': sender_username
        })
    })
        .then(response => response.json)
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
                title: "The friend request was accepted successfully!",
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
                text: "There was an error accepting the friend request!",
                color: '#e4e0f3',
                background: '#110f16',
                showConfirmButton: false,
                timer: 2500,
            });
        });
}

function rejectFriendRequest(sender_username) {
    const manageFriendRequestUrl = document.getElementById('my-account-page-main-script').dataset.manageFriendRequestUrl;
    const csrfToken = document.getElementById('my-account-page-main-script').dataset.csrfToken;

    fetch(manageFriendRequestUrl, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            'action': 'reject',
            'sender_username': sender_username
        })
    })
        .then(response => response.json)
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
                title: "The friend request was rejected successfully!",
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
                text: "There was an error rejecting the friend request!",
                color: '#e4e0f3',
                background: '#110f16',
                showConfirmButton: false,
                timer: 2500,
            });
        });
}

(() => {
    const editAcccountBtn = document.getElementById('editAccountBtn');
    editAcccountBtn.addEventListener('click', () => {
        window.location.href = editAcccountBtn.dataset.editAccountUrl;
    })
})();