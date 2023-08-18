interface SessionData {
    token: string;
    user: string;
    app: string;
    isPluginMode: boolean;
    appColor: string;
}

export class SessionManager {
    private static instance: SessionManager;
    private sessionData: SessionData;

    private constructor() {
        const params = this.loadSessionDataFromUrl()
        this.sessionData = {
            token: params["token"] || "",
            user: params["user"] || "",
            app: params["app"] || "chat",
            isPluginMode: params["pluginMode"]=="true" || false,
            appColor: params["appColor"] || "black"
        }
        console.log("session data", this.sessionData)
    }

    public static getInstance(): SessionManager {
        if (!SessionManager.instance) {
            SessionManager.instance = new SessionManager();
        }

        return SessionManager.instance;
    }

    public setAppKey(appKey: string) {
        this.sessionData.app = appKey;
    }

    public setToken(token: string) {
        this.sessionData.token = token;
    }

    public getSessionData(): SessionData {
        return {...this.sessionData};
    }

    private loadSessionDataFromUrl() {
        const strParams = window.location.href.split("?")
        if (strParams.length < 2) {
            return {}
        }
        return strParams[1].split("&")
            .map(i => {
                const kv = i.split("=")
                if (kv.length < 2) {
                    return {}
                }
                const r = {}
                r[kv[0]] = kv[1]
                return r
            })
            .reduce((acc, curr) => {
                return {...acc, ...curr}
            })
    }

    setUser(email: string) {
        this.sessionData.user = email;
    }
}
