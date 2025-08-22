(() => {
    const sessionCode = document.currentScript.dataset.sessionCode;

    const studySessionSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/study-session/'
        + sessionCode
        + '/'
    );

    studySessionSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        document.querySelector('#chat-log').value += (data.message + '\n');
    };

    studySessionSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function (e) {
        if (e.key === 'Enter') {
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function (e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        studySessionSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    };
})();

