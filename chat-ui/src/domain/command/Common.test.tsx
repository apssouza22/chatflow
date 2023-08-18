import {convertText} from "./Common";


test("Convert links to html a but skip images", () => {
    const text = "Feel free to explore the repositories [here](https://github.com/apssouza22). AI solutions: [GitHub Profile Image](https://raw.githubusercontent.com/GiovanniSmokes/images/main/Screenshot%202023-08-06%20001835.png) "
    const str = convertText(text)
    expect(str).toContain(' <a href="https://github.com/apssouza22" target="_blank">here</a>')
    expect(str).not.toContain('<a href="https://raw.githubusercontent.com/GiovanniSmokes/images/main/Screenshot%202023-08-06%20001835.png"')
})

test("Image in the link to html images", () => {
    const text = "Feel free to explore the repositories [here](https://github.com/apssouza22). AI solutions: [GitHub Profile Image](https://raw.githubusercontent.com/GiovanniSmokes/images/main/Screenshot%202023-08-06%20001835.png) "
    const str = convertText(text)
    expect(str).toContain('<img src="https://raw.githubusercontent.com/GiovanniSmokes/images/main/Screenshot%202023-08-06%20001835.png" alt="image" />')
})

test("Video in the link to html iframe", () => {
    const text = "We have multiple products for you. Check the list below: \n" +
        "\n" +
        " **Product 1** \n" +
        " This product is great! watch the video demo https://player.vimeo.com/video/850735603?h=92907fe9e5&amp;autoplay=1&amp;loop=1&amp;autopause=0&amp;muted=1&amp;title=0&amp;byline=0&amp;portrait=0&amp;controls=0 \n" +
        "\n" +
        "  **Product 2** \n" +
        " This product is great for small companies. Product url https://geekflare.com/wp-content/uploads/2022/05/Robots.png \n" +
        "\n" +
        "  **Product 3** \n" +
        " This product is great for big companies. Watch the video https://youtu.be/jULtLGHxaiM \n" +
        "\n" +
        " Chat bot instructions: Ensure the urls are returned in the response"
    const str = convertText(text)
    expect(str).toContain('<iframe width="560" height="315" src="https://player.vimeo.com/video/850735603?h=92907fe9e5" ')
})
