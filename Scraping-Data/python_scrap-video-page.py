import re, json, time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector


def scroll_page(url):
    service = Service(ChromeDriverManager().install())

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--lang=en')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    old_height = driver.execute_script("""
        function getHeight() {
            return document.querySelector('ytd-app').scrollHeight;
        }
        return getHeight();
    """)

    while True:
        driver.execute_script("window.scrollTo(0, document.querySelector('ytd-app').scrollHeight)")

        time.sleep(2)

        new_height = driver.execute_script("""
            function getHeight() {
                return document.querySelector('ytd-app').scrollHeight;
            }
            return getHeight();
        """)

        if new_height == old_height:
            break

        old_height = new_height

    selector = Selector(driver.page_source)
    driver.quit()

    return selector


def scrape_all_data(selector):
    youtube_video_page = []

    all_script_tags = selector.css('script').getall()

    title = selector.css(".title .ytd-video-primary-info-renderer::text").get()

    # https://regex101.com/r/gHeLwZ/1
    views = int(re.search(r"(.*)\s", selector.css(".view-count::text").get()).group().replace(",", ""))

    # https://regex101.com/r/9OGwJp/1
    likes = int(re.search(r"(.*)\s", selector.css("#top-level-buttons-computed > ytd-toggle-button-renderer:first-child #text::attr(aria-label)").get()).group().replace(",", ""))

    date = selector.css("#info-strings yt-formatted-string::text").get()

    duration = selector.css(".ytp-time-duration::text").get()

    # https://regex101.com/r/0JNma3/1
    keywords = "".join(re.findall(r'"keywords":\[(.*)\],"channelId":".*"', str(all_script_tags))).replace('\"', '').split(",")

    # https://regex101.com/r/9VhH1s/1
    thumbnail = re.findall(r'\[{"url":"(\S+)","width":\d*,"height":\d*},', str(all_script_tags))[0].split('",')[0]

    channel = {
        # https://regex101.com/r/xFUzq5/1
        "id": "".join(re.findall(r'"channelId":"(.*)","isOwnerViewing"', str(all_script_tags))),
        "name": selector.css("#channel-name a::text").get(),
        "link": f'https://www.youtube.com{selector.css("#channel-name a::attr(href)").get()}',
        "subscribers": selector.css("#owner-sub-count::text").get(),
        "thumbnail": selector.css("#img::attr(src)").get(),
    }
    
    description = selector.css(".ytd-expandable-video-description-body-renderer span:nth-child(1)::text").get()
    
    hash_tags = [
        {
            "name": hash_tag.css("::text").get(),
            "link": f'https://www.youtube.com{hash_tag.css("::attr(href)").get()}'
        }
        for hash_tag in selector.css(".ytd-expandable-video-description-body-renderer a")
    ]

    # https://regex101.com/r/onRk9j/1
    category = "".join(re.findall(r'"category":"(.*)","publishDate"', str(all_script_tags)))
    
    comments_amount = int(selector.css("#count .count-text span:nth-child(1)::text").get().replace(",", ""))

    comments = []

    for comment in selector.css("#contents > ytd-comment-thread-renderer"):
        comments.append({
            "author": comment.css("#author-text span::text").get().strip(),
            "link": f'https://www.youtube.com{comment.css("#author-text::attr(href)").get()}',
            "date": comment.css(".published-time-text a::text").get(),
            "likes": comment.css("#vote-count-middle::text").get().strip(),
            "comment": comment.css("#content-text::text").get(),
            "avatar": comment.css("#author-thumbnail #img::attr(src)").get(),
        })

    suggested_videos = []
    
    for video in selector.css("ytd-compact-video-renderer"):

        suggested_videos.append({
            "title": video.css("#video-title::text").get().strip(),
            "link": f'https://www.youtube.com{video.css("#thumbnail::attr(href)").get()}',
            "channel_name": video.css("#channel-name #text::text").get(),
            "date": video.css("#metadata-line span:nth-child(2)::text").get(),
            "views": video.css("#metadata-line span:nth-child(1)::text").get(),
            "duration": video.css("#overlays #text::text").get().strip(),
            "thumbnail": video.css("#thumbnail img::attr(src)").get(),
        })

    youtube_video_page.append({
    	"title": title,
    	"views": views,
    	"likes": likes,
    	"date": date,
    	"duration": duration,
        "channel": channel,
    	"keywords": keywords,
    	"thumbnail": thumbnail,
    	"description": description,
        "hash_tags": hash_tags,
        "category": category,
        "suggested_videos": suggested_videos,
    	"comments_amount": comments_amount,
    	"comments": comments,
    })

    print(json.dumps(youtube_video_page, indent=2, ensure_ascii=False))


def main():
    url = "https://www.youtube.com/watch?v=_BFgzaqyd8w&list=RDCLAK5uy_nMln2JPa-4fhqwquE3dRinwNr6IkN2-7k"
    result = scroll_page(url)
    scrape_all_data(result)


if __name__ == "__main__":
    main()