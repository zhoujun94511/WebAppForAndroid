import threading
import time
import webbrowser
import logging
import adb_utils
from flask import Flask, render_template, request, jsonify, abort
from adb_utils import uninstall_app, initialize_adb, get_new_device_info, get_windows, start_scrcpy, stop_scrcpy

# 初始化 Flask 应用
app = Flask(__name__)

# 设置应用程序的运行环境为开发模式
app.config['ENV'] = 'development'

# 启用调试模式
app.config['DEBUG'] = True

# 设置全局日志配置
logging.basicConfig(
    level=logging.INFO,  # 设置全局日志级别为 INFO，可以更改为其他级别
    format='%(asctime)s [%(levelname)s] %(message)s',  # 设置日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 设置日期时间格式
)


# 初始化服务
@app.before_first_request
def on_first_request():
    if not get_windows():
        # 如果不是Windows系统，终止初始化
        abort(400, "抱歉，当前应用仅支持Windows系统！！！")
    initialize_adb()


# 主页视图
@app.route('/')
def index():
    devices = adb_utils.get_devices()
    return render_template('index.html', devices=devices)


# 刷新设备列表
@app.route('/refresh', methods=['POST'])
def refresh():
    devices = adb_utils.get_devices()
    return jsonify(devices)


# 读取已安装应用
@app.route('/get_apps', methods=['POST'])
def get_apps():
    device_id = request.form.get('device_id')
    apps = adb_utils.get_installed_apps(device_id)
    return jsonify(apps)


# 卸载应用
@app.route('/uninstall_app', methods=['POST'])
def uninstall_app_route():
    device_id = request.form.get('device_id')
    package_name = request.form.get('package_name')
    result = uninstall_app(device_id, package_name)
    return jsonify(result)


# 安装 APK
@app.route('/install_apk', methods=['POST'])
def install_apk():
    device_id = request.form.get('device_id')
    apk_file = request.files.get('apk_file')
    result = adb_utils.install_apk(device_id, apk_file)
    return jsonify(result)


# 截图
@app.route('/screenshot', methods=['POST'])
def screenshot():
    device_id = request.form.get('device_id')
    result = adb_utils.take_screenshot(device_id)
    return jsonify(result)


# 录屏
@app.route('/record_screen', methods=['POST'])
def record_screen():
    device_id = request.form.get('device_id')
    duration = request.form.get('duration')
    result = adb_utils.record_screen(device_id, duration)
    return jsonify(result)


# 重启设备
@app.route('/restart_device', methods=['POST'])
def restart_device():
    device_id = request.form.get('device_id')
    result = adb_utils.restart_device(device_id)
    return jsonify(result)


# 获取设备信息
@app.route('/get_device_info', methods=['POST'])
def get_device_info_route():
    device_id = request.form.get('device_id')
    if not device_id:
        return jsonify({'success': False, 'error': 'Device ID not provided.'})
    try:
        device_info = get_new_device_info(device_id)
        if device_info:
            return jsonify({'success': True, **device_info})
        else:
            return jsonify({'success': False, 'error': 'Failed to get device info.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# 当前正在运行的应用信息
@app.route('/get_current_app_info', methods=['POST'])
def get_current_app_info_route():
    device_id = request.form.get('device_id')
    info = adb_utils.get_current_app_info(device_id)
    return jsonify(info)


# 启用无线调试
@app.route('/enable_wireless_debugging', methods=['POST'])
def enable_wireless_debugging():
    device_id = request.form.get('device_id')
    result = adb_utils.enable_wireless_debugging(device_id)
    return jsonify(result)


# 禁用无线调试
@app.route('/disable_wireless_debugging', methods=['POST'])
def disable_wireless_debugging():
    device_id = request.form.get('device_id')
    result = adb_utils.disable_wireless_debugging(device_id)
    return jsonify(result)


# # 启用投屏互动模式
# @app.route('/scrcpy', methods=['POST'])
# def start_scrcpy():
#     device_id = request.form.get('device_id')
#     if not device_id:
#         return jsonify({'success': False, 'error': 'Device ID not provided.'})
#
#     try:
#         # 指定 scrcpy.exe 的完整路径
#         scrcpy_exe_path = r'D:\Projectx\WebAppForAndroid\Pconfigure\scrcpy-win64-v2.4\scrcpy.exe'
#
#         # 执行 scrcpy 命令，指定设备 ID
#         scrcpy_command = f'"{scrcpy_exe_path}" -s {device_id}'
#         subprocess.Popen(scrcpy_command, shell=True)
#
#         return jsonify({'success': True})
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)})

# # 启用投屏互动模式
# @app.route('/scrcpy', methods=['POST'])
# def start_scrcpy():
#     script_dir_scrcpy = os.path.dirname(os.path.abspath(__file__))
#     logging.info(f"当前脚本所在目录: {script_dir_scrcpy}")
#     device_id = request.form.get('device_id')
#     logging.info(f"当前获取的设备ID为: {device_id}")
#     if not device_id:
#         return jsonify({'success': False, 'error': 'Device ID not provided.'})
#
#     try:
#         # 检测系统架构
#         system_bits = platform.architecture()[0]
#         logging.info(f"系统位数: {system_bits}")
#
#         # 构建 scrcpy-win32-v2.4 和 scrcpy-win64-v2.4 的完整路径
#         scrcpy_exe_path_32 = os.path.join(script_dir_scrcpy, "Pconfigure", "scrcpy-win32-v2.4", "scrcpy.exe")
#         scrcpy_exe_path_64 = os.path.join(script_dir_scrcpy, "Pconfigure", "scrcpy-win64-v2.4", "scrcpy.exe")
#
#         # 选择正确的scrcpy工具相对路径
#         scrcpy_exe_path = scrcpy_exe_path_64 if system_bits == '64bit' else scrcpy_exe_path_32
#         logging.info(f"选择的scrcpy路径: {scrcpy_exe_path}")
#
#         # 指定 scrcpy.exe 的完整路径
#         # scrcpy_exe_path = r'D:\Projectx\WebAppForAndroid\Pconfigure\scrcpy-win64-v2.4\scrcpy.exe'
#
#         # 执行 scrcpy 命令，指定设备 ID
#         scrcpy_command = f'"{scrcpy_exe_path}" -s {device_id}'
#         subprocess.Popen(scrcpy_command, shell=True)
#
#         return jsonify({'success': True})
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)})
#
#
# # 停用投屏互动模式
# @app.route('/stop_scrcpy', methods=['POST'])
# def stop_scrcpy():
#     try:
#         # 获取 scrcpy.exe 进程
#         for proc in psutil.process_iter():
#             if proc.name() == 'scrcpy.exe':
#                 # 终止 scrcpy.exe 进程
#                 proc.terminate()
#                 return jsonify({'success': True})
#
#         # 如果没有找到 scrcpy.exe 进程，返回失败信息
#         return jsonify({'success': False, 'error': 'scrcpy 进程未找到'})
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)})

# 启用投屏互动模式
@app.route('/scrcpy', methods=['POST'])
def start_scrcpy_route():
    device_id = request.form.get('device_id')
    if not device_id:
        return jsonify({'success': False, 'error': 'Device ID not provided.'}), 400

    result, status_code = start_scrcpy(device_id)
    return jsonify(result), status_code


# 停用投屏互动模式
@app.route('/stop_scrcpy', methods=['POST'])
def stop_scrcpy_route():
    result, status_code = stop_scrcpy()
    return jsonify(result), status_code


# 定义一个打开网页的函数
def open_browser():
    # 使用延迟确保 Flask 应用程序完全启动
    time.sleep(1)
    webbrowser.open_new_tab('http://localhost:5000')


if __name__ == '__main__':
    # 在 Flask 应用程序启动之前创建一个线程来打开浏览器
    if not hasattr(app, 'browser_opened') or not app.browser_opened:
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.start()
        app.browser_opened = True  # 标记浏览器已经打开

    # 运行 Flask 应用程序
    app.run(host='0.0.0.0', port=5000, use_reloader=False)
