function View() {

}

View.prototype.run = function () {
    var self = this;
    self.VideoViewTreeEvent();
};


// 查看录像
View.prototype.VideoViewTreeEvent = function () {
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
                                            console.log(rtmp_url);
                                            var player = videojs('player');
                                            player.src({
                                                type: "rtmp/flv",
                                                src: rtmp_url
                                            });
                                            player.play();
                                        }
                                    },
                                    error: function () {
                                        layer.alert('视频流获取失败，请稍后重试...');
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
                            indexBtn.click(function () {
                                var btn = $(this);
                                var index_data = btn.attr('data-id');
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
                                            var rtmp_url = result['data']['rtmp_url']; // 获取播放地址
                                            console.log(rtmp_url);
                                            var player = videojs('player');
                                            player.src({
                                                type: "rtmp/flv",
                                                src: rtmp_url
                                            });
                                            // player.load(rtmp_url);
                                            player.play();
                                        } else {
                                            layer.alert('获取失败,请重试.');
                                        }
                                    }
                                });
                                // var monitor_id = result['data']['monitor_id'];
                                // monitorid = monitor_id;
                                // $.ajax({
                                //     type: 'post',
                                //     url: '/video/stop_video/',
                                //     data: {
                                //         'monitor_id': monitorid
                                //     },
                                //     success: function (result) {
                                //         if (result['code'] === 200) {
                                //             return
                                //         }
                                //     }
                                // });
                            });

                        } else {
                            layer.alert('请先选择监控点.');
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


// 格式化播放录像的时间片段
$(function () {
    if (window.template) {
        template.defaults.imports.timeSince = function (dateValue) {
            // return new Date(parseInt(dateValue) * 1000).toLocaleString().replace(/:\d{1,2}$/, ' ');
            var times = new Date(parseInt(dateValue) * 1000);
            var hour = times.getHours();
            var minute = times.getMinutes();
            var second = times.getSeconds();
            return hour + ":" + minute + ":" + second;
        }
    }
});


$(function () {
    var view = new View();
    view.run();
});