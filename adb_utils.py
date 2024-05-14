import os
import shutil
import adbutils
import logging
import time
import subprocess
import tempfile
import re
import platform
import psutil


# 设置全局日志配置
logging.basicConfig(
    level=logging.INFO,  # 设置全局日志级别为 INFO，可以更改为其他级别
    format='%(asctime)s [%(levelname)s] %(message)s',  # 设置日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 设置日期时间格式
)


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
    logging.info('正在初始化 ADB 服务...')
    subprocess.run([adb_path, 'start-server'])

    # 检查 ADB 服务器状态
    result = subprocess.run([adb_path, 'devices'], capture_output=True, text=True)
    if 'List of devices attached' not in result.stdout:
        raise Exception('Failed to connect to ADB server.')
    logging.info('ADB 服务初始化完毕')


# 获取设备列表
def get_devices():
    try:
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
        return []


# 卸载应用
def uninstall_app(device_id, package_name):
    try:
        logging.info(f'正在卸载设备 {device_id} 上的应用 {package_name}...')
        if not device_id or not package_name:
            logging.warning('设备 ID 和包名是必需的')
            return {'success': False, 'error': '设备 ID 和包名是必需的'}

        device = adbutils.adb.device(device_id)
        device.uninstall(package_name)
        logging.info(f'应用 {package_name} 卸载成功')
        return {'success': True}
    except Exception as e:
        logging.error(f'卸载应用失败: {e}')
        return {'success': False, 'error': str(e)}


# 安装应用
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
    try:
        logging.info(f'正在为设备 {device_id} 截图...')
        device = adbutils.adb.device(device_id)

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
    except Exception as e:
        logging.error(f'截图失败: {e}')
        return {'success': False, 'error': str(e)}


# 录屏函数
def record_screen(device_id, duration):
    try:
        logging.info(f'正在为设备 {device_id} 录屏，时长: {duration} 秒...')
        duration = int(duration)
        device = adbutils.adb.device(device_id)

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
        logging.info(f'执行命令: {command}')

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

        # 高通芯片上的需要获取的参数列表
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
        # 如果既不是 MTK 也不是高通，则选择默认的 desired_properties_mtk
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
            logging.error('设备屏幕未亮，无法获取当前应用信息。')
            return {'success': False, 'error': '设备屏幕未亮，无法获取当前应用信息。'}

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
                    device.shell('setprop service.adb.tcp.port 5555')
                    logging.info("重新设置 service.adb.tcp.port 为 5555")
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

        # 获取设备IP地址列表
        ip_addresses = get_device_ip_address(device_id)
        if not ip_addresses:
            logging.warning("无法获取设备 IP 地址,无法断开无线调试连接")
            return {'success': False, 'error': '无法获取设备 IP 地址'}

        port = '5555'

        # 关闭设备端的无线调试选项
        device.shell('stop adbd')
        logging.info("停止 adb 服务")
        device.shell('start adbd')
        logging.info("启动 adb 服务")

        # 断开对应IP地址的无线连接
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
        logging.exception("启动scrcpy失败")
        return {'success': False, 'error': str(e)}, 500


# 停用互动投屏功能
def stop_scrcpy():
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            # 使用 name() 方法获取进程名称
            if proc.name() == 'scrcpy.exe':
                proc.terminate()
                return {'success': True}, 200

        # 如果没有找到名为'scrcpy.exe'的进程
        return {'success': False, 'error': 'scrcpy 进程未找到'}, 200
    except Exception as e:
        logging.exception("停止scrcpy失败")
        return {'success': False, 'error': str(e)}, 500
