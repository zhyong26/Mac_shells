#!/usr/bin/env python
# coding=utf-8
import os
import subprocess
import asyncio
from playwright.async_api import async_playwright

async def html_to_png(html_file, output_png):
    """
    使用 Playwright 将 HTML 渲染并精确截图 SVG 区域
    """
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)
        # device_scale_factor=2 可提高图片清晰度（类似 Retina 屏幕效果）
        context = await browser.new_context(device_scale_factor=2)
        page = await context.new_page()

        abs_path = os.path.abspath(html_file)
        await page.goto(f"file://{abs_path}")

        try:
            # 1. 定位 Markmap 的 SVG 容器
            svg_selector = "svg.markmap"
            await page.wait_for_selector(svg_selector, timeout=10000)

            # 2. 等待渲染和初始缩放动画完成
            await asyncio.sleep(2)

            # 3. 修正参数名为 omit_background
            element = page.locator(svg_selector)
            await element.screenshot(
                path=output_png,
                omit_background=False  # False 表示保留白色背景，True 为透明背景
            )

        except Exception as e:
            print(f"渲染或截图过程出错: {e}")
        finally:
            await browser.close()

def convert_md_to_png(input_md):
    if not os.path.exists(input_md):
        print(f"错误: 找不到输入文件 {input_md}")
        return

    base_name = os.path.splitext(input_md)[0]
    temp_html = f"{base_name}_temp.html"
    output_png = f"{base_name}.png"

    try:
        # 生成中间 HTML 文件
        subprocess.run(["markmap", input_md, "-o", temp_html, "--offline"], check=True)

        # 运行异步转换
        asyncio.run(html_to_png(temp_html, output_png))

        # 清理临时文件
        if os.path.exists(temp_html):
            os.remove(temp_html)

        if os.path.exists(output_png):
            print(f"成功导出图片: {os.path.abspath(output_png)}")
    except subprocess.CalledProcessError:
        print("错误: markmap-cli 执行失败，请检查 Markdown 格式或 npm 安装情况。")
    except Exception as e:
        print(f"运行失败: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python md2img.py <your_file.md>")
    else:
        convert_md_to_png(sys.argv[1])
