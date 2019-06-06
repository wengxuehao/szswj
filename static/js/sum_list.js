function SumList() {

}

SumList.prototype.run = function () {
    var self = this;
    self.listenSumEvent();
};


SumList.prototype.listenSumEvent = function () {
    //注意：导航 依赖 element 模块，否则无法进行功能性操作
    layui.use(['table', 'form', 'element', 'layer'], function () {
        var table = layui.table,
            form = layui.form,
            layer = layui.layer,
            element = layui.element;

        // ******************************************

        //选项卡切换刷新
        var layid = location.hash.replace(/^#warn-tab=/, '');
        element.tabChange('warn-tab', layid);

        // 监听tab切换，改变地址hash值
        element.on('tab(warn-tab)', function (data) {
            location.hash = 'warn-tab=' + this.getAttribute('lay-id');
        });

        // ******************************************

        // 选项卡 - 已发送
        table.render({
            elem: '#table-sum1',
            height: 'full', // 表格高度始终填满
            even: true, //　列表隔行颜色
            size: 'lg',
            method: 'get', // 请求方法
            url: '/warn_list/newsum_list/', // 数据接口
            where: {
                'is_make': 2
            },
            page: true, // 开启分页　可传入laypage参数
            toolbar: 'true',
            limit: 12,
            text: '暂无数据...',
            cols: [
                [ // 表头　需要显示的数据列
                    // {
                    //     type: 'checkbox',
                    //     fixed: 'left'
                    // },
                    {
                        field: 'event_id',
                        title: '预警编号',
                        sort: true,
                    },
                    {
                        field: 'type_name',
                        title: '任务类型',
                    },
                    {
                        field: 'warn_type',
                        title: '预警类型',
                    },
                    {
                        field: 'map_name',
                        title: '所属监控点',
                    },
                    {
                        field: 'warn_url',
                        title: '事件图片',
                        toolbar: '#sum-image'
                    },
                    {
                        field: 'images',
                        title: '证据图片',
                        templet: '#warn-image'
                    },
                    {
                        field: 'video_url',
                        title: '证据视频',
                        templet: '#warn-video'
                    },
                    {
                        field: 'result',
                        title: '当前状态'
                    },
                    // {
                    //     field: 'manage_user',
                    //     title: '城管处理员'
                    // },
                    {
                        field: 'user',
                        title: '平台处理员'
                    },
                    {
                        field: 'add_time',
                        title: '发生时间',
                        sort: true,
                    }
                ]
            ]
        });

        // 监听工具条 is-make=2
        table.on('tool(warnlist1)', function (obj) {
            var data = obj.data; // 获取当前行数据
            var layEvent = obj.event; // lay-event的值
            if (layEvent === 'view-image') {
                // 弹窗查看图片
                $.ajax({
                    type: 'get',
                    url: '/warn_list/warn_image/',
                    data: {
                        'id': data['id'],
                        'is_make': 2
                    },
                    success: function (result) {
                        if (result['code'] === 200) {
                            var html = template('add-image', {
                                'data': result['data']
                            });
                            document.getElementById('image-views').innerHTML = html;
                            var image_obj = $('#image0');
                            var image_views = $('#image-views');
                            var video_views = $('#video-views');
                            image_obj.click();
                            layer.photos({
                                photos: '#image-views',
                                anim: 5,
                                end: function (index) {
                                    image_views.remove();
                                    video_views.append('<div id="image-views" style="display: none"></div>');
                                }
                            });
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
                        layer.alert('本预警暂无图片，请重试...');
                    }
                });
            }

            else if (layEvent === 'sum-warn') {
                let warn_url = data['warn_url'];
                if (warn_url.length <= 4) {
                    layer.alert('手动预警无标注图片,请选择智能预警!');
                } else {
                    // let image_sign = eval(data['image_sign']);
                    let warn_url = data['warn_url'];
                    let path = 'https://obs-swj.obs.cn-east-2.myhuaweicloud.com/';
                    let warn_image = path + warn_url;
                    json_data = {
                        'data': [
                            {'src': warn_image}
                        ]
                    };
                    layer.photos({
                        photos: json_data,
                        anim: 5
                    });
                    // layer.open({
                    //     type: 1,
                    //     title: '查看图片',
                    //     content: $('#image-url'),
                    //     area: ['1550px', '920px'],
                    //     scrollbar: false,
                    //     success: function (param) {
                    //         var canvas = document.getElementById("canvasId");
                    //         var ctx = canvas.getContext("2d");
                    //         var img = new Image();
                    //         img.src = warn_image;
                    //         img.onload = function () {
                    //             canvas.width = 1550;
                    //             canvas.height = 870;
                    //             ctx.strokeStyle = "#f00";
                    //             ctx.lineWidth = '5';
                    //             ctx.lineHeight = '5';
                    //             ctx.drawImage(img, 0, 0, 1920 * 0.8, 1080 * 0.8);
                    //             ctx.strokeRect(image_sign[0] * 0.8, image_sign[1] * 0.8, image_sign[2] * 0.8, image_sign[3] * 0.8);
                    //         }
                    //     },
                    //     cancel: function (index, layero) {
                    //         var canvas = document.getElementById("canvasId");
                    //         var ctx = canvas.getContext("2d");
                    //         layer.close(index);
                    //         ctx.clearRect(0, 0, 1920 * 0.8, 1080 * 0.8);
                    //     },
                    // })
                }
            }

            else if (layEvent === 'view-video') {
                // 弹窗查看视频
                layer.open({
                    type: 1,
                    title: '播放预警视频',
                    area: '700px',
                    content: $('#video-views'),
                    btn: '点击关闭',
                    success: function () {
                        var video_url = data['video_url']; // 获取播放地址
                        var player = videojs('play-video');
                        player.ready(function () {
                            var myPlayer = this;
                            myPlayer.reset();
                            myPlayer.src({
                                type: "video/mp4",
                                src: video_url
                            });
                            myPlayer.load(video_url); // 这个需要从新加载地址...
                            myPlayer.play(); // 点击播放
                        });
                    },
                    yes: function (index, layero) {
                        layer.close(index);
                    }
                })
            }
        });

        // ******************************************

        // 选项卡 - 已完成
        table.render({
            elem: '#table-sum2',
            height: 'full', // 表格高度始终填满
            even: true, //　列表隔行颜色
            size: 'lg',
            method: 'get', // 请求方法
            url: '/warn_list/newsum_list/', // 数据接口
            where: {
                'is_make': 3
            },
            page: true, // 开启分页　可传入laypage参数
            toolbar: 'true',
            limit: 12,
            text: '暂无数据...',
            cols: [
                [ // 表头　需要显示的数据列
                    // {
                    //     type: 'checkbox',
                    //     fixed: 'left'
                    // },
                    {
                        field: 'event_id',
                        title: '预警编号',
                        sort: true,
                    },
                    {
                        field: 'type_name',
                        title: '任务类型',
                    },
                    {
                        field: 'warn_type',
                        title: '预警类型',
                    },
                    {
                        field: 'map_name',
                        title: '所属监控点',
                    },
                    {
                        field: 'warn_url',
                        title: '事件图片',
                        toolbar: '#sum-image'
                    },
                    {
                        field: 'images',
                        title: '证据图片',
                        templet: '#warn-image'
                    },
                    {
                        field: 'video_url',
                        title: '证据视频',
                        templet: '#warn-video'
                    },
                    {
                        field: 'images_url',
                        title: '执法图片',
                        templet: '#manage-images'
                    },
                    {
                        field: 'result',
                        title: '执法意见',
                    },
                    {
                        field: 'manage_user',
                        title: '城管处理员'
                    },
                    {
                        field: 'user',
                        title: '平台处理员'
                    },
                    {
                        field: 'add_time',
                        title: '发生时间',
                        sort: true,
                    }
                ]
            ]
        });

        //　监听工具条 is-make=3
        table.on('tool(warnlist2)', function (obj) {
            var data = obj.data; // 获取当前行数据
            var layEvent = obj.event; // lay-event的值
            if (layEvent === 'view-image') {
                // 弹窗查看图片
                $.ajax({
                    type: 'get',
                    url: '/warn_list/warn_image/',
                    data: {
                        'id': data['id'],
                    },
                    success: function (result) {
                        if (result['code'] === 200) {
                            var html = template('add-image', {
                                'data': result['data']
                            });
                            document.getElementById('image-views').innerHTML = html;
                            var image_obj = $('#image0');
                            var image_views = $('#image-views');
                            var video_views = $('#video-views');
                            image_obj.click();
                            layer.photos({
                                photos: '#image-views',
                                anim: 5,
                                end: function (index) {
                                    image_views.remove();
                                    video_views.append('<div id="image-views" style="display: none"></div>');
                                }
                            });
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
                        layer.alert('本预警暂无图片，请重试...');
                    }
                });
            }

            else if (layEvent === 'sum-warn') {
                let warn_url = data['warn_url'];
                if (warn_url.length <= 4) {
                    layer.alert('手动预警无标注图片,请选择智能预警!');
                } else {
                    // let image_sign = eval(data['image_sign']);
                    let warn_url = data['warn_url'];
                    let path = 'https://obs-swj.obs.cn-east-2.myhuaweicloud.com/';
                    let warn_image = path + warn_url;
                    json_data = {
                        'data': [
                            {'src': warn_image}
                        ]
                    };
                    layer.photos({
                        photos: json_data,
                        anim: 5
                    });
                    // layer.open({
                    //     type: 1,
                    //     title: '查看图片',
                    //     content: $('#image-url'),
                    //     area: ['1550px', '920px'],
                    //     scrollbar: false,
                    //     success: function (param) {
                    //         var canvas = document.getElementById("canvasId");
                    //         var ctx = canvas.getContext("2d");
                    //         var img = new Image();
                    //         img.src = warn_image;
                    //         img.onload = function () {
                    //             canvas.width = 1550;
                    //             canvas.height = 870;
                    //             ctx.strokeStyle = "#f00";
                    //             ctx.lineWidth = '5';
                    //             ctx.lineHeight = '5';
                    //             ctx.drawImage(img, 0, 0, 1920 * 0.8, 1080 * 0.8);
                    //             ctx.strokeRect(image_sign[0] * 0.8, image_sign[1] * 0.8, image_sign[2] * 0.8, image_sign[3] * 0.8);
                    //         }
                    //     },
                    //     cancel: function (index, layero) {
                    //         var canvas = document.getElementById("canvasId");
                    //         var ctx = canvas.getContext("2d");
                    //         layer.close(index);
                    //         ctx.clearRect(0, 0, 1920 * 0.8, 1080 * 0.8);
                    //     },
                    // })
                }
            }

            else if (layEvent === 'view-video') {
                // 弹窗查看视频
                layer.open({
                    type: 1,
                    title: '播放预警视频',
                    area: '700px',
                    content: $('#video-views'),
                    btn: '点击关闭',
                    success: function () {
                        var video_url = data['video_url']; // 获取播放地址
                        var player = videojs('play-video');
                        player.ready(function () {
                            var myPlayer = this;
                            myPlayer.reset();
                            myPlayer.src({
                                type: "video/mp4",
                                src: video_url
                            });
                            myPlayer.load(video_url); // 这个需要从新加载地址...
                            myPlayer.play(); // 点击播放
                        });
                    },
                    yes: function (index, layero) {
                        layer.close(index);
                    }
                })
            }
            else if (layEvent === 'manage-image') {
                // 弹窗查看执法图片
                $.ajax({
                    type: 'get',
                    url: '/warn_list/manage_image/',
                    data: {
                        'id': data['id'],
                    },
                    success: function (result) {
                        if (result['code'] === 200) {
                            var html = template('add-manage', {
                                'data': result['data']
                            });

                            document.getElementById('manage-views').innerHTML = html;
                            var images_obj = $('#images0');
                            var images_views = $('#manage-views');
                            var video_views = $('#image-views');
                            images_obj.click();
                            layer.photos({
                                photos: '#manage-views',
                                anim: 5,
                                end: function (index) {
                                    images_views.remove();
                                    video_views.append('<div id="manage-views" style="display: none"></div>');
                                }
                            });
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
                        layer.alert('本预警暂无图片，请重试...');
                    }
                });

            }
        });

        // ******************************************

        // 选项卡 - 已丢弃
        table.render({
            elem: '#table-sum3',
            height: 'full', // 表格高度始终填满
            even: true, //　列表隔行颜色
            size: 'lg',
            method: 'get', // 请求方法
            url: '/warn_list/newsum_list/', // 数据接口
            where: {
                'is_make': 4
            },
            page: true, // 开启分页　可传入laypage参数
            toolbar: 'true',
            limit: 12,
            text: '暂无数据...',
            cols: [
                [ // 表头　需要显示的数据列
                    // {
                    //     type: 'checkbox',
                    //     fixed: 'left'
                    // },
                    {
                        field: 'event_id',
                        title: '预警编号',
                        sort: true,
                    },
                    {
                        field: 'type_name',
                        title: '任务类型',
                    },
                    {
                        field: 'warn_type',
                        title: '预警类型',
                    },
                    {
                        field: 'map_name',
                        title: '所属监控点',
                    },
                    {
                        field: 'warn_url',
                        title: '事件图片',
                        toolbar: '#sum-image'
                    },
                    {
                        field: 'images',
                        title: '证据图片',
                        templet: '#warn-image'
                    },
                    {
                        field: 'video_url',
                        title: '证据视频',
                        templet: '#warn-video'
                    },
                    {
                        field: 'result',
                        title: '当前状态'
                    },
                    {
                        field: 'manage_user',
                        title: '城管处理员'
                    },
                    {
                        field: 'user',
                        title: '平台处理员'
                    },
                    {
                        field: 'add_time',
                        title: '发生时间',
                        sort: true,
                    }
                ]
            ]
        });

        //　监听工具条 is-make=4
        table.on('tool(warnlist3)', function (obj) {
            var data = obj.data; // 获取当前行数据
            var layEvent = obj.event; // lay-event的值
            if (layEvent === 'view-image') {
                // 弹窗查看图片
                $.ajax({
                    type: 'get',
                    url: '/warn_list/warn_image/',
                    data: {
                        'id': data['id'],
                        'is_make': 4
                    },
                    success: function (result) {
                        if (result['code'] === 200) {
                            var html = template('add-image', {
                                'data': result['data']
                            });
                            document.getElementById('image-views').innerHTML = html;
                            var image_obj = $('#image0');
                            var image_views = $('#image-views');
                            var video_views = $('#video-views');
                            image_obj.click();
                            layer.photos({
                                photos: '#image-views',
                                anim: 5,
                                end: function (index) {
                                    image_views.remove();
                                    video_views.append('<div id="image-views" style="display: none"></div>');
                                }
                            });
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
                        layer.alert('本预警暂无图片，请重试...');
                    }
                });
            }

            else if (layEvent === 'sum-warn') {
                let warn_url = data['warn_url'];
                if (warn_url.length <= 4) {
                    layer.alert('手动预警无标注图片,请选择智能预警!');
                } else {
                    // let image_sign = eval(data['image_sign']);
                    let warn_url = data['warn_url'];
                    let path = 'https://obs-swj.obs.cn-east-2.myhuaweicloud.com/';
                    let warn_image = path + warn_url;
                    json_data = {
                        'data': [
                            {'src': warn_image}
                        ]
                    };
                    layer.photos({
                        photos: json_data,
                        anim: 5
                    });
                    // layer.open({
                    //     type: 1,
                    //     title: '查看图片',
                    //     content: $('#image-url'),
                    //     area: ['1550px', '920px'],
                    //     scrollbar: false,
                    //     success: function (param) {
                    //         var canvas = document.getElementById("canvasId");
                    //         var ctx = canvas.getContext("2d");
                    //         var img = new Image();
                    //         img.src = warn_image;
                    //         img.onload = function () {
                    //             canvas.width = 1550;
                    //             canvas.height = 870;
                    //             ctx.strokeStyle = "#f00";
                    //             ctx.lineWidth = '5';
                    //             ctx.lineHeight = '5';
                    //             ctx.drawImage(img, 0, 0, 1920 * 0.8, 1080 * 0.8);
                    //             ctx.strokeRect(image_sign[0] * 0.8, image_sign[1] * 0.8, image_sign[2] * 0.8, image_sign[3] * 0.8);
                    //         }
                    //     },
                    //     cancel: function (index, layero) {
                    //         var canvas = document.getElementById("canvasId");
                    //         var ctx = canvas.getContext("2d");
                    //         layer.close(index);
                    //         ctx.clearRect(0, 0, 1920 * 0.8, 1080 * 0.8);
                    //     },
                    // })
                }
            }

            else if (layEvent === 'view-video') {
                // 弹窗查看视频
                layer.open({
                    type: 1,
                    title: '播放预警视频',
                    area: '700px',
                    content: $('#video-views'),
                    btn: '点击关闭',
                    success: function () {
                        var video_url = data['video_url']; // 获取播放地址
                        var player = videojs('play-video');
                        player.ready(function () {
                            var myPlayer = this;
                            myPlayer.reset();
                            myPlayer.src({
                                type: "video/mp4",
                                src: video_url
                            });
                            myPlayer.load(video_url); // 这个需要从新加载地址...
                            myPlayer.play(); // 点击播放
                        });
                    },
                    yes: function (index, layero) {
                        layer.close(index);
                    }
                })
            }
        });
    });
};


$(function () {
    var sum_list = new SumList();
    sum_list.run();
});