function Video() {

}

Video.prototype.run = function () {
    var self = this;
    self.VideoCityTreeEvent();
    self.BdMapEvent();
    self.CityTreeEvent();
};


// 视频监控页面 城市树
Video.prototype.CityTreeEvent = function () {
    layui.use(['tree', 'layer'], function () {
        var tree = layui.tree,
            layer = layui.layer;
        $.ajax({
            type: 'get',
            url: '/public/city_tree/',
            data: {},
            success: function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    layui.tree({
                        elem: '#video-tree', //传入元素选择器
                        nodes: data,
                        skin: 'demo',
                        //　树节点 - 点击
                        click: function (node) {
                            //　点击树节点获取数值操作
                            var dev_id = node['dev_id'];
                            if (dev_id) {
                                layer.open({
                                    type: 1,
                                    title: false,
                                    area: ['460px', '240px'],
                                    scrollbar: false,
                                    content: $('#warn-tips'),
                                    success: function (layero, index) {
                                        let name = node['name'];
                                        let address = node['address'];
                                        let warn_count = node['warn_count'];
                                        var html = template('warn-content-tree', {
                                            'name': name,
                                            'address': address,
                                            'warn_count': warn_count,
                                            'id': node['id']
                                        });
                                        document.getElementById('warn-tips').innerHTML = html;

                                        // 获取播放直播流地址
                                        $.ajax({
                                            type: 'post',
                                            url: '/video/rec_play/',
                                            data: {
                                                'dev_id': dev_id
                                            },
                                            success: function (result) {
                                                if (result['code'] === 200) {
                                                    var rtmp_url = result['data']['rtmp_url']; // 获取播放地址1
                                                    var player = videojs('player');
                                                    player.ready(function () {
                                                        var myPlayer = this;
                                                        myPlayer.reset();
                                                        myPlayer.src({
                                                            type: "rtmp/flv",
                                                            src: rtmp_url
                                                        });
                                                        myPlayer.load(rtmp_url); // 这个需要从新加载地址...
                                                        myPlayer.play(); // 点击播放
                                                    });

                                                    // layer.close(index);
                                                } else {
                                                    layer.alert('服务器出错，请重试...');
                                                }
                                            },
                                            error: function () {
                                                layer.alert('视频流获取失败，请稍后重试...');
                                            }
                                        })
                                    },
                                    cancel: function (index, layero) {
                                        $.ajax({
                                            type: 'get',
                                            url: '/public/bdmap/',
                                            data: {},
                                            success: function (result) {
                                                if (result['code'] === 200) {
                                                    var dev_data = result['data'];
                                                    $.ajax({
                                                        type: 'post',
                                                        url: '/video/stop_play/',
                                                        data: {
                                                            'monitor_id': dev_data[i]['monitor_id'],
                                                        },
                                                        success: function (result) {
                                                            if (result['code'] === 200) {
                                                                window.location.reload();
                                                            } else {
                                                                layer.close(index);
                                                                layer.alert('视频流获取失败，请稍后重试...');
                                                            }
                                                        },
                                                        error: function () {
                                                            layer.close(index);
                                                            layer.alert('视频流获取失败，请稍后重试...');
                                                        }
                                                    });
                                                }
                                            }
                                        });
                                        window.location.reload();
                                    }
                                });
                                // 点击生成预警单逻辑
                                str_obj = '#maps-warn' + node['id'];
                                var mapWarn = $(str_obj);
                                mapWarn.click(function () {
                                    $.ajax({
                                        type: 'post',
                                        url: '/public/rec_data',
                                        data: {
                                            'dev_id': node['dev_id'],
                                            'warn_type': 2
                                        },
                                        success: function (result) {
                                            if (result['code'] === 200) {
                                                layer.alert('预警单创建成功,请稍后查看.');
                                            } else {
                                                layer.alert('获取数据失败，请稍后重试...');
                                            }
                                        },
                                        error: function () {
                                            layer.alert('获取数据失败，请先点击监控点...');
                                        }
                                    });
                                });
                            } else {
                                layer.msg('请双击展开节点.');
                            }
                        }
                    });
                }
            }
        });
    });
};


// 监控管理页面 城市树
Video.prototype.VideoCityTreeEvent = function () {
    layui.use(['tree', 'form', 'layer', 'laydate'], function () {
        var tree = layui.tree,
            form = layui.form,
            laydate = layui.laydate,
            layer = layui.layer;

        var devid = ''; // 定义全局变量
        $.ajax({
            type: 'get',
            url: '/public/city_tree/',
            data: {},
            success: function (result) {
                if (result['code'] === 200) {
                    var json_data = result['data'];
                    layui.tree({
                        elem: '#city-tree', //传入元素选择器
                        nodes: json_data,
                        spread: true,
                        skin: 'demo',

                        //　树节点 - 点击
                        click: function (node) {
                            //　点击树节点获取数值操作
                            var dev_id = node['dev_id'];
                            devid = dev_id; // 赋值给全局变量
                            if (dev_id) {
                                // 点击监控点创建视频流任务
                                layer.open({
                                    type: 1,
                                    title: '下拉选择投放位置',
                                    area: ['300px', '180px'],
                                    content: $('#video-select'),
                                    btn: '点击确认',
                                    yes: function (index) {
                                        var selectBtn = $('#select-num option:selected').val();
                                        id_value = 'player' + selectBtn; // + '_html5_api'
                                        // 获取播放直播流地址
                                        $.ajax({
                                            type: 'post',
                                            url: '/video/rec_play/',
                                            data: {
                                                'dev_id': dev_id
                                            },
                                            success: function (result) {
                                                if (result['code'] === 200) {
                                                    var rtmp_url = result['data']['rtmp_url']; // 获取播放地址
                                                    var player = videojs(id_value);
                                                    player.src({
                                                        type: "rtmp/flv",
                                                        src: rtmp_url
                                                    });
                                                    // player.load(rtmp_url);
                                                    player.play();
                                                    layer.close(index);
                                                } else {
                                                }
                                            },
                                            error: function () {
                                                layer.close(index);
                                                layer.alert('视频流获取失败，请稍后重试...');
                                            }
                                        });
                                    }
                                });
                            } else {
                                layer.msg('请点击具体监控点.');
                            }
                        }
                    });
                }
            }
        });

        //视频录像操作逻辑 加载日期时间控件
        laydate.render({
            elem: '#video-date',
            done: function (value, data) {
                $.ajax({
                    type: 'get',
                    url: '/video/search_video/',
                    data: {
                        'date_value': value,
                        'dev_id': devid
                    },
                    success: function (result) {
                        if (result['code'] === 200) {
                            var data = result['data'];
                            var json_data = JSON.parse(data);
                            var html = template('video-rec', {
                                'data': json_data
                            });
                            document.getElementById('video-play').innerHTML = html;
                            var indexBtn = $('.index-data');
                            var monitorid = '';
                            indexBtn.click(function () {
                                var btn = $(this);
                                var index_data = btn.attr('data-id');
                                layer.open({
                                    type: 1,
                                    title: '视频录像播放',
                                    area: ['680px', '500px'],
                                    content: $('#start-video'),
                                    btn: '点击关闭',
                                    success: function (layero, index) {
                                        // 请求录像播放地址

                                        $.ajax({
                                            type: 'post',
                                            url: '/video/play_video/',
                                            data: {
                                                'dev_id': devid,
                                                'start_time': json_data[index_data]['start_time'],
                                                'stop_time': json_data[index_data]['stop_time'],
                                            },
                                            success: function (result) {
                                                if (result['code'] === 200) {
                                                    var rtmp_url = result['data']['rtmp_url'];
                                                    var monitor_id = result['data']['monitor_id'];
                                                    monitorid = monitor_id;
                                                    var player = videojs('player');
                                                    player.ready(function () {
                                                        var myPlayer = this;
                                                        myPlayer.reset();
                                                        myPlayer.src({
                                                            type: "rtmp/flv",
                                                            src: rtmp_url
                                                        });
                                                        myPlayer.load(rtmp_url); // 这个需要从新加载地址...
                                                        myPlayer.play(); // 点击播放
                                                    });
                                                } else {
                                                    layer.alert('111');
                                                }
                                            },
                                        });
                                    },
                                    yes: function (index) {
                                        layer.close(index);
                                    },
                                    cancel: function (layero, index) {
                                        $.ajax({
                                            type: 'post',
                                            url: '/video/stop_video/',
                                            data: {
                                                'monitor_id': monitorid
                                            },
                                            success: function (result) {
                                                if (result['code'] === 200) {
                                                    return
                                                }
                                            }
                                        });
                                    }
                                });
                            });

                        } else {
                            layer.alert('获取失败，请重试...');
                        }
                    }
                });
            }
        });

        // 点击生成预警单逻辑
        var addWarn = $('#add-warn');
        addWarn.click(function () {
            $.ajax({
                type: 'post',
                url: '/public/rec_data',
                data: {
                    'dev_id': devid,
                    'warn_type': 2
                },
                success: function (result) {
                    if (result['code'] === 200) {
                        layer.alert('预警单创建成功,请稍后查看.');
                    } else {
                        layer.alert('获取数据失败，请稍后重试...');
                    }
                },
                error: function () {
                    layer.alert('获取数据失败，请先点击监控点...');
                }
            });
        });

        // video页面点击查看
        var videoDemoBtn = $('#video-demo');
        videoDemoBtn.click(function () {
            layer.confirm('点击确认，跳转处理页.', {
                btn: '确认',
                yes: function (index, layero) {
                    layer.close(index);
                    setTimeout("window.location.href='/warn_list/'"); //　跳转
                }
            });
        });
    });
};

// 百度地图相关逻辑
Video.prototype.BdMapEvent = function () {
    layui.use('layer', function () {
        var layer = layui.layer;

        $.ajax({
            type: 'get',
            url: '/public/bdmap/',
            data: {},
            success: function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    // 百度地图API功能
                    var map = new BMap.Map("allmap"); // 创建Map实例
                    //添加地图类型控件
                    map.centerAndZoom(new BMap.Point(120.639921, 31.319263), 20); //  初始化地图,设置中心点坐标和地图级别
                    map.enableScrollWheelZoom(true); // 设置鼠标滚轮缩放

                    var navigationControl = new BMap.NavigationControl({
                        // 靠左上角位置
                        anchor: BMAP_ANCHOR_TOP_LEFT,
                        // LARGE类型
                        type: BMAP_NAVIGATION_CONTROL_LARGE,
                        // 启用显示定位
                        enableGeolocation: true
                    });
                    map.addControl(navigationControl); // 设置左上角控件//开启鼠标滚轮缩放

                    var point = []; // 存放标注点经纬度数组
                    var marker = []; // 存放标注点对象的数组

                    // 遍历经纬度数组
                    for (var i = 0; i < data.length; i++) {
                        point[i] = new BMap.Point(data[i]['longitude'], data[i]['latitude']); //　循环生成新的地图点
                        if (data[i]['status'] == 1) {
                            var myIcon = new BMap.Icon('/static/images/摄像头.png', new BMap.Size(50, 50)); // 创建监控点新图标(已启用)
                        } else {
                            var myIcon = new BMap.Icon('/static/images/摄像头2.png', new BMap.Size(50, 50)); // 创建监控点新图标(未启用)
                        }
                        marker[i] = new BMap.Marker(point[i], {
                            icon: myIcon
                        });
                        map.addOverlay(marker[i]); // 按照地图点坐标生成标记
                        addClick(marker[i], data[i], i); // 按照地图点击图标
                    }

                    function addClick(marker, data, i) {
                        marker.addEventListener('click', function (e) {
                            layer.open({
                                type: 1,
                                title: false,
                                area: ['460px', '240px'],
                                scrollbar: false,
                                content: $('#warn-tips'),
                                success: function (layero, index) {
                                    var html = template('warn-content', {
                                        'data': data,
                                        'index': i
                                    });
                                    document.getElementById('warn-tips').innerHTML = html;

                                    // 获取播放直播流地址
                                    $.ajax({
                                        type: 'post',
                                        url: '/video/rec_play/',
                                        data: {
                                            'dev_id': data['dev_id']
                                        },
                                        success: function (result) {
                                            if (result['code'] === 200) {
                                                var rtmp_url = result['data']['rtmp_url']; // 获取播放地址
                                                var player = videojs('player');
                                                player.ready(function () {
                                                    var myPlayer = this;
                                                    myPlayer.reset();
                                                    myPlayer.src({
                                                        type: "rtmp/flv",
                                                        src: rtmp_url
                                                    });
                                                    myPlayer.load(rtmp_url); // 这个需要从新加载地址...
                                                    myPlayer.play(); // 点击播放
                                                });
                                            } else {
                                                layer.alert('服务器出错，请重试...');
                                            }
                                        },
                                        error: function () {
                                            layer.alert('视频流获取失败，请稍后重试...');
                                        }
                                    })
                                },
                                cancel: function (index, layero) {
                                    $.ajax({
                                        type: 'get',
                                        url: '/public/bdmap/',
                                        data: {},
                                        success: function (result) {
                                            if (result['code'] === 200) {
                                                var dev_data = result['data'];
                                                $.ajax({
                                                    type: 'post',
                                                    url: '/video/stop_play/',
                                                    data: {
                                                        'monitor_id': dev_data[i]['monitor_id'],
                                                    },
                                                    success: function (result) {
                                                        if (result['code'] === 200) {
                                                            parent.location.reload();
                                                        } else {
                                                            layer.close(index);
                                                            // layer.alert('视频流获取失败，请稍后重试...');
                                                        }
                                                    },
                                                    error: function () {
                                                        layer.close(index);
                                                        // layer.alert('视频流获取失败，请稍后重试...');
                                                    }
                                                });
                                            }
                                        }
                                    })
                                }
                            });
                            // 点击生成预警单逻辑
                            str_obj = '#maps-warn' + i;
                            var mapWarn = $(str_obj);
                            mapWarn.click(function () {
                                $.ajax({
                                    type: 'post',
                                    url: '/public/rec_data',
                                    data: {
                                        'dev_id': data['dev_id'],
                                        'warn_type': 2
                                    },
                                    success: function (result) {
                                        if (result['code'] === 200) {
                                            layer.alert('预警单创建成功,请稍后查看.');
                                        } else {
                                            layer.alert('获取数据失败，请稍后重试...');
                                        }
                                    },
                                    error: function () {
                                        layer.alert('获取数据失败，请先点击监控点...');
                                    }
                                });
                            });
                        });
                    }
                } else {
                    alert('获取失败...');
                }
            }
        });
    });
};

// 视频监控页 - 鼠标移动显示离线监控点信息
$(function (param) {
    var showBtn = $('#show-down');
    var showMap = $('.show-maps');
    // 鼠标放入
    showBtn.mouseenter(function (param) {
        showMap.css('display', 'block');
    });
    // 鼠标放入
    showMap.mouseenter(function (param) {
        showMap.css('display', 'block');
    });
    // 鼠标拿走
    showMap.mouseleave(function (param) {
        showMap.css('display', 'none');
    });
});


$(function () {
    var video = new Video();
    video.run();
});