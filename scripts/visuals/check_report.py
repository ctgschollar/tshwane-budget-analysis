"""Open report.html in headless Chrome: count rendered Plotly charts, exercise the Sankey buttons, screenshot desktop + phone."""
import sys
from playwright.sync_api import sync_playwright

URL = sys.argv[2] if len(sys.argv) > 2 else "file://" + __import__("os").path.expanduser("~/Documents/tshwane/output/visuals/report.html")
OUT = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1280, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(URL)
    pg.wait_for_timeout(2500)
    n = pg.evaluate("document.querySelectorAll('.js-plotly-plot').length")
    svgs = pg.evaluate("[...document.querySelectorAll('.js-plotly-plot')].map(d => d.querySelectorAll('.main-svg').length)")
    print("plotly charts:", n, "svg layers per chart:", svgs, "errors:", errs)
    # Sankey selector
    sk = pg.locator("#sankey .js-plotly-plot")
    for lab in ("2023/24 – Brink (DA)", "2024/25 – Brink (DA)", "2025/26 – Moya (ActionSA)"):
        btn = pg.locator("#sankey g.updatemenu-button", has_text=lab)
        btn.click()
        pg.wait_for_timeout(700)
        vis = pg.evaluate("document.querySelector('#sankey .js-plotly-plot').data.map(t => t.visible)")
        title = pg.evaluate("document.querySelector('#sankey .js-plotly-plot').layout.title.text.split('<br>')[0]")
        tot = pg.evaluate("document.querySelector('#sankey .js-plotly-plot').querySelectorAll('.sankey-node').length")
        print(f"clicked {lab!r}: visible={vis} title={title!r} nodes drawn={tot}")
        sk.screenshot(path=f"{OUT}/sankey_{lab[:7].replace('/', '-')}.png")
    pg.screenshot(path=f"{OUT}/report_desktop.png", full_page=True)
    ph = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    ph.goto(URL)
    ph.wait_for_timeout(2500)
    ph.screenshot(path=f"{OUT}/report_phone.png", full_page=True)
    print("phone page height:", ph.evaluate("document.body.scrollHeight"), "horizontal overflow:",
          ph.evaluate("document.documentElement.scrollWidth > window.innerWidth"))
    b.close()
