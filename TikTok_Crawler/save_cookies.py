from playwright.sync_api import sync_playwright

def save_tiktok_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://ads.tiktok.com/business/creativecenter/inspiration/popular/kr")
        page.pause()
        input("🔓 로그인 완료 후 Enter 키를 누르세요...")

        context.storage_state(path="tiktok_cookies.json")
        print("✅ tiktok_cookies.json 에 쿠키가 저장되었습니다!")

        browser.close()

if __name__ == "__main__":
    save_tiktok_cookies()
