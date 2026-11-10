#!/usr/bin/env python3
"""Capture an FLBOOK you are authorized to keep for offline use.

macOS: allow Terminal (or the app running Python) Screen Recording and Accessibility.
Install: python3 -m pip install pyautogui pillow
"""
from pathlib import Path
import time
import webbrowser

import pyautogui as pg
from PIL import Image, ImageStat

URL = 'https://flbook.com.cn/v/zUAskOGK2o'
PAGES = 6
PAGE_WAIT_SECONDS = 2.2
OUT = Path.home() / 'Downloads' / '保利_质量文化手册.pdf'
IMAGE_DIR = Path.home() / 'Downloads' / 'flbook_pages'

pg.FAILSAFE = True

def countdown(seconds, label):
    print('\n' + label, flush=True)
    for n in range(seconds, 0, -1):
        print(f'  {n} 秒后记录……', flush=True)
        time.sleep(1)

def point(label):
    input(f'\n{label}\n按 Enter 后有 5 秒切到浏览器并移动鼠标，别点击网页。')
    countdown(5, '请切换到浏览器，并把鼠标停在目标位置。')
    p = pg.position()
    print(f'已记录: ({p.x}, {p.y})', flush=True)
    return p

def main():
    print('FLBOOK 截图合并 PDF (改进版)')
    print('重要：不要使用 Mac 绿色按钮进入独立全屏 Space。')
    print('请把浏览器窗口普通最大化（拖大），与 Terminal 保持在同一个桌面。')
    print('系统设置 → 隐私与安全性：允许 Terminal 屏幕录制、辅助功能。')
    webbrowser.open(URL)
    input('\n请等待网页加载并切到第 1 页；准备好后回到 Terminal 按 Enter。')

    a = point('1/3 把鼠标移到书页左上角')
    b = point('2/3 把鼠标移到书页右下角')
    nxt = point('3/3 把鼠标移到右侧下一页箭头')
    left, top = min(a.x, b.x), min(a.y, b.y)
    width, height = abs(a.x - b.x), abs(a.y - b.y)
    if width < 100 or height < 100:
        raise SystemExit('选区太小，请重新运行。')

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    input('\n请确认浏览器停在第 1 页。按 Enter 后有 8 秒切回浏览器；不要再碰鼠标键盘。')
    countdown(8, '请切换到浏览器，让书页可见。')

    # A single test image catches typical wallpaper / blocked screen recording failures.
    sample = pg.screenshot(region=(left, top, width, height)).convert('RGB')
    sample.save(IMAGE_DIR / 'test_first_page.png')
    means = ImageStat.Stat(sample.resize((64, 64))).stddev
    if max(means) < 9:
        raise SystemExit('检测到截图几乎是纯色，已停止以避免生成 44 页壁纸。检查浏览器是否在当前桌面、屏幕录制权限，以及裁剪区域。测试图：' + str(IMAGE_DIR / 'test_first_page.png'))
    print('已保存测试截图：', IMAGE_DIR / 'test_first_page.png', flush=True)
    paths = []
    for i in range(1, PAGES + 1):
        if i == 1:
            img = sample
        else:
            img = pg.screenshot(region=(left, top, width, height)).convert('RGB')
        path = IMAGE_DIR / f'page_{i:02d}.jpg'
        img.save(path, 'JPEG', quality=94, subsampling=0)
        paths.append(path)
        print(f'已截图 {i}/{PAGES}', flush=True)
        if i < PAGES:
            pg.click(nxt.x, nxt.y)
            time.sleep(PAGE_WAIT_SECONDS)

    images = [Image.open(p).convert('RGB') for p in paths]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(OUT, format='PDF', save_all=True, append_images=images[1:], resolution=120)
    for im in images:
        im.close()
    print('PDF 已生成：', OUT)
    print('请检查是否存在重复页/双页画面。')

if __name__ == '__main__':
    main()
