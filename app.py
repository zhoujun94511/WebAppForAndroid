import os
import json
import time
import datetime
import logging
import adb_utils
import threading
import webbrowser
from flask import Flask, render_template, request, jsonify, abort, send_from_directory, send_file
from adb_utils import uninstall_app, get_new_device_info, get_windows, start_scrcpy, stop_scrcpy, \
    get_local_ip

# 初始化 Flask 应用
app = Flask(__name__)

# 设置应用程序的运行环境为开发模式
app.config['ENV'] = 'development'

# 启用调试模式
app.config['DEBUG'] = True

# 设置全局日志配置
logging.basicConfig(
    level=logging.ERROR,  # 设置全局日志级别为 INFO，可以更改为其他级别
    format='%(asctime)s [%(levelname)s] %(message)s',  # 设置日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 设置日期时间格式
)


# 初始化服务
@app.before_request
def on_first_request():
    if not get_windows():
        # 如果不是Windows系统，终止初始化
        abort(400, "抱歉，当前应用仅支持Windows系统！！！")


# 主页视图
@app.route('/')
def index():
    adb_utils.initialize_adb()
    devices = adb_utils.get_devices()
    return render_template('index.html', devices=devices)


# favicon定义
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'wresource'), 'favicon.ico')


# 刷新设备列表
@app.route('/refresh', methods=['POST'])
def refresh():
    devices = adb_utils.get_devices()
    adb_utils.clear_screenshot_and_record_folders()
    return jsonify(devices)


# 获取已安装应用
@app.route('/get_apps', methods=['POST'])
def get_apps():
    device_id = request.form.get('device_id')
    apps = adb_utils.get_installed_apps(device_id)
    return jsonify(apps)


# 搜索已安装应用信息路由
@app.route('/search_apps', methods=['POST'])
def search_apps():
    device_id = request.form.get('device_id')
    query = request.form.get('query', '').lower()

    try:
        all_apps = adb_utils.get_installed_apps(device_id)
        matched_apps = [installed_app for installed_app in all_apps if query in installed_app.lower()]
        logging.info(f'搜索到 {len(matched_apps)} 个匹配的应用')
        return jsonify(matched_apps)
    except Exception as e:
        logging.error(f'搜索应用时发生错误: {e}')
        return jsonify({'error': str(e)}), 500


# 卸载应用
@app.route('/uninstall_app', methods=['POST'])
def uninstall_app_route():
    device_id = request.form.get('device_id')
    package_name = request.form.get('package_name')
    result = uninstall_app(device_id, package_name)
    return jsonify(result)


# 安装应用
@app.route('/install_apk', methods=['POST'])
def install_apk():
    device_id = request.form.get('device_id')
    apk_files = request.files.getlist('apk_files')

    if not apk_files:
        return jsonify({'success': False, 'error': '没有选择APK文件'})

    results = adb_utils.install_apk(device_id, apk_files)
    return jsonify(results)


# 截图
@app.route('/screenshot', methods=['POST'])
def screenshot():
    adb_utils.clear_screenshot_and_record_folders()
    device_id = request.form.get('device_id')
    result = adb_utils.take_screenshot(device_id)
    return jsonify(result)


# 录屏
@app.route('/record_screen', methods=['POST'])
def record_screen():
    adb_utils.clear_screenshot_and_record_folders()
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


# 获取转化aab证书变量路径
@app.route('/get_certificates')
def get_certificates():
    certificate_var_file_path = adb_utils.get_certificate_var_file_path()
    try:
        with open(certificate_var_file_path, 'r') as f:
            certificate_vars = json.load(f)

        display_name = request.args.get('display_name')

        if display_name:
            filtered_certificates = [cert for cert in certificate_vars if cert['display_name'] == display_name]
            return jsonify(filtered_certificates)
        else:
            return jsonify(certificate_vars)
    except Exception as e:
        app.logger.error(f'Error reading certificate variables: {e}')
        return jsonify({'error': 'Unable to read certificate variables'}), 500


# 获取证书信息
@app.route('/get_certificate_info')
def get_certificate_info_route():
    display_name = request.args.get('display_name')
    if not display_name:
        return jsonify({'error': 'Missing display_name parameter'}), 400

    certificate_info = adb_utils.get_certificate_info(display_name)
    if certificate_info is None:
        return jsonify({'error': 'Certificate not found'}), 404

    return jsonify(certificate_info)


# 上传aab文件的路由
@app.route('/upload_aab', methods=['POST'])
def upload_aab():
    adb_utils.clear_aab_folders()
    logging.info('接收到上传aab文件请求，正在处理中...')
    file = request.files['file']
    if file.filename == '':
        logging.info('No selected file')
        return jsonify({'success': False, 'error': 'No selected file'})
    if file and file.filename.endswith('.aab'):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{os.path.splitext(file.filename)[0]}_{timestamp}{file_extension}"

        # 确保下载文件夹存在
        download_folder = os.path.join(os.path.dirname(__file__), 'aab_conversion', 'download_folder')
        os.makedirs(download_folder, exist_ok=True)

        file_path = os.path.join(download_folder, unique_filename)
        file.save(file_path)
        logging.info(f'保存文件到 {file_path}')
        return jsonify({'success': True, 'filename': unique_filename})
    else:
        logging.info('不支持的文件格式!')
        return jsonify({'success': False, 'error': 'File format not supported'})


# 转化AAB文件的路由
@app.route('/convert_aab', methods=['POST'])
def convert_aab():
    filename = request.form.get('filename')
    display_name = request.form.get('displayName')

    logging.info(f"Received filename: {filename}, display_name: {display_name}")

    if not filename or not display_name:
        logging.info("Missing filename or display_name parameter")
        return jsonify({'error': 'Missing filename or display_name parameter'}), 400

    try:
        success = adb_utils.convert_aab(filename, display_name)
    except Exception as e:
        app.logger.error(f'Error during AAB conversion: {e}')
        return jsonify({'error': 'Error during AAB conversion'}), 500

    return jsonify({'success': success})


# 获取转化后文件列表的路由
@app.route('/get_converted_files', methods=['GET'])
def get_converted_files():
    files = adb_utils.get_converted_files()
    return jsonify(files)


# 用于下载文件的路由（截图、录屏、aab文件）
@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    if filename.startswith('screenshot_') or filename.startswith('screen_record_'):
        screenshot_and_record_folder, record_folder, screenshot_folder = adb_utils.screenshot_and_record_folders()

        if filename.startswith('screenshot_'):
            # file_path = os.path.join(screenshot_folder, filename)
            file_path = str(os.path.join(screenshot_folder, filename))
        else:  # filename.startswith('screen_record_')
            file_path = str(os.path.join(record_folder, filename))

    else:
        # 处理 aab 文件下载
        upload_folder = os.path.join(os.path.dirname(__file__), 'aab_conversion', 'upload_folder')
        file_path = os.path.join(upload_folder, filename)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True,
                         mimetype='video/mp4' if filename.endswith('.mp4') else None)
    else:
        logging.error(f'文件找不到: {filename}')
        return jsonify({'error': '文件找不到'})


# 生成随机证书并自动配置相关文件
@app.route('/generate_signature', methods=['POST'])
def generate_signature_route():
    try:
        certificate_name = adb_utils.generate_signature()
        if certificate_name:
            return jsonify({'success': True, 'certificateName': certificate_name})
        else:
            return jsonify({'success': False, 'error': 'Error generating signature'}), 500
    except Exception as e:
        app.logger.error(f'Error generating signature: {e}')
        return jsonify({'success': False, 'error': 'Error generating signature'}), 500


# 模拟点击：电源、HOME、菜单、返回
@app.route('/simulate_key_press', methods=['POST'])
def simulate_key_press():
    device_id = request.form.get('device_id')
    key = request.form.get('key')
    adb_utils.simulate_key_press(device_id, key)
    return jsonify({"status": "success"})


# 打开网址
@app.route('/open_url', methods=['POST'])
def open_url():
    device_id = request.form.get('device_id')
    url = request.form.get('url')
    adb_utils.open_url(device_id, url)
    return jsonify({"status": "success"})


# 检测IP地址
@app.route('/check_device_ip', methods=['POST'])
def check_device_ip():
    device_id = request.form.get('device_id')
    try:
        adb_utils.check_device_ip(device_id)
        return jsonify({"status": "success"})
    except Exception as e:
        logging.error(f"查看设备 IP 失败: {e}")
        return jsonify({"status": "error", "message":"查看设备 IP 失败"})


# 清理应用缓存
@app.route('/clear_app_cache', methods=['POST'])
def clear_app_cache():
    device_id = request.form.get('device_id')
    package_name = request.form.get('package_name')
    adb_utils.clear_app_cache(device_id, package_name)
    return jsonify({"status": "success"})


# 停止应用运行
@app.route('/stop_app', methods=['POST'])
def stop_app():
    device_id = request.form.get('device_id')
    package_name = request.form.get('package_name')
    adb_utils.stop_app(device_id, package_name)
    return jsonify({"status": "success"})

# 检测clipper应用安装状态
@app.route('/check_clipper', methods=['POST'])
def check_clipper():
    device_id = request.form.get('device_id')
    if not device_id:
        return jsonify({"status": "error", "message": "未选择设备"})

    # 检查是否已安装
    installed = adb_utils.check_clipper_installed(device_id)
    if not installed:
        success = adb_utils.install_clipper(device_id)
        if not success:
            return jsonify({"status": "error", "message": "Clipper安装失败"})
        time.sleep(1)  # 等待安装完成

    # 检查是否正在运行，如果没有运行则启动
    if not adb_utils.is_clipper_running(device_id):
        success = adb_utils.start_clipper(device_id)
        if not success:
            return jsonify({"status": "error", "message": "Clipper启动失败"})

    return jsonify({"status": "success"})

# 发送信息到设备粘贴板
@app.route('/set_clipboard', methods=['POST'])
def set_clipboard_route():
    device_id = request.form.get('device_id')
    text = request.form.get('text')
    if not device_id or not text:
        return jsonify({"status": "error", "message": "参数不完整"})

    # 检查应用状态并设置剪贴板
    success = adb_utils.set_clipboard(device_id, text)
    if not success:
        return jsonify({"status": "error", "message": "设置剪贴板失败"})

    return jsonify({"status": "success"})

# 从设备粘贴板获取信息
@app.route('/get_clipboard', methods=['POST'])
def get_clipboard_route():
    device_id = request.form.get('device_id')
    if not device_id:
        return jsonify({"status": "error", "message": "未选择设备"})

    # 获取剪贴板内容
    text = adb_utils.get_clipboard(device_id)
    if text is None:
        return jsonify({"status": "error", "message": "获取剪贴板内容失败"})

    return jsonify({"status": "success", "text": text})

# 打开语言设置界面
@app.route('/open_locale_settings', methods=['POST'])
def open_locale_settings():
    device_id = request.form.get('device_id')
    try:
        adb_utils.open_locale_settings(device_id)
        return jsonify({"status": "success"})
    except Exception as e:
        logging.error(f"打开语言设置失败: {e}")
        return jsonify({"status": "error", "message": "打开语言设置失败"})

# 定义一个打开网页的函数
use_local_ip = get_local_ip()
def open_browser():
     # 使用延迟确保 Flask 应用程序完全启动
     time.sleep(1)
     webbrowser.open_new_tab(f'http://{use_local_ip}:5001')


if __name__ == '__main__':
    # 在 Flask 应用程序启动之前创建一个线程来打开浏览器
    if not hasattr(app, 'browser_opened') or not app.browser_opened:
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.start()
        app.browser_opened = True  # 标记浏览器已经打开

    # 运行 Flask 应用程序
    app.run(host=use_local_ip, port=5001, debug=True, use_reloader=False)
