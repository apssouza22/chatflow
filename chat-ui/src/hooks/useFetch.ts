import {useState} from "react";

interface RequestOptions {
    method?: "GET" | "POST" | "PATCH" | "DELETE";
    headers?: { [key: string]: string };
    body?: any;
    credentials?: "include" | "omit" | "same-origin",
}

interface UseFetchError {
    status: number,
    statusText: string
}

export interface FetchResult<T> {
    data?: T,
    status: number,
    isLoading: boolean,
    error?: UseFetchError
}

interface UseRestAPI {
    loading: boolean;
    get: <T>(url: string, headers?: { [key: string]: string }) => Promise<FetchResult<T>>;
    post: <T>(url: string, data: any, headers?: { [key: string]: string }) => Promise<FetchResult<T>>;
    patch: <T>(url: string, data: any, headers?: { [key: string]: string }) => Promise<FetchResult<T>>;
    remove: <T>(url: string, headers?: { [key: string]: string }) => Promise<FetchResult<T>>;
    makeRequest: <T>(url: string, options: RequestOptions) => Promise<FetchResult<T>>;
}

type UseRestAPIOptions = {
    beforeRequest?: (params: any) => void,
    afterRequest?: (response: Response) => void,
};

export const useRestAPI = (baseUrl: string, apiOptions?: UseRestAPIOptions): UseRestAPI => {
    const [loading, setLoading] = useState<boolean>(false);

    const makeRequest = async <T>(url: string, options: RequestOptions = {}): Promise<FetchResult<T>> => {
        const result: FetchResult<T> = {
            isLoading: true,
            status: 200
        }
        try {
            setLoading(true);
            const params = {
                method: options.method || "GET",
                headers: {
                    "Content-Type": "application/json",
                    ...options.headers,
                },
                body: JSON.stringify(options.body),
                credentials: options.credentials,
            };
            if (apiOptions !== undefined && apiOptions.beforeRequest !== undefined) {
                apiOptions.beforeRequest(params);
            }
            if (params.method === "GET") {
                delete params.body;
            }
            const response = await fetch(`${baseUrl}${url}`, params);
            if (apiOptions !== undefined && apiOptions.afterRequest !== undefined) {
                apiOptions.afterRequest(response);
            }

            const responseData = await response.json();
            result.data = responseData;
            result.status = response.status;

            if (!response.ok) {
                result.error = {
                    status: response.status,
                    statusText: response.statusText
                }
                return result;
            }
            return result;
        } catch (err: any) {
            console.log("error", err)
            result.error = {
                status: 500,
                statusText: err.message || "An error occurred"
            }
            return result;
        } finally {
            setLoading(false);
        }
    };

    const get = async <T>(url: string, headers?: { [key: string]: string }): Promise<FetchResult<T>> => {
        return await makeRequest<T>(url, {method: "GET", headers});
    };

    const post = async <T>(url: string, data: any, headers?: { [key: string]: string }): Promise<FetchResult<T>> => {
        return await makeRequest<T>(url, {method: "POST", body: data, headers});
    };

    const patch = async <T>(url: string, data: any, headers?: { [key: string]: string }): Promise<FetchResult<T>> => {
        return await makeRequest<T>(url, {method: "PATCH", body: data, headers});
    };

    const remove = async <T>(url: string, headers?: { [key: string]: string }): Promise<FetchResult<T>> => {
        return await makeRequest<T>(url, {method: "DELETE", headers});
    };

    return {
        loading,
        get,
        post,
        patch,
        remove,
        makeRequest
    };
};

export const useOurRestAPI = (baseUrl: string): UseRestAPI => {
    const baseRestAPI = useRestAPI(baseUrl); // used to prolong token

    const secondsBeforeReauth = 5; // TODO: Can we assume that client's clock is correct?
    // TODO: Reirect to login page if token is expired.
    if ((parseInt(localStorage.getItem("exp") ?? '0') + secondsBeforeReauth) * 1000 > new Date().getTime()) {
        // Prolong the session:
        baseRestAPI.post("/auth/refresh", {}).then((result) => {
            if (result.status === 200) {
                localStorage.setItem("token", (result.data! as any).token);
                localStorage.setItem("exp", (result.data! as any).exp);
            } else {
                // TODO: Handle error.
            }
        });
    }
    const beforeRequest = (params: any) => {
        params.headers = {
            ...params.headers,
            // TODO: It was before done with `SessionManager.getInstance().getSessionData().token` - does it has any advantage?
            'Authorization': 'Bearer ' + localStorage.getItem("token"),
        };
    };
    return useRestAPI(baseUrl, {beforeRequest});
}