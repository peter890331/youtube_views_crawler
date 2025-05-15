from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from tqdm import tqdm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import requests
import time
import os
from io import BytesIO
from selenium.webdriver.chrome.service import Service
import subprocess
import sys

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei"]
plt.rcParams["axes.unicode_minus"] = False

def get_channel_handle():
    print("-------------------------------------")
    print("歡迎使用 youtube_views_crawler！")
    print("-------------------------------------")
    while True:
        channel_handle = input("請輸入 YouTube 頻道 ID（例如：@peter0331）：")
        if not channel_handle:
            print("錯誤：頻道名稱不能為空，請重新輸入。")
        elif not channel_handle.startswith("@"):
            return "@" + channel_handle
        else:
            return channel_handle

channel_handle = get_channel_handle()
print(f"即將處理頻道：{channel_handle}")
print("-------------------------------------")
print(" * 啟動 Selenium")

original_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')

options = Options()
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')
options.add_argument("--use-fake-ui-for-media-stream")
options.add_argument("--use-fake-device-for-media-stream")
options.add_experimental_option("prefs", {"profile.default_content_setting_values.media_stream_camera": 2})
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument('--log-level=1')

# 避免 Chrome 輸出「DevTools listening」等冗餘日誌
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Service 隱藏 chromedriver.log
service = Service(log_path=os.devnull, pipe_output=True)

# Windows 系統下隱藏命令視窗 (可選)
if sys.platform.startswith('win'):
    service.creationflags = subprocess.CREATE_NO_WINDOW

driver = webdriver.Chrome(service=service, options=options)

sys.stdout.close()
sys.stdout = original_stdout

def check_error_page(driver):
    try:
        return "404 Not Found" in driver.title
    except:
        return False

def get_profile_picture_from_shorts():
    try:
        img_element = driver.find_element(By.CSS_SELECTOR, "img#avatar-section.yt-img-shadow")
        img_url = img_element.get_attribute("src")
    except:
        try:
            img_element = driver.find_element(By.CSS_SELECTOR, "img.yt-spec-avatar-shape__image")
            img_url = img_element.get_attribute("src")
        except:
            return None

    try:
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        return img
    except Exception:
        return None

def parse_view_count(view_text):
    view_text = view_text.replace("觀看次數：", "").replace("觀看次數", "").replace("次", "").strip()
    try:
        if "萬" in view_text:
            return float(view_text.replace("萬", "")) * 10000
        elif "億" in view_text:
            return float(view_text.replace("億", "")) * 100000000
        else:
            return float(view_text.replace(",", ""))
    except:
        raise ValueError("無法解析觀看次數")

# --- 抓長影片 ---
long_url = f"https://www.youtube.com/{channel_handle}/videos"
print(f"載入長影片頁面：{long_url}")
driver.get(long_url)
time.sleep(2)

if check_error_page(driver):
    print("錯誤：無法瀏覽該頻道頁面，請檢查頻道名稱是否正確。")
    driver.quit()
    print(" * 關閉 Selenium")
    print("-------------------------------------")
    input("按 Enter 鍵退出...")
    exit()

print("正在自動滾動載入長影片資料...")
scroll_pause_time = 0.5
last_height = driver.execute_script("return document.documentElement.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(scroll_pause_time)
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

videos = driver.find_elements(By.CSS_SELECTOR, "ytd-rich-grid-media")
print(f"找到 {len(videos)} 部長影片")

long_titles, long_views, long_dates = [], [], []
with tqdm(videos, desc="處理長影片資料中") as pbar:
    skip_count_long = 0
    for video in pbar:
        try:
            title = video.find_element(By.ID, "video-title").text
            view_element = video.find_element(By.XPATH, ".//span[contains(text(), '觀看')]")
            view_text = view_element.text
            view_count = parse_view_count(view_text)
            date_text = video.find_element(By.XPATH, ".//span[contains(text(), '前')]").text

            long_titles.append(title)
            long_views.append(int(view_count))
            long_dates.append(date_text)
        except Exception:
            skip_count_long += 1
            pbar.set_postfix({"跳過會員專屬長影片 :": f"{skip_count_long} 部"})


# --- 抓短影音 ---
shorts_url = f"https://www.youtube.com/{channel_handle}/shorts"
print(f"載入短影音頁面：{shorts_url}")
driver.get(shorts_url)
time.sleep(2)

profile_img = get_profile_picture_from_shorts()

print("正在自動滾動載入短影音資料...")
scroll_pause_time = 0.5
last_height = driver.execute_script("return document.documentElement.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(scroll_pause_time)
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

shorts = driver.find_elements(By.CSS_SELECTOR, "ytm-shorts-lockup-view-model-v2")
print(f"找到 {len(shorts)} 部短影音")

short_titles, short_views = [], []
with tqdm(shorts, desc="處理短影音資料中") as pbar:
    skip_count_short = 0
    for short in pbar:
        try:
            title = short.find_element(By.CLASS_NAME, "shortsLockupViewModelHostMetadataTitle").text
            view_element = short.find_element(By.XPATH, ".//span[contains(text(), '觀看')]")
            view_text = view_element.text
            view_count = parse_view_count(view_text)

            short_titles.append(title)
            short_views.append(int(view_count))
        except Exception:
            skip_count_short += 1
            pbar.set_postfix({"跳過會員專屬短影音 :": f"{skip_count_short} 部"})

driver.quit()
print(" * 關閉 Selenium")
print("-------------------------------------")

# --- 畫圖 ---
def plot_combined_chart(long_titles, long_views, short_titles, short_views, profile_img):
    def preprocess(titles, views):
        titles = titles[::-1]
        views = views[::-1]

        if not views:
            return titles, views, "次"

        max_view = max(views)

        if max_view >= 100_000_000:
            views_to_plot = [v / 100_000_000 for v in views]
            unit_label = "億次"
        elif max_view >= 10_000:
            views_to_plot = [v / 10_000 for v in views]
            unit_label = "萬次"
        else:
            views_to_plot = views
            unit_label = "次"

        return titles, views_to_plot, unit_label

    long_titles, long_views_plot, long_unit = preprocess(long_titles, long_views)
    short_titles, short_views_plot, short_unit = preprocess(short_titles, short_views)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=False)
    fig.suptitle(f"{channel_handle} 頻道公開影片觀看次數統計圖（截至 {datetime.today().strftime('%Y/%m/%d')}）", fontsize=16)

    if profile_img:
        try:
            size = (60, 60)
            profile_img = profile_img.resize(size).convert("RGBA")
            mask_draw = Image.new("L", size, 0)
            for y in range(size[1]):
                for x in range(size[0]):
                    if (x - size[0] / 2) ** 2 + (y - size[1] / 2) ** 2 < (size[0] / 2) ** 2:
                        mask_draw.putpixel((x, y), 255)
            profile_img.putalpha(mask_draw)

            fig.figimage(profile_img, 20, fig.bbox.ymax - 80)
        except Exception as e:
            print("錯誤：插入大頭貼失敗:", e)

    import matplotlib.ticker as ticker

    def plot_subplot(ax, views, titles, color, label, unit):
        count = len(views)
        if count == 0:
            ax.text(0.5, 0.5, f"沒有{label}", fontsize=20, color="gray",
                    ha="center", va="center", transform=ax.transAxes)
            ax.axis("off")
            return

        max_index = views.index(max(views))
        max_title = titles[max_index]
        max_view = views[max_index]
        avg10 = sum(views[-10:]) / min(10, len(views))
        avg_all = sum(views) / len(views)

        use_marker = count < 10
        if use_marker:
            ax.plot(range(count), views, color=color, marker='o')
        else:
            ax.plot(range(count), views, color=color)

        if count >= 10:
            moving_avg = [sum(views[i - 9:i + 1]) / 10 for i in range(9, count)]
            ax.plot(range(9, count), moving_avg, color="red", linewidth=2)

        ax.set_ylabel(f"{label}觀看（{unit}）", fontsize=11)
        ax.set_ylim(top=max(views) * 1.2)

        # x 軸刻度：避免過密和重複
        if count <= 20:
            ax.set_xticks(range(count))
            ax.set_xticklabels(range(1, count + 1))
        else:
            step = max(1, round(count / 15))
            ticks = list(range(0, count, step))
            if ticks[-1] != count - 1 and (count - 1 - ticks[-1]) >= step // 2:
                ticks.append(count - 1)
            ax.set_xticks(ticks)
            ax.set_xticklabels([i + 1 for i in ticks])

        # y 軸刻度設定，限制最大刻度數量避免重複
        ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=6, integer=True, prune='both'))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x)}"))

        # 文字放左上角
        text_x, text_y = 0.02, 0.95
        max_title_ = max_title if len(max_title) <= 50 else max_title[:50] + "..."

        if unit == "萬次":
            original_view = max_view * 10_000
        elif unit == "億次":
            original_view = max_view * 100_000_000
        else:
            original_view = max_view  # 萬一沒轉換過

        # 根據原始觀看數來決定格式
        if original_view < 10_000:
            view_str = f"{int(round(original_view))}"
            ax.text(text_x, text_y, f"最高觀看：{max_title_} ({view_str}次)",
                    fontsize=12, color="red", ha="left", va="top", transform=ax.transAxes)
        else:
            view_str = f"{max_view:,.1f}"
            ax.text(text_x, text_y, f"最高觀看：{max_title_} ({view_str}{unit})",
                    fontsize=12, color="red", ha="left", va="top", transform=ax.transAxes)

        # 箭頭從「最高觀看」文字正中間指向最高點
        arrow_start = (text_x + 0.03, text_y - 0.05)  # 微調讓箭頭從文字中央出發
        arrow_end = (max_index, max_view)

        ax.annotate(
            '',
            xy=arrow_end,
            xytext=arrow_start,
            textcoords=ax.transAxes,
            arrowprops=dict(arrowstyle='->', color='red', lw=1)
        )

        ax.text(0.98, 0.95, f"最新十部平均：{avg10:.1f}{unit}",
                transform=ax.transAxes, fontsize=10, ha="right",
                bbox=dict(facecolor="yellow", alpha=0.5))
        ax.text(0.98, 0.89, f"全部歷史平均：{avg_all:.1f}{unit}",
                transform=ax.transAxes, fontsize=10, ha="right",
                bbox=dict(facecolor="lightblue", alpha=0.5))

        ax.grid(True)

    plot_subplot(ax1, long_views_plot, long_titles, "blue", "長影片", long_unit)
    plot_subplot(ax2, short_views_plot, short_titles, "blue", "短影音", short_unit)
    ax2.set_xlabel("影片編號（從舊到新）")

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    os.makedirs("results", exist_ok=True)
    output_path = os.path.join("results", f"{channel_handle}_頻道公開影片觀看次數折線圖.png")
    plt.savefig(output_path)
    print(f"已儲存圖表：{output_path}")
    print("-------------------------------------")

print("正在繪製圖表...")
plot_combined_chart(long_titles, long_views, short_titles, short_views, profile_img)
input("按 Enter 鍵退出...")
exit()
