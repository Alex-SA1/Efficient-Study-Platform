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

    document.getElementById('loadMoreBtn').addEventListener('click', (event) => {
        const nextMessagesPage = event.target.dataset.nextMessagesPage;
        const studySessionUrl = event.target.dataset.studySessionUrl;
        const nextMessagesPageQueryUrl = studySessionUrl + "?messages-page=" + nextMessagesPage;

        fetch(nextMessagesPageQueryUrl, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                const parentElement = document.getElementById('messages');
                const firstChildElement = parentElement.firstChild;

                for (let messageIndex = 0; messageIndex < data.messages.length; messageIndex++) {
                    const message = data.messages[messageIndex];

                    const messageSenderElement = document.createElement('p');
                    messageSenderElement.textContent = "message sent by: " + message.sender;


                    const messageContentElement = document.createElement('p');
                    messageContentElement.textContent = "message: " + message.message_content;

                    const breakLine = document.createElement('hr');

                    parentElement.insertBefore(messageSenderElement, firstChildElement);

                    parentElement.insertBefore(messageContentElement, firstChildElement);

                    parentElement.insertBefore(breakLine, firstChildElement);
                }

                if (data.has_next_messages_page) {
                    event.target.dataset.nextMessagesPage = data.next_messages_page;
                } else {
                    event.target.remove();
                }
            });
    });
})();

