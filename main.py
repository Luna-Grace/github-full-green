import os
import re
import json
import sys
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)  # 初始化 Colorama，使颜色输出生效

def check_git_installed():
    # 使用 os.system() 检查 Git 是否安装
    if os.system("git --version") != 0:
        print(f"{Fore.RED}检查Git配置...failed")
        print(f"{Fore.BLUE}原因：未找到 Git，请确保您的设备上已安装 Git。")
        sys.exit(1)
    else:
        print(f"{Fore.GREEN}检查Git配置...done")

def check_in_git_repo():
    # 检查脚本所在位置是否在 Git 仓库中
    if not os.path.isdir('.git'):
        print(f"{Fore.RED}检查仓库配置...failed")
        print(f"{Fore.BLUE}原因：当前位置不是一个 Git 仓库，请将脚本放在一个 Git 仓库中运行。")
        sys.exit(1)
    else:
        print(f"{Fore.GREEN}检查仓库配置...done")

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
        json.dump(config, file)

def update_readme_days(readme_path, config_path):
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # 构建配置文件路径
    config_path = os.path.join(script_dir, config_path)

    # 构建 README 文件路径
    readme_path = os.path.join(script_dir, readme_path)

    # 检查 Git 是否安装
    check_git_installed()

    # 检查是否在 Git 仓库中
    check_in_git_repo()

    # 检查是否有未提交的更改
    if os.system('git diff-index --quiet HEAD --') != 0:
        print(f"{Fore.RED}当前有未提交的更改，请先提交或清空本地修改后再运行此脚本。")
        sys.exit(1)

    # 读取配置文件
    config = load_config(config_path)

    # 检查是否已更新过今天
    today = datetime.now().strftime("%Y-%m-%d")
    if config["last_update"] == today:
        print(f"{Fore.BLUE}今天已更新过 README 文件，无需再次更新。")
        return False

    # 读取 README 文件内容
    with open(readme_path, 'r', encoding='utf-8') as file:
        readme_content = file.read()

    # 使用正则表达式找到天数并更新
    pattern = r'保持全绿的第 \*\*\d+\*\* 天'
    start_date = datetime.strptime("2024-06-09", "%Y-%m-%d")  # 替换"2024-06-09"为你的实际开始日期
    days_since_start = (datetime.now() - start_date).days + 1  # 加1是为了包括开始日期
    replacement = f'保持全绿的第 **{days_since_start}** 天'
    updated_content = re.sub(pattern, replacement, readme_content)

    # 检查 README 是否有变化
    if updated_content == readme_content:
        print(f"{Fore.BLUE}README 文件没有发生变化，无需更新。")
        return False

    # 将更新后的内容写入 README 文件
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    # 更新配置文件中的最近更新日期
    config["last_update"] = today
    save_config(config_path, config)

    print(f"{Fore.GREEN}README 文件已成功更新。")
    return True

def git_commit_and_push():
    try:
        # 提交所有更改
        os.system('git add .')
        # 提交更改并添加提交信息
        commit_message = f"Update README with latest streak count"
        os.system(f'git commit -m "{commit_message}"')
        # 推送到远程仓库
        os.system('git push')
        print(f"{Fore.GREEN}README 文件已成功提交并推送到远程仓库。")
    except Exception as e:
        print(f"{Fore.RED}出现错误: {e}")

if __name__ == "__main__":
    readme_path = "README.md"  # README 文件的路径
    config_path = "config.json"  # 配置文件的路径
    if update_readme_days(readme_path, config_path):
        git_commit_and_push()
