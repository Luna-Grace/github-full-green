import os
import re
import json
import sys
from datetime import datetime

def load_config(config_path):
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        config = {"last_update": ""}
        save_config(config_path, config)
    return config

def save_config(config_path, config):
    with open(config_path, 'w') as file:
        json.dump(config, file, indent=2, ensure_ascii=False)

def update_readme_days(readme_path, config_path):
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # 构建配置文件路径
    config_path = os.path.join(script_dir, config_path)

    # 构建 README 文件路径
    readme_path = os.path.join(script_dir, readme_path)

    # 检查是否有未提交的更改
    if os.system('git diff-index --quiet HEAD --') != 0:
        print(f"当前有未提交的更改，请先提交或清空本地修改后再运行此脚本。")
        sys.exit(1)

    # 读取配置文件
    config = load_config(config_path)

    # 检查是否已更新过今天
    today = datetime.now().strftime("%Y-%m-%d")
    if config["last_update"] == today:
        print(f"今天已更新过 README 文件，无需再次更新。")
        return False

    # 读取 README 文件内容
    with open(readme_path, 'r', encoding='utf-8') as file:
        readme_content = file.read()

    # 使用正则表达式找到天数并更新
    pattern = r'保持全绿的第 \*\*\d+\*\* 天'
    start_date = datetime.strptime("2024-09-01", "%Y-%m-%d")
    days_since_start = (datetime.now() - start_date).days
    days_since_start = days_since_start + 1
    replacement = f'保持全绿的第 **{days_since_start}** 天'
    updated_content = re.sub(pattern, replacement, readme_content)

    # 检查 README 是否有变化
    if updated_content == readme_content:
        print(f"README 文件没有发生变化，无需更新。")
        return False

    # 将更新后的内容写入 README 文件
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    # 更新配置文件中的最近更新日期
    config["last_update"] = today
    save_config(config_path, config)

    print(f"README 文件已成功更新。")
    return True

if __name__ == "__main__":
    readme_path = "README.md"  # README 文件的路径
    config_path = "config.json"  # 配置文件的路径
    update_readme_days(readme_path, config_path)
