async function createStudySession() {
    const mainScript = document.getElementById('collaborative-study-session-menu-page-main-script');
    const generateStudySessionCodeFetchUrl = mainScript.dataset.generateStudySessionCodeUrl;
    const csrfToken = mainScript.dataset.csrfToken;
    const collaborativeStudySessionMenuUrl = mainScript.dataset.collaborativeStudySessionMenuUrl;

    try {
        const response = await fetch(generateStudySessionCodeFetchUrl, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({})
        });

        const data = await response.json();
        const sessionCode = data.study_session_code;

        const studySessionUrl = collaborativeStudySessionMenuUrl + "study-session/" + sessionCode;

        window.location.href = studySessionUrl
    }
    catch (error) {
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "There was an error generating the session code!",
            color: '#e4e0f3',
            background: '#110f16',
            showConfirmButton: false,
            timer: 2500,
        })

        return;
    }
}

function joinStudySession() {
    const mainScript = document.getElementById('collaborative-study-session-menu-page-main-script');
    const collaborativeStudySessionMenuUrl = mainScript.dataset.collaborativeStudySessionMenuUrl;
    const sessionCode = document.getElementById('sessionCode').value;

    const studySessionUrl = collaborativeStudySessionMenuUrl + "study-session/" + sessionCode;

    window.location.href = studySessionUrl;
}