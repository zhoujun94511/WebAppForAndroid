import os
<<<<<<< HEAD
import re
import time
import json
import shlex
import random
import string
import shutil
import psutil
import socket
import zipfile
import logging
import adbutils
import platform
import tempfile
import subprocess
=======
import shutil
import adbutils
import logging
import time
import subprocess
import tempfile
import re
import platform
import psutil

>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5

# 设置全局日志配置
logging.basicConfig(
    level=logging.INFO,  # 设置全局日志级别为 INFO，可以更改为其他级别
    format='%(asctime)s [%(levelname)s] %(message)s',  # 设置日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 设置日期时间格式
)


<<<<<<< HEAD
# 创建截图和录屏储路径
def screenshot_and_record_folders():
    screenshot_and_record_folder = os.path.join(os.path.dirname(__file__), 'screenshot_and_record')
    if not os.path.exists(screenshot_and_record_folder):
        logging.info(f'创建截图与录屏存储路径为: {screenshot_and_record_folder}')
        os.makedirs(screenshot_and_record_folder)

    screenshot_folder = os.path.join(screenshot_and_record_folder, 'mobile_screenshot')
    if not os.path.exists(screenshot_folder):
        logging.info(f'创建截图存储路径为: {screenshot_folder}')
        os.makedirs(screenshot_folder)

    record_folder = os.path.join(screenshot_and_record_folder, 'mobile_record')
    if not os.path.exists(record_folder):
        logging.info(f'创建录屏存储路径为: {record_folder}')
        os.makedirs(record_folder)

    return screenshot_and_record_folder, record_folder, screenshot_folder


# 清理aab生成使用过的文件夹
def clear_aab_folders():
    aab_conversion_clean_folder = os.path.join(os.path.dirname(__file__), 'aab_conversion')
    download_folder_clean = os.path.join(aab_conversion_clean_folder, 'download_folder')
    upload_folder_clean = os.path.join(aab_conversion_clean_folder, 'upload_folder')

    # 清理下载文件夹
    for filename in os.listdir(download_folder_clean):
        file_path = os.path.join(download_folder_clean, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                logging.info(f"已清理文件 {file_path}")
        except Exception as e:
            logging.error(f"清理文件 {file_path} 时出错: {e}")

    # 清理上传文件夹
    for filename in os.listdir(upload_folder_clean):
        file_path = os.path.join(upload_folder_clean, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                logging.info(f"已清理文件 {file_path}")
        except Exception as e:
            logging.error(f"清理文件 {file_path} 时出错: {e}")


# 清理证书生成使用过的文件夹
def clear_generate_random_signature_folder():
    # 获取当前文件的目录
    generate_random_signature_current_dir = os.path.dirname(__file__)

    # 构建要清理的文件夹路径
    generate_random_signature_folder = os.path.join(generate_random_signature_current_dir, 'aab_conversion',
                                                    'certificate_folder',
                                                    'generate_random_signature')

    # 清理文件夹中的文件
    for filename in os.listdir(generate_random_signature_folder):
        file_path = os.path.join(generate_random_signature_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                logging.info(f"已清理文件 {file_path}")
        except Exception as e:
            logging.error(f"清理文件 {file_path} 时出错: {e}")


# 清理截图与录屏使用过的文件夹
def clear_screenshot_and_record_folders():
    screenshot_and_record_folder = os.path.join(os.path.dirname(__file__), 'screenshot_and_record')
    screenshot_folder_clean = os.path.join(screenshot_and_record_folder, 'mobile_screenshot')
    record_folder_clean = os.path.join(screenshot_and_record_folder, 'mobile_record')

    logging.info(f'正在清理截图与录屏文件夹...')

    # 清理screenshot文件夹
    for filename in os.listdir(screenshot_folder_clean):
        file_path = os.path.join(screenshot_folder_clean, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                logging.info(f"已清理截图文件 {file_path}")
        except Exception as e:
            logging.error(f"清理截图文件夹 {file_path} 时出错: {e}")

    # 清理record文件夹
    for filename in os.listdir(record_folder_clean):
        file_path = os.path.join(record_folder_clean, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                logging.info(f"已清理录屏文件 {file_path}")
        except Exception as e:
            logging.error(f"清理录屏文件夹 {file_path} 时出错: {e}")


# 获取系统类型
def get_windows():
    return platform.system().lower() == 'windows'


# 获取本地IP
def get_local_ip():
    sock = None  # 初始化 sock 变量
    try:
        # 创建一个 UDP 套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接一个临时的目标
        sock.connect(("8.8.8.8", 80))
        # 获取本地 IP 地址
        local_ip = sock.getsockname()[0]
        logging.info(f"获取到当前本地IP是: {local_ip}")
        return local_ip
    except Exception as e:
        logging.error("获取本地IP失败: %s", e)
        return None  # 返回 None 表示获取IP失败
    finally:
        if sock is not None:
            sock.close()  # 仅在 sock 变量不为空时关闭


# Webapp初始化adb时调用的函数
def initialize_adb():
    # 获取当前脚本所在的目录
    script_dir_adb = os.path.dirname(os.path.abspath(__file__))
    logging.info(f"获取到当前脚本所在目录是: {script_dir_adb}")
=======
def create_storage_path():
    """
    创建截图存录屏储路径
    """
    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 定义存储路径为脚本所在目录下的 /screenshots 文件夹
    storage_path = os.path.join(script_dir, 'screenshots')

    # 确保存储目录存在
    if not os.path.exists(storage_path):
        logging.info(f'创建截图录屏存储路径: {storage_path}')
        os.makedirs(storage_path)

    # 返回存储路径
    return storage_path


# 调用函数创建截图存储路径，并将返回值存储在变量中
storage_upath = create_storage_path()


# # 初始化adb服务
# def initialize_adb():
#     logging.info('正在初始化 ADB 服务...')
#     subprocess.run(['adb', 'start-server'])
#
#     # 检查 ADB 服务器状态
#     result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
#     if 'List of devices attached' not in result.stdout:
#         raise Exception('Failed to connect to ADB server.')
#     logging.info('ADB 服务初始化完毕')

def get_windows():
    return platform.system().lower() == 'windows'


def initialize_adb():
    # 获取当前脚本所在的目录
    script_dir_adb = os.path.dirname(os.path.abspath(__file__))
    logging.info(f"当前脚本所在目录: {script_dir_adb}")
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5

    # 查询当前环境变量是否配置了adb
    adb_in_path = shutil.which("adb")

    if adb_in_path:
        adb_path = adb_in_path
    else:
        # 检测系统架构
        system_bits = platform.architecture()[0]
        logging.info(f"系统位数: {system_bits}")

        # 构建 scrcpy-win32-v2.4 和 scrcpy-win64-v2.4 的完整路径
        adb_path_32 = os.path.join(script_dir_adb, "Pconfigure", "scrcpy-win32-v2.4", "adb")
        adb_path_64 = os.path.join(script_dir_adb, "Pconfigure", "scrcpy-win64-v2.4", "adb")

        # 选择正确的 adb 工具路径
        adb_path = adb_path_64 if system_bits == '64bit' else adb_path_32
        logging.info(f"选择的ADB路径: {adb_path}")

    # 初始化adb服务
<<<<<<< HEAD
    logging.info('正在初始化ADB服务...')
=======
    logging.info('正在初始化 ADB 服务...')
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
    subprocess.run([adb_path, 'start-server'])

    # 检查 ADB 服务器状态
    result = subprocess.run([adb_path, 'devices'], capture_output=True, text=True)
    if 'List of devices attached' not in result.stdout:
        raise Exception('Failed to connect to ADB server.')
<<<<<<< HEAD
    logging.info('获取到ADB服务初始化完毕...')
=======
    logging.info('ADB 服务初始化完毕')
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5


# 获取设备列表
def get_devices():
    try:
<<<<<<< HEAD
        logging.info('正在获取设备信息...')
        client = adbutils.AdbClient()
        devices = client.device_list()  # 使用 device_list 方法
        device_serials = [device.serial for device in devices]
        logging.info(f'获取到的设备列表信息是: {device_serials}')
        clear_screenshot_and_record_folders()  # 设备每次刷新时清理一次截图与录屏文件夹
        return device_serials
    except Exception as e:
        logging.error(f'获取设备信息失败: {e}')
        return []


# 获取设备型号
def get_device_model(device_id):
    try:
        logging.info(f'正在获取设备 {device_id} 的型号...')
        device = adbutils.adb.device(device_id)
        model = device.prop.model
        logging.info(f'设备 {device_id} 型号为: {model}')
        return model
    except Exception as e:
        logging.error(f"获取设备型号失败: {e}")
        return "unknown"


# 获取已安装的第三方应用数据
def get_installed_apps(device_id, timeout=5):
    try:
        logging.info(f'正在获取设备 {device_id} 上的已安装第三方应用...')
        device = adbutils.adb.device(device_id)

        # 使用 adb shell 命令获取第三方应用列表，添加超时机制
        result = device.shell("pm list packages -3", timeout=timeout)
        # 使用 adb shell 命令获取系统应用列表，添加超时机制
        # result = device.shell("pm list packages -s", timeout=timeout)

        # 处理输出，提取包名
        third_party_packages = [
            line.split(":", 1)[1].strip()
            for line in result.splitlines()
            if line.startswith("package:")
        ]

        logging.info(f'设备 {device_id} 上的已安装第三方应用数量: {len(third_party_packages)}')
        return third_party_packages
    except adbutils.AdbTimeout:
        logging.error(f'获取已安装第三方应用超时')
        return []
    except Exception as e:
        logging.error(f'获取已安装第三方应用失败: {e}')
=======
        logging.info('正在获取设备列表...')
        client = adbutils.AdbClient()
        devices = client.device_list()  # 使用 device_list 方法
        device_serials = [device.serial for device in devices]
        logging.info(f'获取到的设备列表: {device_serials}')
        return device_serials
    except Exception as e:
        logging.error(f'获取设备列表失败: {e}')
        return []


# 获取已安装应用
def get_installed_apps(device_id):
    try:
        logging.info(f'正在获取设备 {device_id} 上的已安装应用...')
        device = adbutils.adb.device(device_id)
        packages = device.list_packages()
        logging.info(f'设备 {device_id} 上的已安装应用: {packages}')
        return packages
    except Exception as e:
        logging.error(f'获取已安装应用失败: {e}')
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
        return []


# 卸载应用
def uninstall_app(device_id, package_name):
    try:
        logging.info(f'正在卸载设备 {device_id} 上的应用 {package_name}...')
        if not device_id or not package_name:
<<<<<<< HEAD
            logging.warning('设备ID和应用包名缺失')
            return {'success': False, 'error': '设备ID和包应用包名缺失'}
=======
            logging.warning('设备 ID 和包名是必需的')
            return {'success': False, 'error': '设备 ID 和包名是必需的'}
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5

        device = adbutils.adb.device(device_id)
        device.uninstall(package_name)
        logging.info(f'应用 {package_name} 卸载成功')
        return {'success': True}
    except Exception as e:
        logging.error(f'卸载应用失败: {e}')
        return {'success': False, 'error': str(e)}


# 安装应用
<<<<<<< HEAD
def install_apk(device_id, apk_files):
    try:
        logging.info(f'正在为设备 {device_id} 安装 APK 文件...')
        device = adbutils.adb.device(device_id)
        results = []

        with tempfile.TemporaryDirectory() as temp_dir:
            for apk_file in apk_files:
                apk_filename = apk_file.filename
                if not apk_filename.lower().endswith('.apk'):
                    logging.warning(f'跳过非APK文件: {apk_filename}')
                    results.append({'filename': apk_filename, 'success': False, 'error': '非APK文件'})
                    continue

                apk_path = os.path.join(temp_dir, apk_filename)
                apk_file.save(apk_path)
                logging.info(f'APK文件已保存到临时文件夹: {apk_path}')

                try:
                    device.install(apk_path)
                    logging.info(f'APK文件 {apk_filename} 安装成功')
                    results.append({'filename': apk_filename, 'success': True})
                except Exception as e:
                    logging.error(f'安装APK {apk_filename} 失败: {e}')
                    results.append({'filename': apk_filename, 'success': False, 'error': str(e)})

        return results

    except Exception as e:
        logging.error(f'安装APK过程中发生错误: {e}')
        return [{'filename': 'unknown', 'success': False, 'error': str(e)}]


# 截图函数
def take_screenshot(device_id):
    _, _, screenshot_folder = screenshot_and_record_folders()
=======
def install_apk(device_id, apk_file):
    try:
        logging.info(f'正在为设备 {device_id} 安装 APK 文件 {apk_file.filename}...')

        # 检查文件是否是 .apk 格式
        if not apk_file.filename.endswith('.apk'):
            logging.warning('文件格式错误：只能安装 .apk 格式的文件')
            return {'success': False, 'error': '文件格式错误：只能安装 .apk 格式的文件'}

        # 通过 adbutils 获取设备对象
        device = adbutils.adb.device(device_id)

        # 使用临时文件夹保存 APK 文件
        with tempfile.TemporaryDirectory() as temp_dir:
            apk_filename = apk_file.filename
            apk_path = os.path.join(temp_dir, apk_filename)

            # 将 APK 文件保存到临时文件夹
            apk_file.save(apk_path)
            logging.info(f'APK 文件已保存到临时文件夹: {apk_path}')

            # 检查 APK 文件是否存在
            if not os.path.exists(apk_path):
                raise FileNotFoundError(f"找不到指定的 APK 文件：{apk_path}")

            # 使用 adbutils 进行 APK 安装
            device.install(apk_path)
            logging.info(f'APK 文件 {apk_path} 安装成功')

            # 返回安装成功的结果
            return {'success': True}

    except FileNotFoundError as e:
        logging.error(f'安装 APK 失败: {e}')
        return {'success': False, 'error': str(e)}

    except Exception as e:
        logging.error(f'安装 APK 失败: {e}')
        return {'success': False, 'error': str(e)}


# 截图
def take_screenshot(device_id):
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
    try:
        logging.info(f'正在为设备 {device_id} 截图...')
        device = adbutils.adb.device(device_id)

<<<<<<< HEAD
        if not device.is_screen_on():
            logging.error('设备屏幕已锁屏，无法进行截图。')
            return {'success': False, 'error': '设备屏幕已锁屏，无法进行截图。'}

        timestamp = time.strftime('%Y%m%d%H%M%S')
        device_model = get_device_model(device_id).replace(' ', '_')  # 替换空格为下划线
        filename = f'screenshot_{device_model}_{timestamp}.png'
        local_screenshot_path = os.path.join(screenshot_folder, filename)
        pil_image = device.screenshot()
        pil_image.save(local_screenshot_path)
        logging.info(f'截图保存至: {local_screenshot_path}')
        return {'success': True, 'path': local_screenshot_path, 'filename': filename}
=======
        # 检查屏幕是否亮屏
        if not device.is_screen_on():
            logging.error('设备屏幕未亮，无法进行截图。')
            return {'success': False, 'error': '设备屏幕未亮，无法进行截图。'}

        timestamp = time.strftime('%Y%m%d%H%M%S')
        local_screenshot_path = os.path.join(storage_upath, f'screenshot_{timestamp}.png')
        pil_image = device.screenshot()
        pil_image.save(local_screenshot_path)
        logging.info(f'截图保存至: {local_screenshot_path}')
        return {'success': True, 'path': local_screenshot_path}
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
    except Exception as e:
        logging.error(f'截图失败: {e}')
        return {'success': False, 'error': str(e)}


# 录屏函数
def record_screen(device_id, duration):
<<<<<<< HEAD
    _, record_folder, _ = screenshot_and_record_folders()
=======
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
    try:
        logging.info(f'正在为设备 {device_id} 录屏，时长: {duration} 秒...')
        duration = int(duration)
        device = adbutils.adb.device(device_id)

<<<<<<< HEAD
        if not device.is_screen_on():
            logging.error('设备屏幕已锁屏，无法进行录屏。')
            return {'success': False, 'error': '设备屏幕已锁屏，无法进行录屏。'}

        timestamp = time.strftime('%Y%m%d%H%M%S')
        device_model = get_device_model(device_id).replace(' ', '_')  # 替换空格为下划线
        filename = f'screen_record_{device_model}_{timestamp}.mp4'
        device_record_path = f'/sdcard/{filename}'

        # 使用 adb shell 命令进行录屏
        cmd = f"adb -s {device_id} shell screenrecord --time-limit {duration} {device_record_path}"
        logging.info(f'执行录屏命令: {cmd}')
        process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            error_message = stderr.decode('utf-8')
            logging.error(f'录屏命令执行失败: {error_message}')
            return {'success': False, 'error': f'录屏失败: {error_message}'}

        # 等待录屏完成
        time.sleep(duration + 1)

        # 将录屏文件从设备拉取到本地
        local_record_path = os.path.join(record_folder, filename)
        pull_cmd = f'adb -s {device_id} pull "{device_record_path}" "{local_record_path}"'
        logging.info(f'执行拉取录屏文件命令: {pull_cmd}')
        result = subprocess.run(pull_cmd, shell=True, capture_output=True, text=True)
        logging.info(f'拉取录屏文件命令标准输出: {result.stdout}')

        if result.returncode != 0:
            logging.error(f'拉取录屏文件失败，返回码: {result.returncode}')
            return {'success': False, 'error': f'拉取录屏文件失败，返回码: {result.returncode}'}

        # 验证文件是否已成功保存到本地
        if not os.path.exists(local_record_path):
            logging.error(f'文件在本地路径中找不到: {local_record_path}')
            return {'success': False, 'error': f'文件找不到: {local_record_path}'}

        # 删除设备上的录屏文件
        logging.info(f'删除设备上的录屏文件: {device_record_path}')
        device.shell(f'rm {device_record_path}')

        logging.info(f'录屏完成，保存至: {local_record_path}')
        return {'success': True, 'path': local_record_path, 'filename': filename}
    except Exception as e:
        logging.error(f'录屏过程中发生错误: {str(e)}')
        return {'success': False, 'error': str(e)}


# 提供下载转换后的文件
def get_take_screenshot_and_record_files():
    screenshot_and_record_folder, record_folder, screenshot_folder = screenshot_and_record_folders()

    converted_files = []

    # 遍历 record 文件夹
    for root, dirs, files in os.walk(record_folder):
        for file in files:
            converted_files.append(file)  # 只添加文件名
            logging.info(f"找到录屏文件: {file}")

    # 遍历 screenshot 文件夹
    for root, dirs, files in os.walk(screenshot_folder):
        for file in files:
            converted_files.append(file)  # 只添加文件名
            logging.info(f"找到截图文件: {file}")

    return converted_files


=======
        # 检查屏幕是否亮屏
        if not device.is_screen_on():
            logging.error('设备屏幕未亮，无法进行录屏。')
            return {'success': False, 'error': '设备屏幕未亮，无法进行录屏。'}

        timestamp = time.strftime('%Y%m%d%H%M%S')
        device_record_path = f'/sdcard/screen_record_{timestamp}.mp4'
        screenrecord_command = f"screenrecord --time-limit {duration} {device_record_path}"
        device.shell(screenrecord_command)
        local_record_path = os.path.join(storage_upath, f'screen_record_{timestamp}.mp4')
        device.sync.pull(device_record_path, local_record_path)
        device.shell(f'rm {device_record_path}')
        logging.info(f'录屏完成，保存至: {local_record_path}')
        return {'success': True, 'path': local_record_path}
    except Exception as e:
        logging.error(f'录屏失败: {e}')
        return {'success': False, 'error': str(e)}


>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
# 重启设备
def restart_device(device_id):
    try:
        logging.info(f'正在重启设备 {device_id}...')
        device = adbutils.adb.device(device_id)
        device.reboot()
        logging.info(f'设备 {device_id} 重启成功')
        return {'success': True}
    except Exception as e:
        logging.error(f'重启设备失败: {e}')
        return {'success': False, 'error': str(e)}


# 获取设备信息
def get_new_device_info(device_id):
    try:
        logging.info(f'正在获取设备 {device_id} 的信息...')
        # 使用 adb 命令获取设备信息
        command = f'adb -s {device_id} shell getprop'
<<<<<<< HEAD
        # logging.info(f'执行命令: {command}')
=======
        logging.info(f'执行命令: {command}')
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5

        output = subprocess.check_output(command, shell=True, encoding='utf-8')
        logging.debug(f'ADB 输出: \n{output}')

        # 默认需要获取的参数列表（MTK芯片）
        desired_properties_mtk = {
            'ro.product.model': '设备名称',
            'ro.product.brand': '设备品牌',
            'ro.build.version.release': '安卓版本',
            'ro.build.version.sdk': 'SDK版本',
            'ro.soc.manufacturer': 'CPU品牌',
            'ro.boot.hardware': 'CPU型号',
            'ro.product.cpu.abi': 'CPU架构',
            'ro.serialno': '设备序列号'
        }

<<<<<<< HEAD
        # 需要获取的参数列表（高通芯片）
=======
        # 高通芯片上的需要获取的参数列表
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
        desired_properties_qualcomm = {
            'ro.product.model': '设备名称',
            'ro.product.brand': '设备品牌',
            'ro.build.version.release': '安卓版本',
            'ro.build.version.sdk': 'SDK版本',
            'ro.soc.manufacturer': 'CPU品牌',
            'ro.boot.hardware.platform': 'CPU型号',
            'ro.product.cpu.abi': 'CPU架构',
            'ro.serialno': '设备序列号'
        }

        # 将输出解析成字典
        device_info = {}
        is_mtk = False
        is_qualcomm = False

        for line in output.strip().split('\n'):
            # 将行分割成键值对
            if ':' in line:
                key, value = line.split(':', 1)
                # 移除前后的空格和特殊符号
                key = key.strip().strip('[]')
                value = value.strip().strip('[]')

                # 检查当前键值对是否与MTK芯片或高通芯片匹配
                if key in desired_properties_mtk:
                    device_info[desired_properties_mtk[key]] = value
                    is_mtk = True
                elif key in desired_properties_qualcomm:
                    device_info[desired_properties_qualcomm[key]] = value
                    is_qualcomm = True

        # 根据芯片品牌选择合适的字典
<<<<<<< HEAD
=======
        # 如果既不是 MTK 也不是高通，则选择默认的 desired_properties_mtk
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
        if is_qualcomm:
            desired_properties = desired_properties_qualcomm
        elif is_mtk:
            desired_properties = desired_properties_mtk
        else:
            # 未能确定芯片类型，返回空字典或默认字典
            logging.warning('未能确定芯片类型')
            return {'success': False, 'error': '未能确定芯片类型'}

        # 检查是否获取到了所有需要的参数
        for prop in desired_properties.values():
            # 如果某个属性缺失，则将其设置为 None
            if prop not in device_info:
                device_info[prop] = None

        logging.info(f'获取到的设备信息: {device_info}')
        return device_info

    except subprocess.CalledProcessError as e:
        logging.error(f'Error fetching device info: {e}')
        return {'error': 'Failed to execute adb command.'}
    except Exception as e:
        logging.error(f'Unexpected error: {e}')
        return {'error': f'Unexpected error: {e}'}


# 获取当前正在运行的应用信息
def get_current_app_info(device_id):
    try:
        logging.info(f'正在获取设备 {device_id} 当前运行的应用信息...')
        # 使用 adbutils 获取设备
        device = adbutils.adb.device(device_id)

        # 检查屏幕是否亮屏
        if not device.is_screen_on():
<<<<<<< HEAD
            logging.error('设备屏幕已锁屏，无法获取当前应用信息，请解锁后重试。')
            return {'success': False, 'error': '设备屏幕已锁屏，无法获取当前应用信息，请解锁后重试。'}
=======
            logging.error('设备屏幕未亮，无法获取当前应用信息。')
            return {'success': False, 'error': '设备屏幕未亮，无法获取当前应用信息。'}
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5

        # 使用命令获取当前聚焦窗口的信息
        focused_window_info = device.shell("dumpsys window | grep mFocusedWindow")

        # 如果找到聚焦窗口信息
        if focused_window_info:
            # 提取包名和活动名的部分
            parts = focused_window_info.split()
            if len(parts) >= 3:
                package_and_activity = parts[-1].rstrip('}')  # 移除末尾的 '}'

                # 检查 package_and_activity 是否包含 '/'
                if '/' in package_and_activity:
                    package_name, activity_name = package_and_activity.split('/')
                    # 返回信息
                    logging.info(f'获取到的当前运行的应用: 包名: {package_name}, 活动名: {activity_name}')
                    return {
                        'success': True,
                        'package_name': package_name,
                        'activity_name': activity_name,
                        'start_activity_name': package_and_activity,  # 完整的启动活动名
                    }
            # 如果未找到 '/'，返回错误信息
            logging.warning('未找到当前运行的应用')
            return {'success': False, 'error': '未找到当前运行的应用'}
    except Exception as e:
        # 在发生异常时记录错误并返回错误信息
        logging.error(f'获取当前应用信息失败: {e}')
        return {'success': False, 'error': str(e)}


# 获取设备IP地址列表
def get_device_ip_address(device_id):
    try:
        device = adbutils.adb.device(device_id)
        # 获取设备的IP地址
        ip_output = device.shell('ip addr show wlan0').strip()
        ip_addresses = re.findall(r'inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ip_output)

        return ip_addresses
    except Exception as e:
        logging.error(f"获取设备 IP 地址失败: {e}")
        return []


# 开启无线调试
def enable_wireless_debugging(device_id, max_retries=2):
    try:
        logging.info(f"正在为设备 {device_id} 启用无线调试...")
        device = adbutils.adb.device(device_id)
        device.shell('setprop service.adb.tcp.port 5555')
        logging.info("设置 service.adb.tcp.port 为 5555")
        device.shell('stop adbd')
        logging.info("停止 adb 服务")
        device.shell('start adbd')
        logging.info("启动 adb 服务")

        # 获取设备IP地址列表
        ip_addresses = get_device_ip_address(device_id)
        if not ip_addresses:
            logging.warning("无法获取设备 IP 地址,无法连接到无线调试端口")
            return {'success': False, 'error': '无法获取设备 IP 地址'}

        # 尝试连接对应的IP地址
        retries = 0
        for ip_addr in ip_addresses:
            port = '5555'
            connect_cmd = f"adb connect {ip_addr}:{port}"
            try:
                subprocess.run(connect_cmd, shell=True, check=True)
                logging.info(f"已连接到设备的无线调试端口: {ip_addr}:{port}")

                # 发送验证命令
                verify_cmd = f"adb -s {device_id} shell echo hello"
                verify_result = subprocess.run(verify_cmd, shell=True, capture_output=True)
                if verify_result.returncode == 0:
                    logging.info("设备处于无线调试状态")
                    return {'success': True}
                else:
                    logging.warning("设备未能正常响应验证命令，可能无线调试失败")
                    return {'success': False, 'error': '设备未能正常响应验证命令，可能无线调试失败'}

            except subprocess.CalledProcessError as e:
                if "10061" in str(e):  # 目标计算机积极拒绝连接错误
                    # 重新设置TCP端口
<<<<<<< HEAD
                    device.shell(f'adb -s {device_id} tcpip 5555')
                    logging.info(f"已重新设置设备 {device_id} 的无线调试端口为：5555")
=======
                    device.shell('setprop service.adb.tcp.port 5555')
                    logging.info("重新设置 service.adb.tcp.port 为 5555")
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
                    retries += 1
                    if retries >= max_retries:
                        logging.warning(f"已达到最大重试次数 ({max_retries}), 无法连接到任何 IP 地址的无线调试端口")
                        return {'success': False, 'error': f"已达到最大重试次数 ({max_retries}), 无法连接到无线调试端口"}
                    else:
                        continue  # 继续尝试连接
                logging.warning(f"无法连接到 {ip_addr}:{port}, 错误: {e}")

        logging.warning("无法连接到任何 IP 地址的无线调试端口")
        return {'success': False, 'error': '无法连接到无线调试端口'}

    except subprocess.CalledProcessError as e:
        logging.error(f"执行 adb 命令失败: {e}")
        return {'success': False, 'error': str(e)}
    except Exception as e:
        logging.error(f"启用无线调试失败: {e}")
        return {'success': False, 'error': str(e)}


# 关闭无线调试
def disable_wireless_debugging(device_id, max_retries=3):
    try:
        logging.info(f"正在为设备 {device_id} 禁用无线调试...")
        device = adbutils.adb.device(device_id)

<<<<<<< HEAD
        # 获取设备端口号
        cmd = f"adb -s {device_id} shell getprop service.adb.tcp.port"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            logging.warning(f"无法获取设备端口号,无法断开无线调试连接: {result.stderr}")
            return {'success': False, 'error': '无法获取设备端口号'}
        port = int(result.stdout.strip())
        logging.info(f"设备端口号为 {port}")

=======
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
        # 获取设备IP地址列表
        ip_addresses = get_device_ip_address(device_id)
        if not ip_addresses:
            logging.warning("无法获取设备 IP 地址,无法断开无线调试连接")
            return {'success': False, 'error': '无法获取设备 IP 地址'}

<<<<<<< HEAD
=======
        port = '5555'

>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
        # 关闭设备端的无线调试选项
        device.shell('stop adbd')
        logging.info("停止 adb 服务")
        device.shell('start adbd')
        logging.info("启动 adb 服务")

        # 断开对应IP地址的无线连接
<<<<<<< HEAD
        disconnected = False
        for ip_addr in ip_addresses:
            retries = 0
            while retries < max_retries:
                disconnect_cmd = f"adb disconnect {ip_addr}:{port}"
                try:
                    subprocess.run(disconnect_cmd, shell=True, check=True)
                    logging.info(f"已断开与设备 {ip_addr}:{port} 的无线连接")
                    disconnected = True
                    break
                except subprocess.CalledProcessError as e:
                    if "10061" in str(e):  # 目标计算机积极拒绝连接错误
                        retries += 1
                        if retries >= max_retries:
                            logging.warning(f"已达到最大重试次数 ({max_retries}), 无法断开与 {ip_addr}:{port} 的无线连接")
                        else:
                            # 重新激活无线调试端口
                            device.shell(f'adb -s {device_id} tcpip {port}')
                            logging.info(f"已重新设置设备 {device_id} 的无线调试端口为：{port}")
                            continue  # 继续尝试断开连接
                    else:
                        logging.warning(f"无法断开与 {ip_addr}:{port} 的连接, 错误: {e}")
                        break

        if disconnected:
            logging.info("无线调试已禁用")
            return {'success': True}
        else:
            logging.warning("无法断开与任何 IP 地址的无线连接")
            return {'success': False, 'error': "无法断开与任何 IP 地址的无线连接"}

=======
        retries = 0
        for ip_addr in ip_addresses:
            disconnect_cmd = f"adb disconnect {ip_addr}:{port}"
            try:
                subprocess.run(disconnect_cmd, shell=True, check=True)
                logging.info(f"已断开与设备 {ip_addr}:{port} 的无线连接")
            except subprocess.CalledProcessError as e:
                if "10061" in str(e):  # 目标计算机积极拒绝连接错误
                    # 重新设置TCP端口
                    device.shell('setprop service.adb.tcp.port 5555')
                    logging.info("重新设置 service.adb.tcp.port 为 5555")
                    retries += 1
                    if retries >= max_retries:
                        logging.warning(f"已达到最大重试次数 ({max_retries}), 无法断开与任何 IP 地址的无线连接")
                        return {'success': False, 'error': f"已达到最大重试次数 ({max_retries}), 无法断开与任何 IP 地址的无线连接"}
                    else:
                        continue  # 继续断开连接
                logging.warning(f"无法断开与 {ip_addr}:{port} 的连接, 错误: {e}")

        logging.info("无线调试已禁用")
        return {'success': True}
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
    except subprocess.CalledProcessError as e:
        logging.error(f"执行 adb 命令失败: {e}")
        return {'success': False, 'error': str(e)}
    except Exception as e:
        logging.error(f"禁用无线调试失败: {e}")
        return {'success': False, 'error': str(e)}


# 获取scrcpy启动路径
def get_scrcpy_executable_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    system_bits = platform.architecture()[0]
    base_path = os.path.join(script_dir, "Pconfigure")
    if system_bits == '64bit':
        return os.path.join(base_path, "scrcpy-win64-v2.4", "scrcpy.exe")
    else:
        return os.path.join(base_path, "scrcpy-win32-v2.4", "scrcpy.exe")


# 启用互动投屏功能
def start_scrcpy(device_id):
    try:
        scrcpy_path = get_scrcpy_executable_path()
        logging.info(f"选择的scrcpy路径: {scrcpy_path}")
        command = [scrcpy_path, '-s', str(device_id)]
        subprocess.Popen(command, shell=True)
        logging.info("scrcpy 启动成功")
        return {'success': True}, 200
    except Exception as e:
<<<<<<< HEAD
        logging.exception("scrcpy启动失败")
=======
        logging.exception("启动scrcpy失败")
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
        return {'success': False, 'error': str(e)}, 500


# 停用互动投屏功能
def stop_scrcpy():
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            # 使用 name() 方法获取进程名称
            if proc.name() == 'scrcpy.exe':
                proc.terminate()
                return {'success': True}, 200

<<<<<<< HEAD
        # 如果没有找到名为'scrcpy'的进程
        return {'success': False, 'error': 'scrcpy 进程未找到'}, 200
    except Exception as e:
        logging.exception("scrcpy停用失败")
        return {'success': False, 'error': str(e)}, 500


# 获取 bundletool.jar 的路径
def get_bundletool_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bundletool_path = os.path.join(script_dir, 'aab_conversion', 'bundletool.jar')
    logging.info(f"bundletool.jar 路径设置为: {bundletool_path}")
    return bundletool_path


# 获取证书变量文件路径
def get_certificate_var_file_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    certificate_var_file = os.path.join(
        script_dir,
        'aab_conversion',
        'certificate_folder',
        'certificate_var',
        'certificate_var.json'
    )
    logging.info(f"证书变量文件路径设置为: {certificate_var_file}")
    return certificate_var_file


# 获取证书信息
def get_certificate_info(display_name):
    certificate_var_file_path = get_certificate_var_file_path()
    try:
        with open(certificate_var_file_path, 'r') as f:
            certificate_vars = json.load(f)
            for entry in certificate_vars:
                if entry['display_name'] == display_name:
                    logging.info(f"找到匹配的证书信息: {display_name}")
                    return entry
            logging.warning(f"未找到匹配的证书信息: {display_name}")
    except IOError as e:
        logging.error(f"读取证书配置文件时发生错误: {e}")
    return None


# 执行AAB上传并转换
def convert_aab(filename, display_name):
    logging.info(f'开始转换aab文件: {filename}')
    bundletool_path = get_bundletool_path()
    if not os.path.exists(bundletool_path):
        logging.error('bundletool.jar 文件不存在，请检查路径')
        raise Exception('bundletool.jar 文件不存在，请检查路径')

    project_root = os.path.dirname(os.path.abspath(__file__))
    aab_conversion_folder = os.path.join(project_root, 'aab_conversion')
    download_folder = os.path.join(aab_conversion_folder, 'download_folder')
    upload_folder = os.path.join(aab_conversion_folder, 'upload_folder')
    certificate_folder = os.path.join(aab_conversion_folder, 'certificate_folder')

    aab_conversion_path = os.path.join(download_folder, filename)
    apks_conversion_path = os.path.join(upload_folder, filename.replace('.aab', '.apks'))
    apk_conversion_path = os.path.join(upload_folder, filename.replace('.aab', '.apk'))

    logging.info(f"当前aab文件存储路径为: {aab_conversion_path}")
    logging.info(f"当前apks文件存储路径为: {apks_conversion_path}")
    logging.info(f"当前apk文件存储路径为: {apk_conversion_path}")

    certificate_info = get_certificate_info(display_name)

    if not certificate_info:
        logging.error(f"未找到证书信息: {display_name}")
        return False

    # 使用 certificate_info 中的数据
    ks_path = os.path.join(certificate_folder, 'certificate_resources', certificate_info['name'])
    ks_pass = certificate_info['keystore_password']
    ks_key_alias = certificate_info['key_alias']
    ks_key_pass = certificate_info['key_password']

    logging.info('正在执行aab文件转换命令...')
    # 执行 AAB 转换命令
    command = [
        'java', '-jar', bundletool_path, 'build-apks',
        '--bundle', aab_conversion_path,
        '--output', apks_conversion_path,
        '--mode=universal',
        '--ks', ks_path,
        '--ks-pass', f'pass:{ks_pass}',
        '--ks-key-alias', ks_key_alias,
        '--key-pass', f'pass:{ks_key_pass}'
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        logging.info('aab文件转换成功!')
        # 成功转换 apks 文件后,将其解压并提取 apk 文件
        with zipfile.ZipFile(apks_conversion_path, 'r') as zip_ref:
            zip_ref.extractall(upload_folder)

        # 检查实际生成的 APK 文件路径
        apk_files = [f for f in os.listdir(upload_folder) if f.endswith('.apk')]
        if apk_files:
            actual_apk_path = os.path.join(upload_folder, apk_files[0])
            logging.info(f"实际生成的apk文件路径为: {actual_apk_path}")

            # 根据实际情况,修改 converted_apk_path 变量的赋值
            converted_apk_path = actual_apk_path.replace('.apk', '-universal.apk')
            os.rename(actual_apk_path, converted_apk_path)
        else:
            logging.error("没有找到生成的 APK 文件")
            return False

        try:
            # 生成新的文件名
            renamed_apk_path = os.path.join(upload_folder, f"{os.path.splitext(filename)[0]}.apk")

            # 检查实际生成的 APK 文件路径
            apk_files = [f for f in os.listdir(upload_folder) if f.endswith('.apk')]
            if apk_files:
                actual_apk_path = os.path.join(upload_folder, apk_files[0])
                logging.info(f"实际生成的apk文件路径为: {actual_apk_path}")

                # 重命名文件
                os.rename(actual_apk_path, renamed_apk_path)
                logging.info(f"已重命名文件为: {renamed_apk_path}")

            # 删除 toc.pb 文件
            toc_file_path = os.path.join(upload_folder, 'toc.pb')
            if os.path.exists(toc_file_path):
                os.remove(toc_file_path)
                logging.info(f"已删除文件: {toc_file_path}")

        except Exception as e:
            logging.error(f"处理文件时出现异常: {e}")

    else:
        logging.error(f'aab文件转换失败: {result.stderr}')
        return False

    return True


# 提供下载转换后的文件
def get_converted_files():
    aab_conversion_folder = os.path.join(os.path.dirname(__file__), 'aab_conversion')
    upload_folder = os.path.join(aab_conversion_folder, 'upload_folder')

    converted_files = []
    for root, dirs, files in os.walk(upload_folder):
        for file in files:
            converted_files.append(file)  # 只添加文件名
            logging.info(f"找到转换后的文件: {file}")
    return converted_files


# 定义随机证书密码
def generate_random_password(length=12):
    try:
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for _ in range(length))
        logging.info(f"生成的随机密码: {password}")
        return password
    except Exception as e:
        logging.error(f"生成随机密码时出错: {e}")
        raise


# 生成随机证书并配置相应文件
def generate_signature():
    try:
        # 检查 keytool 是否存在
        if not shutil.which("keytool"):
            logging.error("keytool 未找到，请确保已正确配置 JDK 并将其添加到系统 PATH 中。")
            return

        project_root = os.path.dirname(os.path.abspath(__file__))
        generate_path = os.path.join(project_root, "aab_conversion", "certificate_folder", "generate_random_signature")
        resources_path = os.path.join(project_root, "aab_conversion", "certificate_folder", "certificate_resources")
        var_path = os.path.join(project_root, "aab_conversion", "certificate_folder", "certificate_var")

        if not os.path.exists(generate_path):
            os.makedirs(generate_path)
        if not os.path.exists(resources_path):
            os.makedirs(resources_path)
        if not os.path.exists(var_path):
            os.makedirs(var_path)

        os.chdir(generate_path)
        timestamp = time.strftime('%Y%m%d%H%M%S')
        key_alias = f"randomkey_{timestamp}"
        key_password = generate_random_password()
        keystore_password = generate_random_password()
        keystore_file = os.path.join(generate_path, f"{key_alias}.jks")

        keytool_cmd = [
            "keytool", "-genkeypair",
            "-keystore", keystore_file,
            "-storetype", "JKS",
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", "10000",
            "-storepass", keystore_password,
            "-keypass", key_password,
            "-alias", key_alias,
            "-dname", "CN=Unknown, OU=Unknown, O=Unknown, L=Unknown, S=Unknown, C=Unknown"
        ]

        subprocess.run(keytool_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # 复制jks文件到 certificate_resources 文件夹
        shutil.copy(keystore_file, os.path.join(resources_path, f"{key_alias}.jks"))

        logging.info("签名证书生成成功！")
        logging.info(f"签名信息存储路径为: {generate_path}/{key_alias}.jks")
        logging.info(f"签名日志信息存储路径为: {generate_path}/{key_alias}_info.txt")

        # 写入签名信息到日志文件
        signature_info_path = os.path.join(generate_path, f"{key_alias}_info.txt")
        with open(signature_info_path, "w", encoding='utf-8') as f:
            f.write("生成签名时的日志信息:\n")
            f.write(f"keystore password: {keystore_password}\n")
            f.write(f"key alias: {key_alias}\n")
            f.write(f"key password: {key_password}\n")

        # 读取签名参数信息并追加到 certificate_var.json 文件
        certificate_var_path = os.path.join(var_path, "certificate_var.json")
        certificate_info = {
            "display_name": f"A00000_{key_alias}",
            "name": f"{key_alias}.jks",
            "keystore_password": keystore_password,
            "key_alias": key_alias,
            "key_password": key_password
        }

        if os.path.exists(certificate_var_path):
            with open(certificate_var_path, "r", encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []

        data.append(certificate_info)

        with open(certificate_var_path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        clear_generate_random_signature_folder()  # <---如果需要保存生成随机证书的日志信息可注释掉此行代码
        return f"{key_alias}.jks"  # 返回证书名称

    except subprocess.CalledProcessError as e:
        logging.error(f"生成签名证书时出错: {e}")
    except Exception as e:
        logging.error(f"发生意外错误: {e}")

# 设备点击：电源、HOME、菜单、返回
def simulate_key_press(device_id, key):
    key_codes = {
        "power": 26,
        "home": 3,
        "menu": 82,
        "back": 4
    }
    try:
        device = adbutils.adb.device(device_id)
        device.shell(f"input keyevent {key_codes[key]}")
        logging.info(f"已模拟按下 {key} 键")
    except Exception as e:
        logging.error(f"模拟按键失败: {e}")


# 打开网址
def open_url(device_id, url):
    try:
        device = adbutils.adb.device(device_id)
        device.shell(f'am start -a android.intent.action.VIEW -d "{url}"')
        logging.info(f"已在设备 {device_id} 上打开网址: {url}")
    except Exception as e:
        logging.error(f"打开网址失败: {e}")


# 检测IP地址
def check_device_ip(device_id):
    try:
        device = adbutils.adb.device(device_id)
        device.shell('am start -a android.intent.action.VIEW -d "https://www.ipaddress.my"')
        logging.info(f"已在设备 {device_id} 上打开 IP 查看页面")
    except Exception as e:
        logging.error(f"查看设备 IP 失败: {e}")


# 清理应用缓存
def clear_app_cache(device_id, package_name):
    try:
        device = adbutils.adb.device(device_id)
        device.shell(f"pm clear {package_name}")
        logging.info(f"已清除应用 {package_name} 的缓存")
    except Exception as e:
        logging.error(f"清除应用缓存失败: {e}")


# 停止应用运行
def stop_app(device_id, package_name):
    try:
        device = adbutils.adb.device(device_id)
        device.shell(f"am force-stop {package_name}")
        logging.info(f"已停止应用 {package_name} 的运行")
    except Exception as e:
        logging.error(f"停止应用运行失败: {e}")

=======
        # 如果没有找到名为'scrcpy.exe'的进程
        return {'success': False, 'error': 'scrcpy 进程未找到'}, 200
    except Exception as e:
        logging.exception("停止scrcpy失败")
        return {'success': False, 'error': str(e)}, 500
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
