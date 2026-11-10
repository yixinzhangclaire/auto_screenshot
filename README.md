# FLBOOK 电子书截图转 PDF 使用说明

本工具使用 Python 自动截取 FLBOOK 网页中的书页，点击“下一页”，最后把截图合并成一个 PDF。适用于 **macOS**，程序文件名为 **`screenshot.py`**。

> 仅对你有权保存或使用的内容运行。此脚本生成的是图片版 PDF，不会自动识别文字。

## 1. 准备文件

将 `screenshot.py` 放到 Mac 的 **Downloads（下载）** 文件夹。

打开 **Terminal（终端）**：按 `Command + Space`，输入 `Terminal`，按 Enter。

## 2. 安装 Python 和依赖

先检查 Python 3 是否已安装：

```bash
python3 --version
```

如果提示找不到 `python3`，请先安装 Python 3（例如从 https://www.python.org/downloads/ 下载）。

安装脚本需要的库：

```bash
python3 -m pip install pyautogui pillow
```

如果 Mac 提示 `externally-managed-environment` 或不允许全局安装，请使用虚拟环境（以下命令可以直接逐行运行）：

```bash
cd ~/Downloads
python3 -m venv .flbook-venv
source .flbook-venv/bin/activate
python3 -m pip install pyautogui pillow
```

使用虚拟环境时，后续运行脚本也要先执行 `source ~/Downloads/.flbook-venv/bin/activate`。

## 3. 开启 macOS 权限（非常重要）

打开 **系统设置（System Settings）→ 隐私与安全性（Privacy & Security）**。

1. 进入 **屏幕与系统音频录制（Screen & System Audio Recording）**（部分 macOS 版本叫 **屏幕录制 / Screen Recording**），启用 **Terminal**。
2. 返回 **隐私与安全性**，进入 **辅助功能（Accessibility）**，启用 **Terminal**，允许脚本控制鼠标。
3. 如果列表里没有 Terminal，点击 `+`，从 **应用程序 → 实用工具（Applications → Utilities）** 中添加 Terminal。
4. 如果系统提示退出并重新打开 Terminal，请照做，再重新运行脚本。

**注意：** 如果你通过 VS Code、iTerm 等其他应用运行 Python，需要授权实际运行脚本的那个应用，而不一定是 Terminal。

## 4. 修改脚本参数

用文本编辑器打开 `screenshot.py`，找到文件开头类似这样的参数（以所提供的修正版脚本为例）：

```python
URL = 'https://flbook.com.cn/v/uA6qZOEHo1'
PAGES = 44
PAGE_WAIT_SECONDS = 2.2
OUT = Path.home() / 'Downloads' / '中国船舶集团_质量文化手册_2023.pdf'
IMAGE_DIR = Path.home() / 'Downloads' / 'flbook_pages'
```

| 参数 | 用途 | 如何修改 |
| --- | --- | --- |
| `URL` | 电子书网址 | 换成要截取的 FLBOOK 链接 |
| `PAGES` | **截图张数（不是点击次数）** | 每次翻页截一张时填需要的截图数量 |
| `PAGE_WAIT_SECONDS` | 翻页后等待网页加载的秒数 | 如果截图重复或尚未加载，可改成 `3` 或 `4` |
| `OUT` | 最终 PDF 路径及文件名 | 改最后的 PDF 文件名即可 |
| `IMAGE_DIR` | 截图及测试图片保存目录 | 可以保留默认值 |

### 如果只想点击 22 次

**重要：** 当前版本的循环在第一张截图之后，每翻一页再截图一次，因此**实际点击次数 = `PAGES - 1`**。

- 想要 **22 张截图**、**21 次点击**：设 `PAGES = 22`。
- 想要 **恰好点击 22 次**、并保存点击前后的全部画面（**23 张截图**）：设 `PAGES = 23`。

如果网页一次翻两张纸页，`PAGES = 23` 并不代表自动获得 44 张独立的单页图片；该脚本保存的是每次**屏幕上可见的整个选区**，不会自动拆分左右页。请按实际翻页方式检查结果。

## 5. 运行程序

在 Terminal 执行：

```bash
python3 ~/Downloads/screenshot.py
```

如果已创建虚拟环境，则先激活它：

```bash
source ~/Downloads/.flbook-venv/bin/activate
python3 ~/Downloads/screenshot.py
```

程序会打开指定网页。**不要使用 Mac 窗口左上角的绿色按钮进入独立全屏模式**。建议把浏览器窗口手动拖大，保持浏览器和 Terminal 在**同一个桌面空间（Space）**。

## 6. 按提示标记截图位置

程序会依次让你记录三个位置：

1. **书页左上角**：在 Terminal 按 Enter，利用 **5 秒倒计时**切回浏览器，将鼠标停在书页左上角；不需要点击。
2. **书页右下角**：回 Terminal 按 Enter，在 **5 秒内**把鼠标停在书页右下角；不需要点击。
3. **“下一页”箭头**：回 Terminal 按 Enter，在 **5 秒内**把鼠标停在网页右侧的翻页箭头；不需要点击。

这些位置以**屏幕坐标**记录。选定后不要移动或缩放浏览器窗口，也不要更改显示器布局，否则截取区域和翻页按钮可能偏移。

接下来确认网页在需要截取的第一页，回 Terminal 按 Enter。程序提供 **8 秒倒计时**，此时马上切回浏览器，让书页处于前台。之后程序会自动截图和点击翻页按钮；不要操作键盘鼠标。

**关键：** 不需要在全屏浏览器上方叠放 Terminal。只需在倒计时结束前切回浏览器即可。

## 7. 查看结果

默认输出位置：

- PDF：`~/Downloads/中国船舶集团_质量文化手册_2023.pdf`
- 中间截图：`~/Downloads/flbook_pages/`
- 第一张测试截图：`~/Downloads/flbook_pages/test_first_page.png`

生成后打开 PDF，检查有没有重复页、漏页、半页、双页画面或未加载完成的内容。

## 8. 常见问题

**Q：截图全是桌面壁纸？**

A：通常是截图时浏览器没有处在前台，或 macOS 屏幕录制权限未开启。不要使用独立全屏模式；确认浏览器与 Terminal 在同一 Space；在最后的 8 秒倒计时内切回浏览器。检查 `test_first_page.png`，正常后再继续。

**Q：程序不自动点击下一页？**

A：检查 **辅助功能**权限，以及第三次标记的位置是否正好是“下一页”箭头。网页布局发生变化时需要重新运行并重新标记。

**Q：几张截图一模一样？**

A：增加 `PAGE_WAIT_SECONDS`，例如改成 `3.5` 或 `4`，并确认每次点击确实翻页。

**Q：提示 `No module named pyautogui`？**

A：用运行脚本的同一个 Python 环境安装库：

```bash
python3 -m pip install pyautogui pillow
```

如果使用虚拟环境，请先激活环境，再安装和运行。

**Q：截图的图片很小或包含大量网页背景？**

A：重新运行，准确标记**书页本身**的左上角和右下角，不要标记整个浏览器窗口。

**Q：如何立刻停止自动截图？**

A：把鼠标快速移动到屏幕**左上角**，触发 PyAutoGUI 的安全停止机制；也可以切回 Terminal 按 `Control + C`。
