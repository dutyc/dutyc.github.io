import os
from PIL import Image
from PIL.ExifTags import TAGS

def get_image_metadata(image_path):
    """
    提取图片的EXIF元数据
    :param image_path: 图片文件路径
    :return: 包含元数据的字典
    """
    metadata = {
        "device": "未知",
        "iso": "未知",
        "aperture": "未知",
        "shutter_speed": "未知"
    }

    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()

        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)

                # 设备型号
                if tag_name == "Make":
                    metadata["device"] = value.strip()
                elif tag_name == "Model":
                    metadata["device"] = f"{metadata['device']} {value.strip()}"

                # ISO
                if tag_name == "ISOSpeedRatings":
                    metadata["iso"] = f"ISO {value}"

                # 光圈
                if tag_name == "FNumber":
                    metadata["aperture"] = f"f/{value[0] / value[1]:.1f}"

                # 快门速度
                if tag_name == "ExposureTime":
                    if value[1] == 1:
                        metadata["shutter_speed"] = f"{value[0]}秒"
                    else:
                        metadata["shutter_speed"] = f"1/{int(1 / value[0] * value[1])}秒"

    except Exception as e:
        print(f"无法读取 {image_path} 的EXIF数据: {e}")

    return metadata


def generate_html_gallery(directory):
    """
    遍历目录中的图片文件，生成包含图片信息的HTML代码
    :param directory: 图片所在目录
    """
    html_template = '''
    <div class="gallery-item">
        <img src="{src}" alt="{alt}">
        <div class="item-info">
            <h3>{device}</h3>
            <p>{details}</p>
        </div>
    </div>
    '''

    html_output = []

    # 遍历目录中的图片文件
    print(f"正在处理目录: {directory}")
    for filename in os.listdir(directory):
        print(f"找到文件: {filename}")
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.JPG')):
            print(f"处理图片: {filename}")
            image_path = os.path.join(directory, filename)
            metadata = get_image_metadata(image_path)

            # 拼接详细信息
            details = (
                f"{metadata['iso']} | "
                f"{metadata['aperture']} | "
                f"{metadata['shutter_speed']}"
            )

            # 确保图片路径以 /egimg/ 开头
            src_path = f"/egimg/{filename}"

            # 生成HTML代码
            html_code = html_template.format(
                src=src_path,
                alt=filename,
                device=metadata["device"],
                details=details
            )
            html_output.append(html_code)

    # 输出HTML代码
    output_file = os.path.join(directory, "output.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("<html><body>\n")
        f.write('<div class="gallery">\n')  # 添加外层容器
        f.write("\n".join(html_output))
        f.write('\n</div>\n')  # 关闭外层容器
        f.write("</body></html>")

    print(f"HTML代码已生成，保存在 {output_file}")


if __name__ == "__main__":
    # 设置目标目录为 egimg 子目录
    target_directory = os.path.join(os.getcwd(), "egimg")
    print(f"目标工作目录: {target_directory}")
    generate_html_gallery(target_directory)