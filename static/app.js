// 刷新设备列表
function refreshDevices() {
    const refreshDevicesButton = $('#refresh-devices-button');
    refreshDevicesButton.prop('disabled', true);

    $.post('/refresh', function(data) {
        const deviceSelect = $('#device-select');
        deviceSelect.empty();

        if (data.length === 0) {
<<<<<<< HEAD
            deviceSelect.html('<option value="">未检测到设备</option>');
=======
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
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
<<<<<<< HEAD
    const deviceId = $('#device-select').val();

    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备',
            text: '请选择设备。',
            confirmButtonText: '确定'
        });
    getInstalledAppsButton.prop('disabled', false);
    return;
}
=======

    const deviceId = $('#device-select').val();

>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
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

<<<<<<< HEAD
// 搜索应用
function searchApps() {
    const query = $('#app-search-input').val().toLowerCase();
    const deviceId = $('#device-select').val();

    $.post('/search_apps', { device_id: deviceId, query: query }, function(data) {
        updateAppSelect(data);
    }).fail(function(xhr, status, error) {
        console.error('搜索应用失败:', error);
        Swal.fire({
            icon: 'error',
            title: '搜索应用失败',
            text: '请稍后重试',
            confirmButtonText: '确定'
        });
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
    searchApps();
});

=======
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
// 卸载应用程序
function uninstallApp() {
    const uninstallAppButton = $('#uninstall-app-button');
    uninstallAppButton.prop('disabled', true);

    const deviceId = $('#device-select').val();
    const packageName = $('#app-select').val();

    if (!deviceId || !packageName) {
        Swal.fire({
            icon: 'warning',
<<<<<<< HEAD
            title: '必要信息缺失',
            text: '请选择所要卸载的设备ID和应用程序包名。',
=======
            title: '请选择要卸载的设备和应用程序。',
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
            confirmButtonText: '确定'
        });
        uninstallAppButton.prop('disabled', false);
        return;
    }

    // 二次确认
    Swal.fire({
<<<<<<< HEAD
        title: `卸载应用`,
=======
        title: '确认',
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
        text: `您确定要卸载包名为 ${packageName} 的应用程序吗？`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: '确定',
        cancelButtonText: '取消'
    }).then((result) => {
        if (result.isConfirmed) {
<<<<<<< HEAD
            showLoading();
=======
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
            $.post('/uninstall_app', { device_id: deviceId, package_name: packageName })
                .done(function(response) {
                    if (response.success) {
                        Swal.fire({
                            icon: 'success',
<<<<<<< HEAD
                            title: '卸载成功',
                            text: '目标应用程序已卸载成功。',
=======
                            title: '应用程序卸载成功。',
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
                            confirmButtonText: '确定'
                        });
                        getInstalledApps();
                    } else {
                        Swal.fire({
                            icon: 'error',
<<<<<<< HEAD
                            title: '卸载失败',
                            text: '目标应用程序卸载失败。',
=======
                            title: '无法卸载应用',
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
                            text: response.error,
                            confirmButtonText: '确定'
                        });
                    }
                })
                .fail(function() {
                    Swal.fire({
                        icon: 'error',
<<<<<<< HEAD
                        title: '卸载异常',
                        text: '目标应用程序无法卸载。',
=======
                        title: '错误',
                        text: '无法卸载应用程序。',
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
                        confirmButtonText: '确定'
                    });
                })
                .always(function() {
                    uninstallAppButton.prop('disabled', false);
<<<<<<< HEAD
                    hideLoading();
=======
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
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
<<<<<<< HEAD
    const deviceId = $('#device-select').val();
    const apkFiles = $('#apk-file')[0].files;

    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备',
            text: '请选择设备。',
=======

    const deviceId = $('#device-select').val();
    const apkFile = $('#apk-file')[0].files[0];

    if (!apkFile) {
        Swal.fire({
            icon: 'warning',
            title: '请先选择一个 APK 文件。',
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
            confirmButtonText: '确定'
        });
        installApkButton.prop('disabled', false);
        return;
    }
<<<<<<< HEAD
    showLoading();

    if (apkFiles.length === 0) {
        Swal.fire({
            icon: 'warning',
            title: 'APK文件缺失',
            text: '请先选择至少一个APK文件。',
            confirmButtonText: '确定'
        });
        installApkButton.prop('disabled', false);
        hideLoading();
        return;
    }

    let invalidFile = false;
    for (let i = 0; i < apkFiles.length; i++) {
        if (!apkFiles[i].name.endsWith('.apk')) {
            invalidFile = true;
            break;
        }
    }

    if (invalidFile) {
        Swal.fire({
            icon: 'error',
            title: '安装失败',
            text: '请选择apk格式的文件进行安装',
            confirmButtonText: '确定'
        });
        installApkButton.prop('disabled', false);
        hideLoading();
        return;
    }

    showLoading();

    const formData = new FormData();
    formData.append('device_id', deviceId);
    for (let i = 0; i < apkFiles.length; i++) {
        formData.append('apk_files', apkFiles[i]);
    }
=======

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
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5

    $.ajax({
        url: '/install_apk',
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
<<<<<<< HEAD
            displayInstallResult(data);
=======
            Swal.fire({
                icon: data.success ? 'success' : 'error',
                title: data.success ? 'APK 安装成功' : 'APK 安装失败',
                text: data.success ? '' : data.error,
                confirmButtonText: '确定'
            });
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
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
<<<<<<< HEAD
        hideLoading();
    });
}


// 显示安装结果
function displayInstallResult(results) {
    const failedList = $('#failed-list');
    const successList = $('#success-list');
    failedList.empty();
    successList.empty();

    results.forEach(result => {
        if (result.success) {
            successList.append(`<li>${result.filename}</li>`);
        } else {
            failedList.append(`
                <li>
                    ${result.filename}
                    <div class="error-message">${result.error}</div>
                </li>
            `);
        }
    });

    if (failedList.children().length === 0) {
        $('#failed-installs').hide();
    } else {
        $('#failed-installs').show();
    }

    if (successList.children().length === 0) {
        $('#successful-installs').hide();
    } else {
        $('#successful-installs').show();
    }

    $('#install-result').show();
}

// 添加关闭结果模态框的事件处理
$('#close-result').on('click', function() {
    $('#install-result').hide();
});


// 截图
function takeScreenshot() {
    const takeScreenshotButton = $('#take-screenshot-button');
    takeScreenshotButton.prop('disabled', true);
    const deviceId = $('#device-select').val();

    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备',
            text: '请选择设备。',
            confirmButtonText: '确定'
        });
        takeScreenshotButton.prop('disabled', false);
        return;
    }
    showLoading();

=======
    });
}

// 截图函数
function takeScreenshot() {
    const takeScreenshotButton = $('#take-screenshot-button');
    takeScreenshotButton.prop('disabled', true);

    const deviceId = $('#device-select').val();
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
    $.post('/screenshot', { device_id: deviceId }, function(data) {
        if (data.success) {
            Swal.fire({
                icon: 'success',
                title: '截图成功！',
<<<<<<< HEAD
                text: `文件名：${data.filename}`,
                confirmButtonText: '确定'
            }).then(() => {
                // 触发下载
                window.location.href = '/download/' + encodeURIComponent(data.filename);
=======
                text: `路径：${data.path}`,
                confirmButtonText: '确定'
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
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
<<<<<<< HEAD
        hideLoading();
    });
}

// 录屏
function recordScreen() {
    const recordScreenButton = $('#record-screen-button');
    recordScreenButton.prop('disabled', true);
    const deviceId = $('#device-select').val();

    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备',
            text: '请选择设备。',
            confirmButtonText: '确定'
        });
        recordScreenButton.prop('disabled', false);
        return;
    }
    showLoading();

    const duration = prompt('请输入录屏时长（大于1秒）：');
    const parsedDuration = parseInt(duration, 10);

    if (isNaN(parsedDuration) || parsedDuration <= 1) {
        Swal.fire({
            icon: 'warning',
            title: '无效的录屏时长。',
            text: '请输入大于1的有效正整数。',
            confirmButtonText: '确定'
        });
        recordScreenButton.prop('disabled', false);
        hideLoading();
        return;
    }

    $.post('/record_screen', { device_id: deviceId, duration: parsedDuration }, function(data) {
=======
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
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
        if (data.success) {
            Swal.fire({
                icon: 'success',
                title: '录屏成功！',
<<<<<<< HEAD
                text: `文件名：${data.filename}`,
                confirmButtonText: '确定',
                showLoaderOnConfirm: true,
                preConfirm: () => {
                    return new Promise((resolve) => {
                        window.location.href = '/download/' + encodeURIComponent(data.filename);
                        setTimeout(resolve, 2000);
                    });
                }
=======
                text: `路径：${data.path}`,
                confirmButtonText: '确定'
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
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
<<<<<<< HEAD
        hideLoading();
=======
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
    });
}

// 重启设备函数
function restartDevice() {
    const restartDeviceButton = $('#restart-device-button');
    restartDeviceButton.prop('disabled', true);

    const deviceId = $('#device-select').val();

<<<<<<< HEAD
    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备',
            text: '请选择设备。',
            confirmButtonText: '确定'
        });
        restartDeviceButton.prop('disabled', false);
        return;
    }
    showLoading();

=======
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
    $.post('/restart_device', { device_id: deviceId }, function(data) {
        if (data.success) {
            Swal.fire({
                icon: 'success',
<<<<<<< HEAD
                title: '设备重启成功。',
=======
                title: '设备已重启。',
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
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
<<<<<<< HEAD
    hideLoading();
=======
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
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
<<<<<<< HEAD
            title: '请选择设备',
            text: '请选择设备。',
=======
            title: '请选择设备。',
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
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
<<<<<<< HEAD
    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备',
            text: '请选择设备。',
            confirmButtonText: '确定'
        });
        enableWirelessDebuggingButton.prop('disabled', false);
        return;
    }
=======
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5

    $.post('/enable_wireless_debugging', { device_id: deviceId }, function(data) {
        if (data.success) {
            Swal.fire({
                icon: 'success',
<<<<<<< HEAD
                title: '无线调试启用成功。',
=======
                title: '无线调试已启用。',
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
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
<<<<<<< HEAD
    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备',
            text: '请选择设备。',
            confirmButtonText: '确定'
        });
        disableWirelessDebuggingButton.prop('disabled', false);
        return;
    }
=======
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5

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
<<<<<<< HEAD
            title: '请选择设备',
            text: '请选择设备。',
=======
            title: '请选择设备。',
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
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
<<<<<<< HEAD
                title: '启用投屏互动模式',
=======
                title: '启动 scrcpy 失败',
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
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
<<<<<<< HEAD
                title: '停用投屏互动模式失败',
=======
                title: '停止 scrcpy 失败',
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
                text: data.error,
                confirmButtonText: '确定'
            });
        }
    }).always(function() {
        stopScrcpyButton.prop('disabled', false);
    });
}
<<<<<<< HEAD


// 当整个文档准备好时，隐藏加载覆盖层，打印信息到控制台，并调用 fetchCertificates 函数获取证书列表
$(document).ready(function() {
    $('#loading-overlay').hide();
    console.log('jQuery document ready');
    fetchCertificates();
});

// 通过 fetch API 请求 '/get_certificates' 获取证书列表，然后将证书列表传递给 populateCertificateList 函数
function fetchCertificates() {
    fetch('/get_certificates')
        .then(response => response.json())
        .then(certificates => populateCertificateList(certificates))
        .catch(error => {
            console.error('Error fetching certificates:', error);
        });
}

// 将获取到的证书列表填充到下拉菜单中
function populateCertificateList(certificates) {
    const certificateSelect = document.getElementById('certificate-select');
    certificateSelect.innerHTML = '';
    certificates.forEach(certificate => {
        const option = document.createElement('option');
        option.value = certificate.display_name;
        option.textContent = certificate.display_name;
        certificateSelect.appendChild(option);
    });
}

function showLoading() {
    // 显示加载覆盖层。
    document.getElementById('loading-overlay').style.display = 'flex';
}

function hideLoading() {
    // 隐藏加载覆盖层。
    document.getElementById('loading-overlay').style.display = 'none';
}

// 用上传.aab文件并。
function uploadAab() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (!file) {
        Swal.fire({
            icon: 'warning',
            title: 'AAB文件缺失',
            text: '请上传所要转化的AAB格式文件。',
            confirmButtonText: '确定'
        });
        return;
    }

    console.log('File selected:', file.name);

    const uploadButton = $('#upload-button');
    uploadButton.prop('disabled', true);

    if (!file.name.endsWith('.aab')) {
        Swal.fire({
            icon: 'error',
            title: '转换失败',
            text: '请选择AAB格式的文件进行转换',
            confirmButtonText: '确定'
        });
        uploadButton.prop('disabled', false);
        return;
    }

    showLoading();
    $('#certificate-select').prop('disabled', true);

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload_aab', {
        method: 'POST',
        body: formData,
    })
    .then(handleFetchResponse)
    .catch(handleFetchError);
}

// 处理 fetch 请求的响应。
function handleFetchResponse(response) {
    console.log('Response received:', response);
    if (response.ok) {
        return response.json().then(data => {
            console.log('Response data:', data);
            if (data.success) {
                convertAab(data.filename);
            } else {
                console.log('Error from server:', data.error);
                $('#upload-button').prop('disabled', false);
                hideLoading();
                $('#certificate-select').prop('disabled', false);
            }
        });
    } else {
        console.log('Error response:', response.status);
        throw new Error('无法连接服务器');
    }
}

// 处理 fetch 请求的错误
function handleFetchError(error) {
    console.error('Error:', error);
    Swal.fire({
        icon: 'error',
        title: '上传失败',
        text: '无法连接服务器',
        confirmButtonText: '确定'
    });
    $('#upload-button').prop('disabled', false);
    hideLoading();
    $('#certificate-select').prop('disabled', false);
}

// 调用后台服务将.aab 文件转换，并更新界面状态
function convertAab(filename) {
    const certificateSelect = document.getElementById('certificate-select');
    const displayName = certificateSelect.value;

    $.post('/convert_aab', { filename: filename, displayName: displayName })
        .done(function (response) {
            if (response.success) {
                getConvertedFiles();
                Swal.fire({
                    icon: 'success',
                    title: '转化成功',
                    text: 'aab文件转换完成。',
                    confirmButtonText: '确定'
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: '转化失败',
                    text: '无法转化aab文件。',
                    confirmButtonText: '确定'
                });
            }
            $('#upload-button').prop('disabled', false);
            hideLoading();
            $('#certificate-select').prop('disabled', false);
        })
        .fail(function () {
            Swal.fire({
                icon: 'error',
                title: '转化失败',
                text: '无法连接服务器。',
                confirmButtonText: '确定'
            });
            $('#upload-button').prop('disabled', false);
            hideLoading();
            $('#certificate-select').prop('disabled', false);
        });
}

// 获取并显示转换后的文件列表
async function getConvertedFiles() {
    try {
        const response = await fetch('/get_converted_files');
        if (!response.ok) {
            throw new Error('无法连接服务器');
        }
        const fileList = await response.json();
        const fileListElement = document.getElementById('file-list');
        fileListElement.innerHTML = '';

        fileList.forEach(file => {
            const link = document.createElement('a');
            link.setAttribute('href', `/download/${file}`);
            link.setAttribute('download', '');
            link.innerText = file;

            const downloadButton = document.createElement('button');
            downloadButton.innerText = '下载文件';
            downloadButton.classList.add('btn', 'btn-success', 'w-100', 'mb-2');

            downloadButton.onclick = function () {
                downloadConvertedFile(file);
            };

            const listItem = document.createElement('li');
            listItem.style.textAlign = 'center';
            listItem.appendChild(link);
            listItem.appendChild(downloadButton);
            fileListElement.appendChild(listItem);
        });
    } catch (error) {
        Swal.fire({
            icon: 'error',
            title: '获取文件列表失败',
            text: '无法连接服务器',
            confirmButtonText: '确定'
        });
    }
}


//用于下载转换后的文件
function downloadConvertedFile(filename) {
    console.log('Downloading file:', filename);
    showLoading();

    var xhr = new XMLHttpRequest();
    var url = '/download/' + encodeURIComponent(filename);
    xhr.open('GET', url, true);
    xhr.responseType = 'blob';

    xhr.onload = function () {
        if (xhr.status === 200) {
            var blob = new Blob([xhr.response], { type: 'application/octet-stream' });
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            Swal.fire({
                icon: 'error',
                title: '下载失败',
                text: '无法下载文件',
                confirmButtonText: '确定'
            });
        }
        hideLoading();
    };

    xhr.onerror = function () {
        Swal.fire({
            icon: 'error',
            title: '下载失败',
            text: '无法连接服务器',
            confirmButtonText: '确定'
        });
        hideLoading();
    };

    xhr.send();
}

document.getElementById('generate-signature-button').addEventListener('click', function() {
    // 生成新签名证书的确认提示。
    Swal.fire({
        icon: 'question',
        title: '随机签名证书生成',
        text: `您确定要生成新的随机签名证书吗？`,
        showCancelButton: true,
        confirmButtonText: '确定',
        cancelButtonText: '取消'
    }).then((result) => {
        if (result.isConfirmed) {
            generateSignature();
        }
    });
});

// 用于生成新的随机签名证书并更新证书列表
function generateSignature() {
    const certificateSelect = document.getElementById('certificate-select');
    const displayName = certificateSelect.value;

    if (!displayName) {
        Swal.fire({
            icon: 'warning',
            title: '请选择证书',
            confirmButtonText: '确定'
        });
        return;
    }

    showLoading();

    $.post('/generate_signature', { displayName: displayName })
        .done(function (response) {
            if (response.success) {
                Swal.fire({
                    icon: 'success',
                    title: '签名生成成功',
                    text: `随机签名证书已生成成功，新生成证书的名称是：${response.certificateName}`,
                    confirmButtonText: '确定'
                }).then(() => {
                    fetchCertificates();
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: '签名生成失败',
                    text: response.error || '无法生成签名。',
                    confirmButtonText: '确定'
                });
            }
            hideLoading();
        })
        .fail(function () {
            Swal.fire({
                icon: 'error',
                title: '签名生成失败',
                text: '无法连接服务器。',
                confirmButtonText: '确定'
            });
            hideLoading();
        });
}

// 设备点击：电源、HOME、菜单、返回
function simulateKeyPress(key) {
    const deviceId = $('#device-select').val();
    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备',
            text: '请选择设备。',
            confirmButtonText: '确定'
        });
    return;
    }

    showLoading(); // 显示加载动画

    $.post('/simulate_key_press', { device_id: deviceId, key: key }, function(data) {
        Swal.fire({
            icon: 'success',
            title: '已选择目标按键',
            confirmButtonText: '确定'
        });
    }).fail(function() {
        Swal.fire({
            icon: 'error',
            title: '目标按键选择失败',
            confirmButtonText: '确定'
        });
    }).always(function() {
        hideLoading(); // 隐藏加载动画
    });
}

// 打开网址
function openUrl() {
    const deviceId = $('#device-select').val();
    const url = $('#url-input').val().trim();

    // 设备选择校验
    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备',
            text: '请选择设备。',
            confirmButtonText: '确定'
        });
        return;
    }

    // URL输入内容检测
    if (!url) {
        Swal.fire({
            icon: 'warning',
            title: '请输入网址',
            text: '网址不能为空。',
            confirmButtonText: '确定'
        });
        return;
    }

    // URL格式校验
    const urlPattern = /^(https?:\/\/)?(([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,})|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))(:(\d{1,9}))?(\/[\w\-./?%&=]*)?$/i;
    if (!urlPattern.test(url)) {
        $('#url-input').css('border-color', 'red');
        Swal.fire({
            icon: 'warning',
            title: '网址格式无效',
            text: '请输入有效的URL，例如：http://example.com。',
            confirmButtonText: '确定'
        });
        return;
    }


    showLoading(); // 显示加载动画

    $.post('/open_url', { device_id: deviceId, url: url }, function(data) {
        Swal.fire({
            icon: 'success',
            title: '网页已打开',
            text: '请在目标测试机上进行查看',
            confirmButtonText: '确定'
        });
        $('#url-input').val('');
    }).fail(function() {
        Swal.fire({
            icon: 'error',
            title: '打开网页失败',
            confirmButtonText: '确定'
        });
    }).always(function() {
        hideLoading(); // 隐藏加载动画
    });
}


// 检测IP地址
function checkDeviceIp() {
    const deviceId = $('#device-select').val();
    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备',
            text: '请选择设备。',
            confirmButtonText: '确定'
        });
        return;
    }

    showLoading(); // 显示加载动画

    $.post('/check_device_ip', { device_id: deviceId }, function(data) {
        Swal.fire({
            icon: 'success',
            title: '设备IP查看',
            text: '请在目标测试机上查看设备IP信息',
            confirmButtonText: '确定'
        });
    }).fail(function() {
        Swal.fire({
            icon: 'error',
            title: '查看设备IP失败',
            confirmButtonText: '确定'
        });
    }).always(function() {
        hideLoading(); // 隐藏加载动画
    });
}

// 清除应用缓存
function clearAppCache() {
    const deviceId = $('#device-select').val();
    const packageName = $('#app-select').val();

    // 设备选择校验
    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备',
            text: '请选择设备。',
            confirmButtonText: '确定'
        });
        return;
    }

    // 包名选择校验
    if (!packageName) {
        Swal.fire({
            icon: 'warning',
            title: '请选择应用包名',
            text: '请选择要清除缓存的应用包名。',
            confirmButtonText: '确定'
        });
        return;
    }

    showLoading(); // 显示加载动画

    $.post('/clear_app_cache', { device_id: deviceId, package_name: packageName }, function(data) {
        Swal.fire({
            icon: 'success',
            title: '已清除应用缓存',
            confirmButtonText: '确定'
        });
    }).fail(function() {
        Swal.fire({
            icon: 'error',
            title: '清除应用缓存失败',
            confirmButtonText: '确定'
        });
    }).always(function() {
        hideLoading(); // 隐藏加载动画
    });
}

// 停止应用运行
function stopApp() {
    const deviceId = $('#device-select').val();
    const packageName = $('#app-select').val();

    // 设备选择校验
    if (!deviceId) {
        Swal.fire({
            icon: 'warning',
            title: '请选择设备',
            text: '请选择设备。',
            confirmButtonText: '确定'
        });
        return;
    }

    // 包名选择校验
    if (!packageName) {
        Swal.fire({
            icon: 'warning',
            title: '请选择应用包名',
            text: '请选择要停止运行的应用包名。',
            confirmButtonText: '确定'
        });
        return;
    }

    showLoading(); // 显示加载动画

    $.post('/stop_app', { device_id: deviceId, package_name: packageName }, function(data) {
        Swal.fire({
            icon: 'success',
            title: '已停止应用运行',
            confirmButtonText: '确定'
        });
    }).fail(function() {
        Swal.fire({
            icon: 'error',
            title: '停止应用运行失败',
            confirmButtonText: '确定'
        });
    }).always(function() {
        hideLoading(); // 隐藏加载动画
    });
}

=======
>>>>>>> 9724e3b4f2c0436c579f209b5149c0bc2649c6d5
