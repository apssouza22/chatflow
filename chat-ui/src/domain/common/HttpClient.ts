interface RequestOptions {
    method?: "GET" | "POST" | "PATCH" | "DELETE";
    headers?: { [key: string]: string };
    body?: any;
}


export interface FetchResult<T> {
    data?: T,
    status: number,
    isLoading: boolean,
    error?: string
}

export class HttpClient {
    private readonly baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    async makeRequest<T>(url: string, options: RequestOptions): Promise<FetchResult<T>> {
        const result: FetchResult<T> = {
            isLoading: true,
            status: 200
        }
        // Remark: This 
        const hasFiles = Object.values(options.body).some((v: any) => Array.isArray(v) && v[0] instanceof Blob); // `File` is derived from `Blob`.
        const body = undefined;
        if (hasFiles) {
            const formData = new FormData();
            for (const [key, value] of Object.entries(options.body)) {
                if (Array.isArray(value)) { // Usually, it's an array of files, because a single file dialog may harvest multiple files.
                    for (const subvalue of value) { // so, `subvalue` is a `File` object, usually.
                        formData.append(key, subvalue as string | Blob); // TODO: Is it a `string | Blob` for sure?
                    }
                } else {
                    formData.append(key, value as string | Blob); // TODO: Is it a `string | Blob` for sure?
                }
            }
        }
        try {
            let params = {
                method: options.method || "GET",
                headers: {
                    "Content-Type": "application/json",
                    ...options.headers,
                },
                body: body ?? JSON.stringify(options.body);
            };
            if (params.method === "GET") {
                delete params.body;
            }
            const response = await fetch(`${this.baseUrl}${url}`, params);

            result.data = await response.json();
            result.status = response.status;

            if (!response.ok) {
                result.error = response.statusText
                return result;
            }
            return result;
        } catch (err: any) {
            console.log("fetch error", err)
            result.status = 500;
            result.error = err.message || "An error occurred"
            return result;
        }
    }

    async get<T>(url: string, headers?: { [key: string]: string }): Promise<FetchResult<T>> {
        return await this.makeRequest<T>(url, {method: "GET", headers});
    }

    async post<T>(url: string, data: any, headers?: { [key: string]: string }): Promise<FetchResult<T>> {
        return await this.makeRequest<T>(url, {method: "POST", body: data, headers});
    }

    async patch<T>(url: string, data: any, headers?: { [key: string]: string }): Promise<FetchResult<T>> {
        return await this.makeRequest<T>(url, {method: "PATCH", body: data, headers});
    }

    async remove<T>(url: string, headers?: { [key: string]: string }): Promise<FetchResult<T>> {
        return await this.makeRequest<T>(url, {method: "DELETE", headers});
    }
}
