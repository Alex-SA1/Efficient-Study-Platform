function format_datetime(datetime) {
    const [date, time] = datetime.split("T")
    const [year, month, day] = date.split("-").map(Number)
    const [hourString, minutesString, secondsExtended] = time.split(":")
    const [secondsString, fractionalSeconds_timezone] = secondsExtended.split(".")

    const hour = Number(hourString)
    const minutes = Number(minutesString)
    const seconds = Number(secondsString)

    const months = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }

    const formatted_datetime = `${day} ${months[month]} ${hour}:${minutes}`;
    return formatted_datetime;
}

function createMessageHeader(datetime, sender) {
    const username = document.getElementById('study-session-main-script').dataset.username;

    const messageHeader = document.createElement('div');
    messageHeader.classList = "d-flex justify-content-between";

    const messageDatetimeElement = document.createElement('p');
    messageDatetimeElement.classList = "datetime small mb-1";
    messageDatetimeElement.textContent = datetime;

    const messageSenderElement = document.createElement('p');
    messageSenderElement.classList = "username small mb-1"
    messageSenderElement.textContent = sender;

    if (sender === username) {
        messageHeader.appendChild(messageDatetimeElement);
        messageHeader.appendChild(messageSenderElement);
    }
    else {
        messageHeader.appendChild(messageSenderElement);
        messageHeader.appendChild(messageDatetimeElement);
    }

    return messageHeader;
}

function createMessageBody(message_content, sender, profile_picture_url) {
    const username = document.getElementById('study-session-main-script').dataset.username;

    const messageBody = document.createElement('div');
    messageBody.classList = "d-flex flex-row mb-4 pt-1 ";

    if (sender === username) {
        messageBody.classList += "justify-content-end";
    }
    else {
        messageBody.classList += "justify-content-start";
    }

    const messageContentElement = document.createElement('p');
    messageContentElement.classList = "small p-2 mb-3 rounded-3 ";
    messageContentElement.textContent = message_content;

    if (sender === username) {
        messageContentElement.classList += "me-3 user-message ";
    }
    else {
        messageContentElement.classList += "ms-3 others-message ";
    }

    const messageContentSection = document.createElement('div');
    messageContentSection.appendChild(messageContentElement);

    const messageImageElement = document.createElement('img');
    messageImageElement.src = profile_picture_url;
    messageImageElement.classList = "rounded-circle";
    messageImageElement.style.width = "45px";
    messageImageElement.style.height = "100%";

    if (sender === username) {
        messageBody.appendChild(messageContentSection);
        messageBody.appendChild(messageImageElement);
    }
    else {
        messageBody.appendChild(messageImageElement);
        messageBody.appendChild(messageContentSection);
    }

    return messageBody;
}

function setChatBoxScrollbarToBottom() {
    const chatBoxElement = document.getElementById('chatBox');
    chatBoxElement.scrollTop = chatBoxElement.scrollHeight;
}

function copyToClipboard() {
    const textElement = document.querySelector('.form-control.session-code');
    navigator.clipboard.writeText(textElement.value);
}

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

        const chatBoxElement = document.getElementById('chatBox');

        const formatted_datetime = format_datetime(data.datetime);
        const messageHeader = createMessageHeader(formatted_datetime, data.sender);
        const messageBody = createMessageBody(data.message, data.sender, data.profile_picture_url);

        chatBoxElement.appendChild(messageHeader);
        chatBoxElement.appendChild(messageBody);

        setChatBoxScrollbarToBottom();
    };

    studySessionSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').onkeyup = function (e) {
        if (e.key === 'Enter') {
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function (e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        const profilePictureUrl = JSON.parse(
            document.getElementById('profile-picture-url').textContent
        );

        studySessionSocket.send(JSON.stringify({
            'message': message,
            'profile_picture_url': profilePictureUrl
        }));

        messageInputDom.value = '';
    };

    setChatBoxScrollbarToBottom();

    const loadMoreBtnElement = document.getElementById('loadMoreBtn');
    if (loadMoreBtnElement !== null) {
        loadMoreBtnElement.addEventListener('click', (event) => {
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
                    const chatBoxElement = document.getElementById('chatBox');
                    const lastChatBoxMessage = chatBoxElement.firstChild.nextSibling.nextSibling.nextSibling;

                    for (let messageIndex = 0; messageIndex < data.messages.length; messageIndex++) {
                        const message = data.messages[messageIndex];

                        const messageHeader = createMessageHeader(message.datetime, message.sender);
                        const messageBody = createMessageBody(message.message_content, message.sender, message.profile_picture_url);

                        chatBoxElement.insertBefore(messageHeader, lastChatBoxMessage);

                        chatBoxElement.insertBefore(messageBody, lastChatBoxMessage);

                    }

                    if (data.has_next_messages_page) {
                        event.target.dataset.nextMessagesPage = data.next_messages_page;
                    } else {
                        event.target.remove();
                    }
                });
        });
    }
})();

