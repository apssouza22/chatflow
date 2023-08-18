const apiUrl = "http://localhost:8880/api/v1"

const login = async (email, app_key) => {
    const endpoint = `/user/${email}/app/${app_key}/auth`
    const resp = await makeRequest(`${endpoint}`, {
        method: "GET",
    })

    if (resp.status !== 200 || resp.data?.access_token == null) {
        alert("Login failed")
        return
    }
    sessionStorage.setItem("token", resp.data.access_token);
    return resp.data.access_token
};

async function makeRequest(url, options) {
    const result = {}
    try {
        let params = {
            method: options.method || "GET",
            headers: {
                "Content-Type": "application/json",
                ...options.headers,
            },
            body: JSON.stringify(options.body),
        };
        if (params.method === "GET") {
            delete params.body;
        }
        const response = await fetch(`${url}`, params);

        result.data = await response.json();
        result.status = response.status;

        if (!response.ok) {
            result.error = {
                status: response.status,
                statusText: response.statusText
            }
            return result;
        }
        return result;
    } catch (err) {
        console.log("error", err)
        result.error = {
            status: 500,
            statusText: err.message || "An error occurred"
        }
        return result;
    }
}

export function toElement(html) {
    let template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}


function addChatbotButton() {

    const chatBtn = `
    <div class="intercom-lightweight-app-launcher intercom-launcher" role="button" tabindex="0" aria-label="Open Intercom Messenger" aria-live="polite">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 28 32"><path d="M28 32s-4.714-1.855-8.527-3.34H3.437C1.54 28.66 0 27.026 0 25.013V3.644C0 1.633 1.54 0 3.437 0h21.125c1.898 0 3.437 1.632 3.437 3.645v18.404H28V32zm-4.139-11.982a.88.88 0 00-1.292-.105c-.03.026-3.015 2.681-8.57 2.681-5.486 0-8.517-2.636-8.571-2.684a.88.88 0 00-1.29.107 1.01 1.01 0 00-.219.708.992.992 0 00.318.664c.142.128 3.537 3.15 9.762 3.15 6.226 0 9.621-3.022 9.763-3.15a.992.992 0 00.317-.664 1.01 1.01 0 00-.218-.707z"></path>
            </svg>
    </div>`
    const button = toElement(chatBtn)

    button.id = 'btn-chatbot-open';

    // Add an event listener to show the chatbot
    button.addEventListener('click', function () {
        const chatbotC = document.querySelector('#chatbot-iframe-container');
        if (chatbotC.style.display === 'flex') {
            chatbotC.style.display = 'none';
            return;
        }
        chatbotC.style.display = 'flex';
    });
    document.body.appendChild(button);
}

function createChat(token, user, appId, color, appURL) {
    const params = "pluginMode=true&token=" + token + "&user=" + user + "&app=" + appId + "&appColor=" + color
    const chatbotContainer = document.createElement("iframe");
    chatbotContainer.id = "chatbot-iframe-container";
    chatbotContainer.src = appURL + "index.html/#/chatbot?" + params;
    document.body.appendChild(chatbotContainer);
}

function addStyle() {
    const style = document.createElement('style');

// Set the CSS rules for the <style> element
    const css = `
    
#chatbot-iframe-container {
    display: block;
    font-family: 'Roboto', sans-serif;
    font-size: 12px;
    color: #444;
    width: 30%;
    height: 70%;
    border: 1px solid #ccc;
    border-radius: 25px 25px 15px 15px;
    overflow: hidden;
    flex-direction: column;
    position: fixed;
    bottom: 80px;
    right: 20px;
    background: white;
    z-index: 10001;
    box-shadow: rgba(0, 0, 0, 0.16) 0px 5px 40px;
}

@media screen and (max-width: 768px) {
  #chatbot-iframe-container {
    width: 100%;
    height: 100%;
    bottom: 0;
    right: 0;
    border-radius: 0;
  }
}

.intercom-lightweight-app-launcher {
    position: fixed;
    z-index: 1000;
    border: none;
    bottom: 20px;
    right: 20px;
    max-width: 48px;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    box-sizing: content-box;
    background: white;
    padding: 8px;
}

.intercom-lightweight-app-launcher svg{
    height: 40px;
}

.intercom-lightweight-app-launcher:hover {
    transition: transform 250ms cubic-bezier(0.33, 0.00, 0.00, 1.00);
    transform: scale(1.1);
}
.intercom-lightweight-app-launcher-icon {
    align-items: center;
    justify-content: center;
    position: absolute;
    top: 0;
    left: 0;
    width: 48px;
    height: 48px;
    transition: transform 100ms linear, opacity 80ms linear;
    background: white;
}
`;

    style.textContent = css;
    document.head.appendChild(style);
}

(async function () {
    console.log("Run chatbot plugin");
    const token = await login(CHATBOT_EMAIL, APP_KEY)
    let color = "";
    let appUrl = "https://apps.newaisolutions.com/assets/";

    try {
        color = APP_COLOR
    } catch (e) {
    }
    try {
        appUrl = APP_URL
    } catch (e) {
    }

    createChat(token, CHATBOT_EMAIL, APP_KEY, color, appUrl)
    addStyle();
    addChatbotButton();
}());
