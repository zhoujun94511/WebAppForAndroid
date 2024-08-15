import os
import logging


def clear_screenshots_folder():
    # 获取当前脚本所在的目录
    current_script_path = os.path.abspath(__file__)
    current_project_path = os.path.dirname(current_script_path)

    # 定位到 screenshots 文件夹
    screenshots_folder_path = os.path.join(current_project_path, 'screenshots')

    # 检查文件夹是否存在
    if not os.path.exists(screenshots_folder_path):
        logging.warning(f"文件夹 {screenshots_folder_path} 不存在")
        return

    # 遍历 screenshots 文件夹下的所有文件
    for filename in os.listdir(screenshots_folder_path):
        file_path = os.path.join(screenshots_folder_path, filename)

        # 删除文件
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                logging.info(f"已删除文件: {file_path}")
        except Exception as e:
            logging.error(f"删除文件时出错: {file_path} - 错误信息: {e}")

    logging.info("截图和录屏文件已清理完毕")


if __name__ == "__main__":
    # 配置日志输出格式
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # 执行清理操作
    clear_screenshots_folder()
