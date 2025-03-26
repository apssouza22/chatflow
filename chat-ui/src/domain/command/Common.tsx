import parse, {domToReact} from 'html-react-parser';
import {Link} from 'react-router-dom';
import * as React from "react";

export type RequestRender = {
    field_type: string;
    field_options?: Array<string>
}

enum ResponseRenderType {
    Chart = "chart",
    List = "list",
}

export enum CommandName {
    SEND_EMAIL = "send_email",
    API_CALL = "api_call",
    BROWSE_WEBSITE = "browse_website",
    CHAT_QUESTION = "chat_question",
    JAVASCRIPT = "js_func",
}

export type ResponseRenderDto = {
    render_type: ResponseRenderType
    fields?: Array<string>
}

export type Command = {
    name: string;
    args?: {
        headers: { [x: string]: string };
        url: string;
        method: any;
        data_request: any;
    };
    function?: {
        name: string;
        code: string;
        param: Map<string, string>;
    };
    request_render?: Record<string, RequestRender>
    response_render?: ResponseRenderDto
};

export type TaskCommand = {
    speak: string;
    dataUpdate: any;
    command: Command
    chat: string
}

function replaceMarkdownWithImageUrl(text: string): string {
    // Regular expression to find Markdown image links
    const pattern = /!\[.*?\]\((https?:\/\/[^\s]+?\.(?:jpg|jpeg|png|gif))\)/g;

    // Replace the Markdown link with the actual image URL
    return text.replace(pattern, (match, url) => url);
}

function markdownToHtmlLink(markdown: string): string {
    const regExpAllLinks = /[^!]\[([^[]+)\]\(([^)]+)\)/g;
    let regExpSingleLink = /[^!]\[([^[]+)\]\(([^)]+)\)/;
    let isImgUrlRegex = /\.(jpg|jpeg|png|gif)/;
    const isVideoUrlRegex = /youtube|vimeo|youtu\.be/;
    const matches = markdown.match(regExpAllLinks);
    matches?.forEach((match) => {
        const m = match.match(regExpSingleLink);
        if (m && m.length === 3) {
            const text = m[1];
            const url = m[2];
            if (isImgUrlRegex.test(url) || isVideoUrlRegex.test(url)) {
                markdown = markdown.replace(regExpSingleLink, " " + url);
                return;
            }
            const htmlLink = ` <a href="${url}" target="_blank">${text}</a>`;
            markdown = markdown.replace(regExpSingleLink, htmlLink);
        }
    })
    if (matches?.length > 0) {
        return markdown;
    }
    // const regex = /http(s)?:\/\/[^\s]+/g;
    // const matches2 = markdown.match(regex);
    // matches2?.forEach((match) => {
    //     if (!isImgUrlRegex.test(match) && !isVideoUrlRegex.test(match)) {
    //         const htmlLink = `<a href="${match}" target="_blank">${match}</a>`;
    //         markdown = markdown.replace(match, htmlLink);
    //     }
    // })
    return markdown
}

function replaceImageLinksWithImgTags(text: string): string {
    // Regular expression to find URLs ending with common image file extensions
    const pattern = /(https?:\/\/[^\s]+?\.(?:jpg|jpeg|png|gif))/g;

    // Replace the URL with an HTML <img> tag
    return text.replace(pattern, (match) => `<a href="${match}" class="nsbbox" data-lightbox="image-${match}"><img src="${match}" alt="image" /></a>`);
}

function replaceVideoLinksWithIframeTags(text: string): string {
    // YouTube URL to iframe
    text = text.replace(/(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?([^\s.]+)/g,
        '<a href="https://www.youtube.com/embed/$1" class="nsbbox" data-lightbox="video-$1"><img style="max-width:400px" src="http://img.youtube.com/vi/$1/maxresdefault.jpg" alt="YouTube video"></a>');

    // Vimeo URL to iframe
    text = text.replace(/(?:https?:\/\/)?(?:www\.)?(?:player\.)?vimeo\.com\/([^\s]+)/g,
        '<a href="https://player.vimeo.com/$1" class="nsbbox" data-lightbox="video-$1"><img style="max-width:400px" src="https://vumbnail.com/$1.jpg" alt="Vimeo video"></a>');
    return text;
}

function replaceMarkdownImageWithHtmlTag(text) {
    // Regular expression to find Markdown image notation
    const pattern = /!\[(.*?)\]\((https?:\/\/[^\s]+?\.(?:jpg|jpeg|png|gif))\)/g;

    // Replace the Markdown image notation with an HTML <img> tag
    return text.replace(pattern, (match, alt, url) => `<img src="${url}" alt="${alt}" />`);
}

function createImgTag(text: string): string {
    return replaceImageLinksWithImgTags(
        replaceMarkdownImageWithHtmlTag(
            replaceMarkdownWithImageUrl(text)
        )
    )
}

function markdownToHtmlBold(str: string) {
    return str.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
}

function markdownToHtmlSpan(str: string) {
    return str.replace(/`(.*?)`/g, '<span>$1</span>');
}

export function convertText(text: string) {
    return markdownToHtmlSpan(
        markdownToHtmlBold(
            replaceVideoLinksWithIframeTags(
                createImgTag(
                    markdownToHtmlLink(
                        text
                    )
                )
            )
        )
    );
}

export function formatText(text: string) {
    return toReact(
        convertText(text)
    );
}

function toReact(text: string): string | JSX.Element {
    const options = {
        replace: ({name, attribs, children}) => {
            if (name === 'a' && attribs.href) {
                if (attribs.href.endsWith('.')) {
                    attribs.href = attribs.href.slice(0, -1);
                }
                return <Link to={attribs.href} rel={attribs.rel} className={attribs.class === 'nsbbox' ? 'nsbbox' : undefined} data-lightbox={attribs['data-lightbox']} target={"_blank"} style={{
                    "color": "blue",
                }}>{domToReact(children)}</Link>;
            }
            if (name === 'b') {
                return <b>{domToReact(children)}</b>;
            }
            if (name === 'span') {
                return <span style={{"color": "#9a9a1a"}}>{domToReact(children)}</span>;
            }
            if (name === 'img' && attribs.src) {
                if (attribs.src.endsWith('.')) {
                    attribs.src = attribs.src.slice(0, -1);
                }
                return <img src={attribs.src} style={{"maxWidth": "90%", "margin": "10px auto"}} alt={"img"}/>;
            }
            if (name === 'iframe' && attribs.src) {
                if (attribs.src.endsWith('.')) {
                    attribs.src = attribs.src.slice(0, -1);
                }
                return <iframe {...attribs} style={{"maxWidth": "90%", "margin": "10px auto"}}/>
            }
        }
    };
    // @ts-ignore
    return parse(text, options);
}

export function setRenderInfo(renderInfoDto: ResponseRenderDto) {
    if (renderInfoDto == null) {
        return
    }
    localStorage.setItem("renderInfo", JSON.stringify(renderInfoDto))
}

export function getRenderInfo(): ResponseRenderDto {
    let item = localStorage.getItem("renderInfo");
    if (item == null) {
        return {render_type: ResponseRenderType.List}
    }
    return JSON.parse(item)
}

export function isRenderChart(): boolean {
    return getRenderInfo().render_type === ResponseRenderType.Chart;
}
