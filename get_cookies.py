from playwright.sync_api import sync_playwright

def get_cookies(url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        cookies = page.context.cookies()
        browser.close()
        return cookies

def set_cookies(url, cookies):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        for cookie in cookies:
            page.context.add_cookies(cookie)
        browser.close()

