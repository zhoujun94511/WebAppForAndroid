import os
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


#  创建截图和录屏存储目录。
def screenshot_and_record_folders():
    # 获取项目根目录
    screenshot_and_record_project_root = os.path.dirname(os.path.abspath(__file__))

    # 定义目录路径
    screenshot_and_record_folder = os.path.join(screenshot_and_record_project_root, 'screenshot_and_record')
    screenshot_folder = os.path.join(screenshot_and_record_folder, 'mobile_screenshot')
    record_folder = os.path.join(screenshot_and_record_folder, 'mobile_record')

    # 创建screenshot_and_record_folder目录路径（如不存在）
    os.makedirs(screenshot_and_record_folder, exist_ok=True)
    logging.info(f'创建截图与录屏存储路径为: {screenshot_and_record_folder}')

    # 创建截图文件目录路径（如不存在）
    os.makedirs(screenshot_folder, exist_ok=True)
    logging.info(f'创建截图存储路径为: {screenshot_folder}')

    # 创建录屏文件目录路径（如不存在）
    os.makedirs(record_folder, exist_ok=True)
    logging.info(f'创建录屏存储路径为: {record_folder}')

    return screenshot_and_record_folder, record_folder, screenshot_folder


# 创建 AAB 转换相关目录。
def create_aab_converted_directories():
    # 获取项目根目录
    aab_project_root = os.path.dirname(os.path.abspath(__file__))

    # 定义目录路径
    aab_conversion_folder = os.path.join(aab_project_root, 'aab_conversion')
    download_folder = os.path.join(aab_conversion_folder, 'download_folder')
    upload_folder = os.path.join(aab_conversion_folder, 'upload_folder')
    certificate_folder = os.path.join(aab_conversion_folder, 'certificate_folder')
    certificate_resources_folder = os.path.join(certificate_folder, 'certificate_resources')
    certificate_var_folder = os.path.join(certificate_folder, 'certificate_var')
    generate_random_signature_folder = os.path.join(certificate_folder, 'generate_random_signature')

    # 创建aab_conversion_folder目录（如不存在）
    os.makedirs(aab_conversion_folder, exist_ok=True)
    logging.info(f'创建 AAB 转换主目录: {aab_conversion_folder}')

    # 创建下载文件目录路径（如不存在）
    os.makedirs(download_folder, exist_ok=True)
    logging.info(f'创建下载文件夹路径为: {download_folder}')

    # 创建上传文件目录路径（如不存在）
    os.makedirs(upload_folder, exist_ok=True)
    logging.info(f'创建上传文件夹路径为: {upload_folder}')

    # 创建证书文件目录路径（如不存在）
    os.makedirs(certificate_folder, exist_ok=True)
    logging.info(f'创建证书文件夹路径为: {certificate_folder}')

    # 创建证书文件存储目录路径（如不存在）
    os.makedirs(certificate_resources_folder, exist_ok=True)
    logging.info(f'创建证书文件存储目录路径为: {certificate_resources_folder}')

    # 创建证书配置参数文件目录路径（如不存在）
    os.makedirs(certificate_var_folder, exist_ok=True)
    logging.info(f'创建证书配置参数文件目录路径为: {certificate_var_folder}')

    # 创建随机证书配置文件目录路径（如不存在）
    os.makedirs(generate_random_signature_folder, exist_ok=True)
    logging.info(f'创建随机证书配置文件目录路径为: {generate_random_signature_folder}')

    return aab_conversion_folder, download_folder, upload_folder, certificate_folder, certificate_resources_folder, certificate_var_folder, generate_random_signature_folder


# 清理aab生成使用过的文件夹
def clear_aab_folders():
    _, download_folder, upload_folder, _, _, _, _ = create_aab_converted_directories()
    download_folder_clean = download_folder
    upload_folder_clean = upload_folder
    logging.info(f'正在清理aab文件下载与上传文件夹...')
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
    _, _, _, _, _, _, generate_random_signature_folder = create_aab_converted_directories()
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
    _, record_folder, screenshot_folder = screenshot_and_record_folders()

    logging.info(f'正在清理截图与录屏文件夹...')

    # 清理screenshot文件夹
    for filename in os.listdir(screenshot_folder):
        file_path = os.path.join(screenshot_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                logging.info(f"已清理截图文件 {file_path}")
        except Exception as e:
            logging.error(f"清理截图文件夹 {file_path} 时出错: {e}")

    # 清理record文件夹
    for filename in os.listdir(record_folder):
        file_path = os.path.join(record_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                logging.info(f"已清理录屏文件 {file_path}")
        except Exception as e:
            logging.error(f"清理录屏文件夹 {file_path} 时出错: {e}")


#  定义Clipper应用读取目录
def clipper_folders_path():
    # 获取项目根目录
    clipper_apks_root_path = os.path.dirname(os.path.abspath(__file__))

    clipper_apks_path = os.path.join(clipper_apks_root_path, "static", "apks", "clipper_1.0.0.apk")
    logging.info(f"获取到当前Clipper应用所在目录是: {clipper_apks_path}")
    return clipper_apks_path

#  定义Xtestw文件读取目录
def xtest_folders_path():
    xtest_root_path = os.path.dirname(os.path.abspath(__file__))

    xtest_file_path = os.path.join(xtest_root_path, "static", "apks", "xtest-agent")
    logging.info(f"获取到当前Xtest文件所在目录是: {xtest_file_path}")
    return xtest_file_path

# 获取 bundletool.jar 的路径
def get_bundletool_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bundletool_path = os.path.join(script_dir, 'aab_conversion', 'bundletool.jar')
    logging.info(f"bundletool.jar 路径设置为: {bundletool_path}")
    return bundletool_path


# 获取证书变量文件路径
def get_certificate_var_file_path():
    _, _, _, _, _, certificate_var_folder, _ = create_aab_converted_directories()
    certificate_var_file = os.path.join(certificate_var_folder, 'certificate_var.json')
    logging.info(f"证书变量文件路径设置为: {certificate_var_file}")
    return certificate_var_file


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

    # 查询当前环境变量是否配置了adb
    adb_in_path = shutil.which("adb")

    if adb_in_path:
        adb_path = adb_in_path
    else:
        # 检测系统架构
        system_bits = platform.architecture()[0]
        logging.info(f"系统位数: {system_bits}")

        # 构建 scrcpy-win32-v2.4 和 scrcpy-win64-v2.6.1 的完整路径
        adb_path_32 = os.path.join(script_dir_adb, "Pconfigure", "scrcpy-win32-v2.6.1", "adb")
        adb_path_64 = os.path.join(script_dir_adb, "Pconfigure", "scrcpy-win64-v2.6.1", "adb")

        # 选择正确的 adb 工具路径
        adb_path = adb_path_64 if system_bits == '64bit' else adb_path_32
        logging.info(f"选择的ADB路径: {adb_path}")

    # 初始化adb服务
    logging.info('正在初始化ADB服务...')
    subprocess.run([adb_path, 'start-server'])

    # 检查 ADB 服务器状态
    result = subprocess.run([adb_path, 'devices'], capture_output=True, text=True)
    if 'List of devices attached' not in result.stdout:
        raise Exception('Failed to connect to ADB server.')
    logging.info('获取到ADB服务初始化完毕...')
    return adb_path


# 获取设备列表
def get_devices():
    try:
        logging.info('正在获取设备信息...')
        client = adbutils.AdbClient()
        devices = client.device_list()  # 使用 device_list 方法
        device_serials = [device.serial for device in devices]
        logging.info(f'获取到的设备列表信息是: {device_serials}')
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
        return []


# 卸载应用
def uninstall_app(device_id, package_name):
    try:
        logging.info(f'正在卸载设备 {device_id} 上的应用 {package_name}...')
        if not device_id or not package_name:
            logging.warning('设备ID和应用包名缺失')
            return {'success': False, 'error': '设备ID和包应用包名缺失'}

        device = adbutils.adb.device(device_id)
        device.uninstall(package_name)
        logging.info(f'应用 {package_name} 卸载成功')
        return {'success': True}
    except Exception as e:
        logging.error(f'卸载应用失败: {e}')
        return {'success': False, 'error': str(e)}

# 安装应用
def install_apk(device_id, apk_files):
    try:
        logging.info(f'正在为设备 {device_id} 安装应用文件...')
        device = adbutils.adb.device(device_id)
        adb_path = initialize_adb()
        results = []

        with tempfile.TemporaryDirectory() as temp_dir:
            standalone_apk_list = []  # 普通 APK 列表
            xapk_apk_groups = []  # XAPK 解压后的 APK 组

            for apk_file in apk_files:
                apk_filename = apk_file.filename.lower()

                if not (apk_filename.endswith('.apk') or apk_filename.endswith('.xapk')):
                    logging.warning(f'跳过非 APK/XAPK 文件: {apk_filename}')
                    results.append({'filename': apk_filename, 'success': False, 'error': '非APK或XAPK文件'})
                    continue

                apk_path = os.path.join(temp_dir, apk_file.filename)
                apk_file.save(apk_path)
                logging.info(f'{apk_path}文件已保存到临时文件夹！')

                if apk_filename.endswith('.apk'):
                    standalone_apk_list.append(apk_path)

                elif apk_filename.endswith('.xapk'):
                    # 处理 XAPK
                    try:
                        extracted_dir = os.path.join(temp_dir, apk_filename.replace('.xapk', ''))
                        os.makedirs(extracted_dir, exist_ok=True)

                        with zipfile.ZipFile(apk_path, 'r') as zip_ref:
                            zip_ref.extractall(extracted_dir)

                        extracted_apks = [os.path.join(extracted_dir, f) for f in os.listdir(extracted_dir) if f.endswith('.apk')]

                        if not extracted_apks:
                            logging.error(f'XAPK {apk_filename} 中未找到APK文件')
                            results.append({'filename': apk_filename, 'success': False, 'error': 'XAPK中未包含APK文件'})
                            continue

                        xapk_apk_groups.append(extracted_apks)
                        logging.info(f'XAPK {apk_filename} 解压成功，包含 {len(extracted_apks)} 个APK文件')

                    except Exception as e:
                        logging.error(f'解压 XAPK {apk_filename} 失败: {e}')
                        results.append({'filename': apk_filename, 'success': False, 'error': str(e)})

            for apk in standalone_apk_list:
                try:
                    device.install(apk)
                    logging.info(f'{apk}文件安装成功')
                    results.append({'filename': os.path.basename(apk), 'success': True})
                except Exception as e:
                    logging.error(f'{apk}文件安装失败: {e}')
                    results.append({'filename': os.path.basename(apk), 'success': False, 'error': str(e)})

            # 使用 adb install-multiple 安装 XAPK 拆分的 APK
            for split_apk_list in xapk_apk_groups:
                try:
                    cmd = [adb_path, "-s", device_id, "install-multiple", "-r", "-t"] + split_apk_list
                    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    logging.info(f'安装XAPK拆分的APK文件成功: {split_apk_list}')
                    results.append({'filename': f'XAPK ({len(split_apk_list)} APKs)', 'success': True})
                except subprocess.CalledProcessError as e:
                    logging.error(f'安装XAPK拆分的APK文件失败: {e.stderr}')
                    results.append({'filename': f'XAPK ({len(split_apk_list)} APKs)', 'success': False, 'error': e.stderr})

        return results

    except Exception as e:
        logging.error(f'安装应用过程中发生错误: {e}')
        return [{'filename': 'unknown', 'success': False, 'error': str(e)}]

# 截图函数
def take_screenshot(device_id):
    _, _, screenshot_folder = screenshot_and_record_folders()
    try:
        logging.info(f'正在为设备 {device_id} 截图...')
        device = adbutils.adb.device(device_id)

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
    except Exception as e:
        logging.error(f'截图失败: {e}')
        return {'success': False, 'error': str(e)}


# 录屏函数
def record_screen(device_id, duration):
    _, record_folder, _ = screenshot_and_record_folders()
    try:
        logging.info(f'正在为设备 {device_id} 录屏，时长: {duration} 秒...')
        duration = int(duration)
        device = adbutils.adb.device(device_id)

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
    _, record_folder, screenshot_folder = screenshot_and_record_folders()

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


# 使用adbutils重启设备
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
        # logging.info(f'执行命令: {command}')

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

        # 需要获取的参数列表（高通芯片）
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
            logging.error('设备屏幕已锁屏，无法获取当前应用信息，请解锁后重试。')
            return {'success': False, 'error': '设备屏幕已锁屏，无法获取当前应用信息，请解锁后重试。'}

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
        return None
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
        logging.info(f'当前获取到的设备IP是：{ip_addresses}')
        return ip_addresses
    except Exception as e:
        logging.error(f"获取设备 IP 地址失败: {e}")
        return []

# 开启无线调试
def enable_wireless_debugging(device_id):
    try:
        logging.info(f"正在为设备 {device_id} 启用无线调试...")
        device = adbutils.adb.device(device_id)

        # 设置 ADB 端口并重启 ADB
        device.shell(f'-s {device_id} setprop service.adb.tcp.port 5555')
        device.shell('stop adbd')
        device.shell('start adbd')

        # 获取设备 IP 地址
        ip_addresses = get_device_ip_address(device_id)
        if not ip_addresses:
            logging.error("无法获取设备 IP 地址")
            return {'success': False, 'error': '无法获取设备 IP 地址'}

        # 直接尝试连接第一个 IP
        ip_addr = ip_addresses[0]
        subprocess.run(["adb", "connect", f"{ip_addr}:5555"], check=True)
        logging.info(f"已连接到 {ip_addr}:5555")

        return {'success': True}
    except Exception as e:
        logging.error(f"启用无线调试失败: {e}")
        return {'success': False, 'error': str(e)}

# 停用无线调试
def disable_wireless_debugging(device_id):
    try:
        logging.info(f"正在为设备 {device_id} 停用无线调试...")

        # 获取设备的 IP 地址列表
        ip_addresses = get_device_ip_address(device_id)
        if not ip_addresses:
            logging.error("无法获取设备 IP 地址，无法断开无线连接")
            return {'success': False, 'error': '无法获取设备 IP 地址'}

        # 断开与设备的无线调试连接
        for ip_addr in ip_addresses:
            try:
                logging.info(f"尝试断开与设备 {ip_addr}:5555 的无线连接")
                subprocess.run(["adb", "-s", device_id, "disconnect", f"{ip_addr}:5555"], check=True)
                logging.info(f"已断开与设备 {ip_addr}:5555 的无线连接")
            except subprocess.CalledProcessError as e:
                logging.warning(f"无法断开与设备 {ip_addr}:5555 的连接, 错误: {e}")

        logging.info("无线调试已停用")
        return {'success': True}
    except Exception as e:
        logging.error(f"停用无线调试失败: {e}")
        return {'success': False, 'error': str(e)}


# 获取scrcpy启动路径
def get_scrcpy_executable_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    system_bits = platform.architecture()[0]
    base_path = os.path.join(script_dir, "Pconfigure")
    if system_bits == '64bit':
        return os.path.join(base_path, "scrcpy-win64-v2.6.1", "scrcpy.exe")
    else:
        return os.path.join(base_path, "scrcpy-win32-v2.6.1", "scrcpy.exe")


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
        logging.exception("scrcpy启动失败")
        return {'success': False, 'error': str(e)}, 500


# 停用互动投屏功能
def stop_scrcpy():
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            # 使用 name() 方法获取进程名称
            if proc.name() == 'scrcpy.exe':
                proc.terminate()
                return {'success': True}, 200

        # 如果没有找到名为'scrcpy'的进程
        return {'success': False, 'error': 'scrcpy 进程未找到'}, 200
    except Exception as e:
        logging.exception("scrcpy停用失败")
        return {'success': False, 'error': str(e)}, 500


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
    _, download_folder, upload_folder, certificate_folder, certificate_resources_folder, _, _ = create_aab_converted_directories()
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
    ks_path = os.path.join(certificate_resources_folder, certificate_info['name'])
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
    _, _, upload_folder, _, _, _, _ = create_aab_converted_directories()

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
            return None

        _, _, _, _, certificate_resources_folder, certificate_var_folder, generate_random_signature_folder = create_aab_converted_directories()

        generate_path = generate_random_signature_folder
        resources_path = certificate_resources_folder
        var_path = certificate_var_folder

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
        return None
    except Exception as e:
        logging.error(f"发生意外错误: {e}")
        return None


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
        logging.info(f"已操作{key}键")
    except Exception as e:
        logging.error(f"操作失败: {e}")


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


# 清理应用缓存并启动
def clear_app_cache(device_id, package_name):
    try:
        device = adbutils.adb.device(device_id)
        # 执行清除应用缓存的命令并启动应用
        device.shell(f"pm clear {package_name} && monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
        logging.info(f"已清除应用 {package_name} 的缓存并启动应用")
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

# 检查设备是否安装了Clipper应用
def check_clipper_installed(device_id):
    try:
        device = adbutils.adb.device(device_id)
        result = device.shell('pm list packages -3 | grep com.utils.clipper')
        return bool(result.strip())
    except Exception as e:
        logging.error(f"检查Clipper安装状态失败: {e}")
        return False


# 安装Clipper应用
def install_clipper(device_id):
    try:
        device = adbutils.adb.device(device_id)
        apk_path = clipper_folders_path()
        device.install(apk_path)
        logging.info("Clipper应用安装成功")
        return True
    except Exception as e:
        logging.error(f"安装Clipper应用失败: {e}")
        return False

# 启动Clipper应用
def start_clipper(device_id):
    try:
        device = adbutils.adb.device(device_id)

        # 先检查应用是否已安装
        if not check_clipper_installed(device_id):
            logging.error("Clipper应用未安装")
            return False

        # 启动应用
        device.shell('am start -n com.utils.clipper/com.utils.clipper.Main')

        # 等待应用启动并初始化，最多重试3次
        for i in range(3):
            time.sleep(1)  # 每次检查间隔1秒
            if is_clipper_running(device_id):
                logging.info(f"Clipper应用成功启动 (尝试{i + 1}次)")
                # 额外等待一秒确保应用完全初始化
                time.sleep(1)
                return True

        logging.error("Clipper应用启动超时")
        return False
    except Exception as e:
        logging.error(f"启动Clipper应用失败: {e}")
        return False

# 检查Clipper运行状态
def is_clipper_running(device_id):
    try:
        device = adbutils.adb.device(device_id)

        if not device.is_screen_on():
            logging.error('检测到设备屏幕已锁屏，请解锁后重试。')
            return False

        process_check = device.shell('pidof com.utils.clipper').strip()
        is_running = bool(process_check)

        window_focus = device.shell('dumpsys window | grep mCurrentFocus')
        is_foreground = 'com.utils.clipper' in window_focus

        if is_running and is_foreground:
            logging.info("Clipper正处于前台运行。")
            return True

        if is_running and not is_foreground:
            logging.info("Clipper在后台运行，但未在前台，尝试启动Clipper...")
        else:
            logging.info("Clipper未运行，尝试启动Clipper...")

        device.shell('am start -n com.utils.clipper/com.utils.clipper.Main')
        time.sleep(1)  # 等待 1 秒，确保应用启动

        window_focus = device.shell('dumpsys window | grep mCurrentFocus')
        if 'com.utils.clipper' in window_focus:
            logging.info("Clipper成功启动并进入前台。")
            return True
        else:
            logging.error("Clipper启动失败或未进入前台。")
            return False

    except Exception as e:
        logging.error(f"检查Clipper运行状态失败: {e}")
        return False

# 发送文本到设备剪贴板
def set_clipboard(device_id, text):
    try:
        # 确保应用正在运行
        if not is_clipper_running(device_id):
            logging.info("Clipper未运行，尝试启动...")
            if not start_clipper(device_id):
                logging.error("无法启动Clipper应用。")
                return False
            time.sleep(1)
        device = adbutils.adb.device(device_id)
        result = device.shell(f'am broadcast -a clipper.set -n com.utils.clipper/.ClipperReceiver -e text "{text}"')
        success = 'result=-1' in result and 'Text is copied into clipboard' in result

        if success:
            logging.info("成功设置剪贴板内容。")
        else:
            logging.error("设置剪贴板内容失败。")

        return success
    except Exception as e:
        logging.error(f"设置剪贴板内容失败: {e}")
        return False


# 获取设备剪贴板内容
def get_clipboard(device_id):
    try:
        # 确保应用正在运行
        if not is_clipper_running(device_id):
            logging.info("Clipper未运行，尝试启动...")
            if not start_clipper(device_id):
                logging.error("无法启动Clipper应用")
                return None
            time.sleep(1)  # 等待应用初始化

        device = adbutils.adb.device(device_id)
        result = device.shell('am broadcast -a clipper.get -n com.utils.clipper/.ClipperReceiver')

        # 检查广播结果
        if 'result=-1' not in result:
            logging.error("获取剪贴板广播失败")
            return None

        # 提取剪贴板内容
        match = re.search(r'data="([^"]*)"', result)
        if match:
            clipboard_text = match.group(1)
            logging.info(f"成功获取剪贴板内容: {clipboard_text[:1000]}...")  # 只记录前50个字符
            return clipboard_text
        else:
            logging.error("未找到剪贴板内容")
            return None

    except Exception as e:
        logging.error(f"获取剪贴板内容失败: {e}")
        return None

# 打开语言设置界面
def open_locale_settings(device_id):
    try:
        device = adbutils.adb.device(device_id)
        device.shell('am start -a android.settings.LOCALE_SETTINGS')
        logging.info(f"已在设备 {device_id} 上打开语言设置界面")
    except Exception as e:
        logging.error(f"打开语言设置界面失败: {e}")

# 检查是否存在Xtest文件
def check_xtest_exists_on_device(device_id):
    try:
        device = adbutils.adb.device(device_id)
        result = device.shell('ls /data/local/tmp/xtest-agent')
        return 'No such file' not in result and result.strip() != ''
    except Exception as e:
        logging.error(f"检查Xtest文件文件失败: {e}")
        return False

#将Xtest文件推送到设备
def push_xtest_to_device(device_id):
    xtest_file_path = xtest_folders_path()

    if not os.path.exists(xtest_file_path):
        logging.error(f"{xtest_file_path}路径下不存在Xtest文件")
        return False

    try:
        device = adbutils.adb.device(device_id)
        device.sync.push(xtest_file_path, '/data/local/tmp/xtest-agent')
        logging.error(f"对设备{device_id}推送Xtest文件成功")
        return True
    except Exception as e:
        logging.error(f"对设备{device_id}推送Xtest发生异常: {e}")
        return False

#设置Xtest文件权限
def set_xtest_permissions(device_id):
    try:
        device = adbutils.adb.device(device_id)
        device.shell('chmod 755 /data/local/tmp/xtest-agent')
        return True
    except Exception as e:
        logging.error(f"对设备{device_id}的Xtest权限设置发生异常: {e}")
        return False

#启动Xtest服务进程
def start_xtest_server(device_id):
    try:
        device = adbutils.adb.device(device_id)
        device.shell('/data/local/tmp/xtest-agent server -d')
        logging.error(f"设备{device_id}启用Xtest服务成功")
        return True
    except Exception as e:
        logging.error(f"设备{device_id}启用Xtest服务失败: {e}")
        return False

#停止Xtest服务进程
def stop_xtest_server(device_id):
    try:
        device = adbutils.adb.device(device_id)
        device.shell('/data/local/tmp/xtest-agent server --stop')
        logging.error(f"设备{device_id}停用Xtest服务成功")
        return True
    except Exception as e:
        logging.error(f"设备{device_id}停用Xtest服务失败: {e}")
        return False
