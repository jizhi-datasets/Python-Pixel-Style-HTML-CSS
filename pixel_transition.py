#!/usr/bin/env python3
# pixel_transition.py
from PIL import Image
from collections import Counter
import argparse

def pixelize(input_path, output_path, pixel_size=10, interval=1):
    img = Image.open(input_path).convert('RGB')
    w, h = img.size

    # 1. 统计颜色频率
    colors = []
    for y in range(0, h, interval):
        for x in range(0, w, interval):
            colors.append(img.getpixel((x, y)))
    bg_color = Counter(colors).most_common(1)[0][0]

    # 2. 计算输出画布大小
    out_w = (w + interval - 1) // interval
    out_h = (h + interval - 1) // interval
    out_img = Image.new('RGB', (out_w * pixel_size, out_h * pixel_size), bg_color)

    # 3. 绘制非背景色像素块
    for y in range(0, h, interval):
        for x in range(0, w, interval):
            c = img.getpixel((x, y))
            if c != bg_color:
                px = (x // interval) * pixel_size
                py = (y // interval) * pixel_size
                pixel_block = Image.new('RGB', (pixel_size, pixel_size), c)
                out_img.paste(pixel_block, (px, py))

    out_img.save(output_path)
    print(f'Saved: {output_path} | background: #{bg_color[0]:02x}{bg_color[1]:02x}{bg_color[2]:02x}')

if __name__ == '__main__':
    # python pixel_transition.py cats-8096304_1280.jpg cats-8096304_1280_pixel.jpg --pixel 12 --interval 6
    parser = argparse.ArgumentParser(description='Pixel-art transition with color optimization')
    parser.add_argument('input', help='source image')
    parser.add_argument('output', help='destination PNG')
    parser.add_argument('--pixel', type=int, default=10, help='size of each pixel block (px)')
    parser.add_argument('--interval', type=int, default=1, help='sampling interval')
    args = parser.parse_args()

    pixelize(args.input, args.output, args.pixel, args.interval)
