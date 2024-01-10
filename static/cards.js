export function createCard() {
    let cardDiv = document.createElement('div');
    cardDiv.classList.add('card', 'border', 'border-dark', 'rounded-3', "mb-4");

    let cardBodyDiv = document.createElement('div');
    cardBodyDiv.classList.add('card-body', "pl-4");

    cardDiv.appendChild(cardBodyDiv);
    return cardDiv;
}

export function createServerCardBody() {
    let serverCard = createCard();
    let serverCardBody = serverCard.querySelector('.card-body');
    serverCardBody.classList.add('server-message', 'text-start');

    return serverCardBody;
}

export function createClientCardBody(message) {
    let clientCard = createCard();
    let clientCardBody = clientCard.querySelector('.card-body');
    clientCardBody.textContent = message;
    clientCardBody.classList.add('client-message', 'bg-dark', 'text-white');

    return clientCardBody;
}

export function createCurrentOutput() {
    let currentOutput = document.createElement('div');
    currentOutput.classList.add('output');

    return currentOutput;
}
