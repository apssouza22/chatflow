export function parseUrlParams(url: string) {
    const params = {};
    if (!url) {
        return params;
    }
    const urlParts = url.split('?');
    if (urlParts.length > 1) {
        const queryParams = urlParts[1].split('&');
        for (let i = 0; i < queryParams.length; i++) {
            const param = queryParams[i].split('=');
            const paramName = decodeURIComponent(param[0]);
            const paramValue = decodeURIComponent(param[1]).replace(/\+/g, ' ');
            if (paramName.length > 0) {
                params[paramName] = paramValue;
            }
        }
    }
    return params;
}
