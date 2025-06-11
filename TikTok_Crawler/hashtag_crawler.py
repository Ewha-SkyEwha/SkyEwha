from playwright.sync_api import sync_playwright
import re
import time
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

COOKIES_FILE = "tiktok_cookies.json"
HASHTAG_URL = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en"

def scrape_travel_hashtags_fixed():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context(storage_state=COOKIES_FILE)
        page = ctx.new_page()
        page.goto(HASHTAG_URL, wait_until="networkidle")
        time.sleep(1)

        btn = page.query_selector("button:has-text('Industry')") \
            or page.query_selector("span:has-text('Industry')")
        if btn:
            btn.click()
            time.sleep(1)

        for _ in range(15):
            t = page.query_selector("li:has-text('Travel')") \
                or page.query_selector("span:has-text('Travel')") \
                or page.query_selector("div:has-text('Travel')")
            if t and t.is_visible():
                t.scroll_into_view_if_needed()
                t.click()
                break
            page.keyboard.press("ArrowDown")
            time.sleep(0.2)
        time.sleep(2)

        for _ in range(12):
            page.mouse.wheel(0, 2150)
            time.sleep(0.5)
        time.sleep(1)

        lines = [l.strip() for l in page.inner_text("body").splitlines() if l.strip()]
        browser.close()

    results = []
    i = 0
    found_first = False
    while i < len(lines) - 4:
        if not found_first:
            if (
                re.match(r"^\d+$", lines[i])
                and lines[i+1].startswith("#")
                and lines[i+2] == "Travel"
                and re.match(r"^[0-9,.]+[KMB]?$", lines[i+3])
                and lines[i+4] == "Posts"
            ):
                results.append((lines[i+1], lines[i+3]))
                found_first = True

                i += 5

                while i < len(lines) and (
                    lines[i] in [
                        "See analytics",
                        "Access detail page for more insights of the trend",
                        "Got it"
                    ]
                ):
                    i += 1
                continue
            else:
                i += 1
                continue

        if (
            re.match(r"^\d+$", lines[i])
            and lines[i+1].startswith("#")
            and lines[i+2] == "Travel"
            and re.match(r"^[0-9,.]+[KMB]?$", lines[i+3])
            and lines[i+4] == "Posts"
        ):
            results.append((lines[i+1], lines[i+3]))
            i += 5
        else:
            i += 1

    return results

def cluster_hashtags(results, k=7):
    hashtags = [tag.lstrip("#") for tag, _ in results]
    posts = [cnt for _, cnt in results]

    n_samples = len(hashtags)
    if n_samples == 0:
        print("❌ 해시태그가 하나도 없습니다. 크롤링 실패!")
        return
    if n_samples == 1:
        print("❗ 해시태그가 1개만 수집되었습니다. 클러스터링 불가.")
        print(f"# {hashtags[0]} ({posts[0]})")
        return
    if n_samples < k:
        k = n_samples
        print(f"⚠️ 데이터가 {n_samples}개라서 클러스터 수 k를 {k}로 조정합니다.")

    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    embeddings = model.encode(hashtags)

    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    df = pd.DataFrame({
        "hashtag": hashtags,
        "posts": posts,
        "cluster": labels,
    })

    print(f"{'순위':<4} {'해시태그':<20} 게시글수   클러스터")
    for idx, row in df.iterrows():
        print(f"{idx+1:<4} #{row['hashtag']:<19} {row['posts']:<10} {row['cluster']}")

    for i in range(k):
        print(f"\n[클러스터 {i}]")
        print(df[df.cluster == i][["hashtag", "posts"]])

    # CSV 및 엑셀로 저장
    df.to_csv("travel_hashtags_clustered.csv", index=False, encoding="utf-8-sig")
    print("✅ travel_hashtags_clustered.csv 저장 완료!")

    return df

if __name__ == "__main__":
    import os
    if not os.path.exists(COOKIES_FILE):
        save_tiktok_cookies()
    results = scrape_travel_hashtags_fixed()
    print(f"🔎 크롤링된 해시태그 개수: {len(results)}개")
    if not results:
        print("❌ 해시태그 크롤링 실패! (쿠키 만료/페이지 변경 등)")
    else:
        cluster_hashtags(results)
