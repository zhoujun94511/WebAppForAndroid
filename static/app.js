// 刷新设备列表
function refreshDevices() {
    const refreshDevicesButton = $('#refresh-devices-button');
    refreshDevicesButton.prop('disabled', true);

    $.post('/refresh', function(data) {
        const deviceSelect = $('#device-select');
        deviceSelect.empty();

        if (data.length === 0) {
            Swal.fire({
                icon: 'warning',
                title: '未检测到设备',
                text: '请检查连接。',
                confirmButtonText: '确定'
            });
        } else {
            deviceSelect.html(data.map(device => `<option value="${device}">${device}</option>`).join(''));
        }
    }).fail(function() {
        Swal.fire({
            icon: 'error',
            title: '刷新设备列表时发生错误',
            text: '请检查网络连接。',
            confirmButtonText: '确定'
        });
    }).always(function() {
        refreshDevicesButton.prop('disabled', false);
    });
}

// 获取设备信息
function getDeviceInfo() {
    const getDeviceInfoButton = $('#get-device-info-button');
    getDeviceInfoButton.prop('disabled', true);

    const deviceId = $('#device-select').val();

    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备',
            text: '请选择设备。',
            confirmButtonText: '确定'
        });
        getDeviceInfoButton.prop('disabled', false);
        return;
    }

    $.post('/get_device_info', { device_id: deviceId })
        .done(function(data) {
            if (data.error) {
                Swal.fire({
                    icon: 'error',
                    title: '获取设备信息失败',
                    text: data.error,
                    confirmButtonText: '确定'
                });
            } else {
                displayDeviceInfo(data);
            }
        })
        .fail(function() {
            Swal.fire({
                icon: 'error',
                title: '获取设备信息时发生错误',
                confirmButtonText: '确定'
            });
        })
        .always(function() {
            getDeviceInfoButton.prop('disabled', false);
        });
}

// 显示设备信息
function displayDeviceInfo(deviceInfo) {
    const deviceInfoDiv = $('#device-info');
    deviceInfoDiv.empty();

    const displayOrder = [
        '设备名称',
        '设备品牌',
        '安卓版本',
        'SDK版本',
        'CPU品牌',
        'CPU型号',
        'CPU架构',
        '设备序列号'
    ];

    const htmlContent = displayOrder.map(key => {
        if (deviceInfo.hasOwnProperty(key)) {
            return `<div><strong>${key}:</strong> ${deviceInfo[key]}</div>`;
        }
        return '';
    }).join('');

    deviceInfoDiv.append(htmlContent);
}

// 假设 installedApps 是一个数组，包含所有已安装的应用包名
let installedApps = [];

// 初始化已安装应用列表
function getInstalledApps() {
    const getInstalledAppsButton = $('#get-installed-apps-button');
    getInstalledAppsButton.prop('disabled', true);

    const deviceId = $('#device-select').val();

    $.post('/get_apps', { device_id: deviceId }, function(data) {
        if (data && data.length > 0) {
            installedApps = data; // 将获取到的应用包名列表存储到 installedApps 中
            updateAppSelect(installedApps);
        } else {
            Swal.fire({
                icon: 'warning',
                title: '未能获取到已安装的应用程序',
                confirmButtonText: '确定'
            });
        }
    }).fail(function() {
        Swal.fire({
            icon: 'error',
            title: '获取已安装的应用程序失败',
            confirmButtonText: '确定'
        });
    }).always(function() {
        getInstalledAppsButton.prop('disabled', false);
    });
}

// 更新选择框内容
function updateAppSelect(apps) {
    const appSelect = $('#app-select');
    appSelect.empty();
    apps.forEach(app => {
        const option = new Option(app, app);
        appSelect.append(option);
    });
}

// 在输入事件中调用 searchApps
$('#app-search-input').on('input', function() {
    const query = $(this).val().toLowerCase();
    searchApps(query);
});

// 使用 filter 方法实现搜索
function searchApps(query) {
    // 根据查询参数在 installedApps 列表中过滤包名
    const filteredApps = installedApps.filter(app => app.toLowerCase().includes(query));
    // 将过滤后的结果显示在选择框中
    updateAppSelect(filteredApps);
}

// 卸载应用程序
function uninstallApp() {
    const uninstallAppButton = $('#uninstall-app-button');
    uninstallAppButton.prop('disabled', true);

    const deviceId = $('#device-select').val();
    const packageName = $('#app-select').val();

    if (!deviceId || !packageName) {
        Swal.fire({
            icon: 'warning',
            title: '请选择要卸载的设备和应用程序。',
            confirmButtonText: '确定'
        });
        uninstallAppButton.prop('disabled', false);
        return;
    }

    // 二次确认
    Swal.fire({
        title: '确认',
        text: `您确定要卸载包名为 ${packageName} 的应用程序吗？`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: '确定',
        cancelButtonText: '取消'
    }).then((result) => {
        if (result.isConfirmed) {
            $.post('/uninstall_app', { device_id: deviceId, package_name: packageName })
                .done(function(response) {
                    if (response.success) {
                        Swal.fire({
                            icon: 'success',
                            title: '应用程序卸载成功。',
                            confirmButtonText: '确定'
                        });
                        getInstalledApps();
                    } else {
                        Swal.fire({
                            icon: 'error',
                            title: '无法卸载应用',
                            text: response.error,
                            confirmButtonText: '确定'
                        });
                    }
                })
                .fail(function() {
                    Swal.fire({
                        icon: 'error',
                        title: '错误',
                        text: '无法卸载应用程序。',
                        confirmButtonText: '确定'
                    });
                })
                .always(function() {
                    uninstallAppButton.prop('disabled', false);
                });
        } else {
            uninstallAppButton.prop('disabled', false);
        }
    });
}

// 安装 APK 文件
function installApk() {
    const installApkButton = $('#install-apk-button');
    installApkButton.prop('disabled', true);

    const deviceId = $('#device-select').val();
    const apkFile = $('#apk-file')[0].files[0];

    if (!apkFile) {
        Swal.fire({
            icon: 'warning',
            title: '请先选择一个 APK 文件。',
            confirmButtonText: '确定'
        });
        installApkButton.prop('disabled', false);
        return;
    }

    if (!apkFile.name.toLowerCase().endsWith('.apk')) {
        Swal.fire({
            icon: 'warning',
            title: '请选择一个 .apk 文件。',
            confirmButtonText: '确定'
        });
        installApkButton.prop('disabled', false);
        return;
    }

    const formData = new FormData();
    formData.append('device_id', deviceId);
    formData.append('apk_file', apkFile);

    $.ajax({
        url: '/install_apk',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            Swal.fire({
                icon: data.success ? 'success' : 'error',
                title: data.success ? 'APK 安装成功' : 'APK 安装失败',
                text: data.success ? '' : data.error,
                confirmButtonText: '确定'
            });
        },
        error: function() {
            Swal.fire({
                icon: 'error',
                title: '错误',
                text: '无法安装 APK',
                confirmButtonText: '确定'
            });
        }
    }).always(function() {
        installApkButton.prop('disabled', false);
    });
}

// 截图函数
function takeScreenshot() {
    const takeScreenshotButton = $('#take-screenshot-button');
    takeScreenshotButton.prop('disabled', true);

    const deviceId = $('#device-select').val();
    $.post('/screenshot', { device_id: deviceId }, function(data) {
        if (data.success) {
            Swal.fire({
                icon: 'success',
                title: '截图成功！',
                text: `路径：${data.path}`,
                confirmButtonText: '确定'
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: '截图失败',
                text: data.error,
                confirmButtonText: '确定'
            });
        }
    }).always(function() {
        takeScreenshotButton.prop('disabled', false);
    });
}

// 屏幕录制函数
function recordScreen() {
    const recordScreenButton = $('#record-screen-button');
    recordScreenButton.prop('disabled', true);

    const deviceId = $('#device-select').val();
    const duration = prompt('请输入录屏时长（秒）：');

    if (!duration) {
        Swal.fire({
            icon: 'warning',
            title: '请输入录屏时长。',
            confirmButtonText: '确定'
        });
        recordScreenButton.prop('disabled', false);
        return;
    }

    $.post('/record_screen', { device_id: deviceId, duration: duration }, function(data) {
        if (data.success) {
            Swal.fire({
                icon: 'success',
                title: '录屏成功！',
                text: `路径：${data.path}`,
                confirmButtonText: '确定'
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: '录屏失败',
                text: data.error,
                confirmButtonText: '确定'
            });
        }
    }).always(function() {
        recordScreenButton.prop('disabled', false);
    });
}

// 重启设备函数
function restartDevice() {
    const restartDeviceButton = $('#restart-device-button');
    restartDeviceButton.prop('disabled', true);

    const deviceId = $('#device-select').val();

    $.post('/restart_device', { device_id: deviceId }, function(data) {
        if (data.success) {
            Swal.fire({
                icon: 'success',
                title: '设备已重启。',
                confirmButtonText: '确定'
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: '设备重启失败',
                text: data.error,
                confirmButtonText: '确定'
            });
        }
    }).always(function() {
        restartDeviceButton.prop('disabled', false);
    });
}

// 获取当前应用程序信息
function getCurrentAppInfo() {
    const getCurrentAppInfoButton = $('#get-current-app-info-button');
    getCurrentAppInfoButton.prop('disabled', true);

    const deviceId = $('#device-select').val();

    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备。',
            confirmButtonText: '确定'
        });
        getCurrentAppInfoButton.prop('disabled', false);
        return;
    }

    $.post('/get_current_app_info', { device_id: deviceId }, function(data) {
        const appInfoDiv = $('#current-app-info');
        appInfoDiv.empty();

        if (data.success) {
            appInfoDiv.append(`<div><strong>Package Name:</strong> ${data.package_name}</div>`);
            appInfoDiv.append(`<div><strong>Activity Name:</strong> ${data.activity_name}</div>`);
            appInfoDiv.append(`<div><strong>Start Activity Name:</strong> ${data.start_activity_name}</div>`);
        } else {
            Swal.fire({
                icon: 'error',
                title: '获取当前应用信息失败',
                text: data.error,
                confirmButtonText: '确定'
            });
        }
    }).fail(function() {
        Swal.fire({
            icon: 'error',
            title: '错误',
            text: '无法获取当前应用程序信息！',
            confirmButtonText: '确定'
        });
    }).always(function() {
        getCurrentAppInfoButton.prop('disabled', false);
    });
}

// 启用无线调试
function enableWirelessDebugging() {
    const enableWirelessDebuggingButton = $('#enable-wireless-debugging-button');
    enableWirelessDebuggingButton.prop('disabled', true);

    const deviceId = $('#device-select').val();

    $.post('/enable_wireless_debugging', { device_id: deviceId }, function(data) {
        if (data.success) {
            Swal.fire({
                icon: 'success',
                title: '无线调试已启用。',
                confirmButtonText: '确定'
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: '启用无线调试失败。',
                text: data.error,
                confirmButtonText: '确定'
            });
        }
    }).always(function() {
        enableWirelessDebuggingButton.prop('disabled', false);
    });
}

// 禁用无线调试
function disableWirelessDebugging() {
    const disableWirelessDebuggingButton = $('#disable-wireless-debugging-button');
    disableWirelessDebuggingButton.prop('disabled', true);

    const deviceId = $('#device-select').val();

    $.post('/disable_wireless_debugging', { device_id: deviceId }, function(data) {
        if (data.success) {
            Swal.fire({
                icon: 'success',
                title: '无线调试已禁用。',
                confirmButtonText: '确定'
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: '禁用无线调试失败。',
                text: data.error,
                confirmButtonText: '确定'
            });
        }
    }).always(function() {
        disableWirelessDebuggingButton.prop('disabled', false);
    });
}

// 启用投屏互动模式
function startScrcpy() {
    const startScrcpyButton = $('#start-scrcpy-button');
    startScrcpyButton.prop('disabled', true);

    const deviceId = $('#device-select').val();

    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备。',
            confirmButtonText: '确定'
        });
        startScrcpyButton.prop('disabled', false);
        return;
    }

    $.post('/scrcpy', { device_id: deviceId }, function(data) {
        if (data.success) {
            Swal.fire({
                icon: 'success',
                title: 'scrcpy 已启动。',
                confirmButtonText: '确定'
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: '启动 scrcpy 失败',
                text: data.error,
                confirmButtonText: '确定'
            });
        }
    }).always(function() {
        startScrcpyButton.prop('disabled', false);
    });
}

// 停用投屏互动模式
function stopScrcpy() {
    const stopScrcpyButton = $('#stop-scrcpy-button');
    stopScrcpyButton.prop('disabled', true);

    $.post('/stop_scrcpy', function(data) {
        if (data.success) {
            Swal.fire({
                icon: 'success',
                title: 'scrcpy 已停止。',
                confirmButtonText: '确定'
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: '停止 scrcpy 失败',
                text: data.error,
                confirmButtonText: '确定'
            });
        }
    }).always(function() {
        stopScrcpyButton.prop('disabled', false);
    });
}
