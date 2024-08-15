import adbutils


def get_app_names():
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)

    devices = adb.device_list()
    if not devices:
        print('No devices connected')
        return []

    device = devices[0]  # 使用第一个连接的设备

    app_names = []
    packages = device.shell("pm list packages -f").splitlines()

    for package in packages:
        if package.strip():
            # 提取包名
            apk_path, package_name = package.split(':')[1].split('=')

            # 使用 aapt 命令获取应用名称
            cmd = f"aapt dump badging {apk_path} | grep 'application-label:'"
            result = device.shell(cmd)

            if result:
                app_name = result.split("'")[1]
                app_names.append((package_name, app_name))
            else:
                # 如果 aapt 无法获取名称，尝试使用 dumpsys
                cmd = f"dumpsys package {package_name} | grep 'applicationInfo'"
                result = device.shell(cmd)
                for line in result.splitlines():
                    if "label=" in line:
                        app_name = line.split("label=")[1].split(" ")[0]
                        app_names.append((package_name, app_name))
                        break

    return app_names


# 运行函数并打印结果
app_list = get_app_names()
for package_name, app_name in app_list:
    print(f"Package: {package_name}, Name: {app_name}")