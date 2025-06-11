from playwright.sync_api import sync_playwright
import time

COOKIES_FILE = "tiktok_cookies.json"
MUSIC_URL = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en"

def parse_song_list_from_spans(spans, max_items=100):
    results = []
    current = {}
    for s in spans:
        text = s.inner_text().strip()
        if text.isdigit() and 1 <= int(text) <= 100:
            if current:
                if 'rank' in current and 'title' in current and 'artist' in current:
                    results.append(current)
                current = {}
            current['rank'] = int(text)
        elif text and not text.isdigit() and \
            all(x not in text for x in ["See analytics", "Approved for business use", "Posts"]):
            if 'title' not in current:
                current['title'] = text
            elif 'artist' not in current:
                current['artist'] = text
        if len(results) >= max_items:
            break
    if current and 'rank' in current and 'title' in current and 'artist' in current:
        results.append(current)
    return results[:max_items]

def scrape_popular_and_breakout_music(max_items=100):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context(storage_state=COOKIES_FILE)
        page = ctx.new_page()
        page.goto(MUSIC_URL, wait_until="networkidle")
        time.sleep(2)

        popular_tab = page.query_selector("span:has-text('Popular')")
        if popular_tab:
            popular_tab.click()
            print("✅ Popular 탭 정보 수집 중...")
            time.sleep(2)
        else:
            print("❌ Popular 탭을 찾지 못했습니다.")

        for _ in range(8):
            page.mouse.wheel(0, 2500)
            time.sleep(1)
            
        spans = page.query_selector_all("span")
        popular_results = parse_song_list_from_spans(spans, max_items=max_items)

        breakout_tab = page.query_selector("span:has-text('Breakout')")
        if breakout_tab:
            breakout_tab.click()
            print("✅ Breakout 탭 정보 수집 중...")
            time.sleep(2.5)

            for _ in range(8):
                page.mouse.wheel(0, 2500)
                time.sleep(1)
            spans = page.query_selector_all("span")
            breakout_results = parse_song_list_from_spans(spans, max_items=max_items)
        else:
            print("❌ Breakout 탭을 찾지 못했습니다.")
            breakout_results = []

        browser.close()
        return popular_results, breakout_results

if __name__ == "__main__":
    popular, breakout = scrape_popular_and_breakout_music(100)
    print("\n[Popular 탭 Top Songs]")
    if not popular:
        print("❌ 데이터를 가져오지 못했습니다.")
    else:
        print(f"{'순위':<5} {'곡명':<40} {'아티스트':<20}")
        for m in popular:
            print(f"{m['rank']:<5} {m['title']:<40} {m['artist']:<20}")
    print("\n[Breakout 탭 Top Songs]")
    if not breakout:
        print("❌ 데이터를 가져오지 못했습니다.")
    else:
        print(f"{'순위':<5} {'곡명':<40} {'아티스트':<20}")
        for m in breakout:
            print(f"{m['rank']:<5} {m['title']:<40} {m['artist']:<20}")
