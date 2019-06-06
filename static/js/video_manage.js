function Manage() {

}


Manage.prototype.run = function () {
    var self = this;
    self.listenVideoInitEvent();
    self.CityTreeEvent();
    self.BdMapEvent();

};


Manage.prototype.listenVideoInitEvent = function () {
    layui.use(['layer', 'element', 'tree', 'form'], function () {
        var element = layui.element,
            tree = layui.tree,
            form = layui.form,
            layer = layui.layer;
        layer.msg('注：1.点击监控图标修改信息。2.已同步云端最新数据。');
    });
};


// 百度地图相关逻辑
Manage.prototype.BdMapEvent = function () {
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
                    var map = new BMap.Map("allmap");    // 创建Map实例
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
                            var myIcon = new BMap.Icon('/static/images/摄像头.png', new BMap.Size(58, 55)); // 创建监控点新图标(已启用)
                        } else {
                            var myIcon = new BMap.Icon('/static/images/摄像头2.png', new BMap.Size(58, 55)); // 创建监控点新图标(未启用)
                        }
                        marker[i] = new BMap.Marker(point[i], {icon: myIcon});
                        map.addOverlay(marker[i]); // 按照地图点坐标生成标记
                        addClick(marker[i], data[i], i); // 按照地图点坐标生成标记
                    }

                    function addClick(marker, data, i) {
                        marker.addEventListener('click', function (e) {
                            layer.open({
                                type: 0,
                                title: '监控点操作',
                                btn: ['修改'],
                                content: '可操作修改设备名称~',
                                yes: function (index) {
                                    // 二次弹窗
                                    layer.open({
                                        type: 1,
                                        title: false,
                                        btn: '点击修改',
                                        content: $('#video-manage'),
                                        yes: function () {
                                            var name = $("input[name='name']").val();
                                            $.ajax({
                                                type: 'post',
                                                url: '/maps/map_name/',
                                                data: {
                                                    'id': data['id'],
                                                    'name': name
                                                },
                                                success: function (result) {
                                                    if (result['code'] === 200) {
                                                        layer.alert('修改成功');
                                                        setTimeout('parent.location.reload();', 1000); // 手动关闭弹窗
                                                    } else {
                                                        var messageObject = result['message'];
                                                        if (typeof messageObject == 'string') {
                                                            layer.alert(messageObject);
                                                        } else {
                                                            for (var key in messageObject) {
                                                                var messages = messageObject[key];
                                                                var message = messages[0];
                                                                layer.alert(message);
                                                            }
                                                        }
                                                    }
                                                },
                                                error: function () {
                                                    layer.alert('修改失败,请重试...');
                                                }
                                            });
                                        }
                                    });
                                    layer.close(index); // 手动关闭弹窗
                                },
                            });
                        })
                    }
                } else {
                    alert('获取失败...');
                }
            }
        });
    });
};


Manage.prototype.CityTreeEvent = function () {
    layui.use(['tree', 'form', 'layer'], function () {
        var tree = layui.tree,
            form = layui.form,
            layer = layui.layer;

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
                        skin:'demo',
                        //　树节点 - 点击
                        click: function (node) {
                            //　点击树节点获取数值操作
                            var id = node['id'];
                            let dev_id = node['dev_id'];
                            if (dev_id) {
                                layer.open({
                                type: 1,
                                title: false,
                                btn: '点击修改',
                                content: $('#video-manage'),
                                yes: function () {
                                    var name = $("input[name='name']").val();
                                    $.ajax({
                                        type: 'post',
                                        url: '/maps/map_name/',
                                        data: {
                                            'id': id,
                                            'name': name
                                        },
                                        success: function (result) {
                                            if (result['code'] === 200) {
                                                layer.alert('修改成功');
                                                setTimeout('parent.location.reload();', 1000); // 手动关闭弹窗
                                            } else {
                                                var messageObject = result['message'];
                                                if (typeof messageObject == 'string') {
                                                    layer.alert(messageObject);
                                                } else {
                                                    for (var key in messageObject) {
                                                        var messages = messageObject[key];
                                                        var message = messages[0];
                                                        layer.alert(message);
                                                    }
                                                }
                                            }
                                        },
                                        error: function () {
                                            layer.alert('修改失败,请重试...');
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
    });
};


// 视频监控页 - 鼠标移动显示离线监控点信息
$(function (param) {
    var showBtn = $('#show-down');
    var showMap = $('.show-maps');
    // 鼠标放入
    showBtn.mouseenter(function (param) {
            showMap.css('display', 'block');
        }),
        // 鼠标放入
        showMap.mouseenter(function (param) {
            showMap.css('display', 'block');
        }),
        // 鼠标拿走
        showMap.mouseleave(function (param) {
            showMap.css('display', 'none');
        })
})


$(function () {
    var manage = new Manage();
    manage.run();
});
