#一个简单的HTML的<img>标签生成小程序
def get_user_input():
    print("请输入文件目录信息（输入完成后按两次回车结束输入）：")
    contents = []
    while True:
        try:
            line = input()
            if line == '' and len(contents) > 0 and contents[-1] == '':
                # 如果连续两行都是空行，则认为输入结束
                break
            contents.append(line)
        except EOFError:
            # 捕获EOF错误（通常是Ctrl+D触发）
            break
    return "\n".join(contents[:-1])  # 去除最后一个多余的空行

# 获取用户输入作为file_info
file_info = get_user_input()

# 解析文件名并生成HTML img标签
lines = file_info.strip().split("\n")
img_tags = []
for index, line in enumerate(lines):
    # 提取文件名
    filename = line.split()[-1]
    img_tag = f'<img src="/egimg/{filename}" alt="Image {index + 1}">\n'
    img_tags.append(img_tag)

# 使用写模式"w"打开_img_.txt文件，这将清空文件中的现有内容
with open("_img_.txt", "w") as f:
    f.write("".join(img_tags))

print("IMG tags have been written to _img_.txt. The file has been overwritten with new content.")