function Warn() {

}

Warn.prototype.run = function () {
    var self = this;
    self.listenWarnEvent();
};

Warn.prototype.listenWarnEvent = function () {
    //注意：导航 依赖 element 模块，否则无法进行功能性操作
    layui.use(['table', 'element', 'form', 'layer'], function () {
        var table = layui.table,
            form = layui.form,
            layer = layui.layer,
            element = layui.element;

        var check_value = [];
        var check_dev = [];
        var check_manage = [];
        var check_day = [];
        table.render({
            elem: '#warn-table',
            height: 'full', // 表格高度始终填满
            even: true, //　列表隔行颜色
            size: 'lg',
            method: 'get', // 请求方法
            where: {
                check_value: check_value,
                check_dev: check_dev,
                check_manage: check_manage,
                check_day: check_day
            },
            url: '/warn_list/rec_data/', // 数据接口
            page: true, // 开启分页　可传入laypage参数
            toolbar: '#warn-tool',
            limit: 12,
            text: {
                none: '暂无数据...'
            },
            cols: [
                [ // 表头　需要显示的数据列
                    {
                        type: 'checkbox',
                        fixed: 'left'
                    },
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
                        sort: true,
                    },
                    {
                        field: 'warn_url',
                        title: '事件图片',
                        toolbar: '#warns-image'
                    },
                    {
                        field: 'images',
                        title: '证据图片',
                        toolbar: '#warn-image'
                    },
                    {
                        field: 'video_url',
                        title: '证据视频',
                        toolbar: '#warn-video'
                    },
                    {
                        field: 'add_time',
                        title: '发生时间',
                        sort: true,
                    },
                    {
                        field: 'id',
                        title: '事件处理',
                        fixed: 'right',
                        align: 'center',
                        toolbar: '#warn-make'
                    },
                ]
            ],
            done: function (res, curr, count) {
                // $(".layui-laypage-btn")[0].click();
            }
        });

        // 多选框处理
        table.on('toolbar(warnlist)', function (obj) {
            switch (obj.event) {
                // 一键跳过
                case 'make-pass':
                    var check_data = table.checkStatus(obj.config.id);
                    if (check_data.data.length == 0) {
                        layer.alert('请先勾选需要跳过的行...');
                    } else {
                        var data_list = new Array();
                        for (var i = 0; i < check_data.data.length; i++) {
                            data_list.push(check_data.data[i]['id'])
                        }
                        var data_str = data_list.join(',');
                        layer.open({
                            content: '确认跳过吗？',
                            btn: ['确认', '取消'],
                            yes: function (index, layero) {
                                $.ajax({
                                    type: 'post',
                                    url: '/warn_list/rec_data/',
                                    data: {
                                        'data_list': data_str
                                    },
                                    success: function (result) {
                                        if (result['code'] === 200) {
                                            layer.alert('丢弃成功，您可在统计备案页面找到他们哦~');
                                            setTimeout('parent.location.reload()', 1000);
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
                                        layer.alert('丢弃失败，请重试...');
                                    }
                                });
                            },
                            btn2: function (index) {
                                layer.close(index);
                                parent.location.reload();
                            }
                        });
                    }
                    break;

                // 任务类型筛选
                case 'manage-select':
                    layer.open({
                        type: 1,
                        title: '请勾选预警类型',
                        content: $('#layer-manage-select'),
                        offset: ['100px', '500px'],
                        area: ['300px', '200px'],
                        btn: ['确认', '取消'],
                        yes: function (index) {
                            obj = document.getElementsByName('manage');
                            check_val = [];
                            for (k in obj) {
                                if (obj[k].checked) {
                                    check_val.push(obj[k].value);
                                }
                            }
                            var new_val = check_val.join(',');
                            check_manage = new_val;

                            if (check_manage.length != 0) {
                                table.reload('warn-table', {
                                    where: {
                                        check_manage: check_manage
                                    },
                                    url: '/warn_list/rec_data/', // 数据接口
                                });
                            } else if (check_manage.length == 0) {
                                parent.location.reload();
                            }
                            layer.close(index);
                        }
                    });
                    break;

                // 预警类型筛选
                case 'warn-select':
                    layer.open({
                        type: 1,
                        title: '请勾选预警类型',
                        content: $('#layer-warn-select'),
                        offset: ['100px', '500px'],
                        area: ['300px', '200px'],
                        btn: ['确认', '取消'],
                        yes: function (index) {
                            obj = document.getElementsByName('warn');
                            check_val = [];
                            for (k in obj) {
                                if (obj[k].checked) {
                                    check_val.push(obj[k].value);
                                }
                            }
                            var new_val = check_val.join(',');
                            check_value = new_val;

                            if (check_value.length != 0) {
                                table.reload('warn-table', {
                                    where: {
                                        check_value: check_value
                                    },
                                    url: '/warn_list/rec_data/', // 数据接口
                                });
                            } else if (check_value.length == 0) {
                                parent.location.reload();
                            }
                            layer.close(index);
                        }
                    });
                    break;

                // 时间筛选
                case 'day-select':
                    layer.open({
                        type: 1,
                        title: '请勾选筛选时间',
                        content: $('#layer-day-select'),
                        offset: ['100px', '500px'],
                        area: ['300px', '200px'],
                        btn: ['确认', '取消'],
                        yes: function (index) {
                            obj = document.getElementsByName('day');
                            check_day = [];
                            for (k in obj) {
                                if (obj[k].checked) {
                                    check_day.push(obj[k].value);
                                }
                            }
                            var new_val = check_day.join(',');
                            check_day = new_val;

                            if (check_day.length != 0) {
                                table.reload('warn-table', {
                                    where: {
                                        check_day: check_day
                                    },
                                    url: '/warn_list/rec_data/', // 数据接口
                                });
                            } else if (check_day.length == 0) {
                                parent.location.reload();
                            }
                            layer.close(index);
                        }
                    });
                    break;

                // 监控点筛选
                case 'dev-select':
                    layer.open({
                        type: 1,
                        title: '请勾选监控点',
                        content: $('#layer-dev-select'),
                        offset: ['100px', '500px'],
                        area: ['430px', '400px'],
                        btn: ['确认', '取消'],
                        success: function () {
                            $.ajax({
                                type: 'get',
                                url: '/public/select_dev/',
                                data: {},

                                success: function (result) {
                                    if (result['code'] === 200) {
                                        var html = template('select-dev', {
                                            'data': result['data']
                                        });
                                        document.getElementById('add-select-dev').innerHTML = html;
                                        form.render();

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
                                    layer.alert('获取失败，请重试...');
                                }
                            })
                        },
                        yes: function (index) {
                            obj = document.getElementsByName('dev');
                            check_val = [];
                            for (k in obj) {
                                if (obj[k].checked) {
                                    check_val.push(obj[k].value);
                                }
                            }
                            var new_dev = check_val.join(',');
                            check_dev = new_dev;
                            if (check_dev.length != 0) {
                                table.reload('warn-table', {
                                    where: {
                                        check_dev: check_dev
                                    },
                                    url: '/warn_list/rec_data/', // 数据接口
                                });
                            }
                            layer.close(index);
                        }
                    });
                    break;
            }
        });

        //　监听工具条
        table.on('tool(warnlist)', function (obj) {
            var data = obj.data; // 获取当前行数据
            var layEvent = obj.event; // lay-event的值

            if (layEvent === 'warn-del') {
                layer.confirm('确认丢弃吗?', function (index) {
                    $.ajax({
                        type: 'post',
                        url: '/warn_list/rec_data/',
                        data: {
                            'id': data['id']
                        },
                        success: function (result) {
                            if (result['code'] === 200) {
                                layer.alert('丢弃成功，您可在统计备案页面找到他们哦~');
                                setTimeout('parent.location.reload()', 1000);
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
                            layer.alert('删除失败，请重试...');
                        }
                    });
                    layer.close(index);
                });
            } else if (layEvent === 'warn-save') {
                layer.confirm('确认上报至城管系统吗?', function (index) {
                    console.log(data['dev_id']);
                    $.ajax({
                        type: 'post',
                        url: '/public/send_data/',
                        data: {
                            'id': data['id'],
                            'type_name': data['type_name'],
                            'video_url': data['video_url'],
                            'images': JSON.stringify(data['images']),
                            'event_id': data['event_id'],
                            'map_name': data['map_name'],
                            'warn_url': data['warn_url'],
                            'dev_id': data['dev_id']
                        },
                        success: function (result) {
                            if (result['code'] === 200) {
                                console.log(result['data']);

                                layer.alert('上报成功，您可在统计备案页面找到他们哦~');
                                setTimeout('parent.location.reload()', 1000);
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
                        }
                    })
                });
            } else if (layEvent === 'view-warns') {
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
                    // var canvas = document.getElementById("canvasId");
                    // var ctx = canvas.getContext("2d");
                    // var img = new Image();
                    // img.src = warn_image;
                    // img.onload = function () {
                    //     canvas.width = 1550;
                    //     canvas.height = 870;
                    //     ctx.strokeStyle = "#f00";
                    //     ctx.lineWidth = '5';
                    //     ctx.lineHeight = '5';
                    //     ctx.drawImage(img, 0, 0, 1920 * 0.8, 1080 * 0.8);
                    //     ctx.strokeRect(image_sign[0] * 0.8, image_sign[1] * 0.8, image_sign[2] * 0.8, image_sign[3] * 0.8);
                    // }
            //     }
            // ,
                // cancel: function (index, layero) {
                //     var canvas = document.getElementById("canvasId");
                //     var ctx = canvas.getContext("2d");
                //     layer.close(index);
                //     ctx.clearRect(0, 0, 1920 * 0.8, 1080 * 0.8);
                // },
                // })
            }
        }
    else
        if (layEvent === 'view-image') {
            // 弹窗查看图片
            $.ajax({
                type: 'get',
                url: '/warn_list/warn_image/',
                data: {
                    'id': data['id']
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
        } else if (layEvent === 'view-video') {
            // 弹窗查看视频
            layer.open({
                type: 1,
                title: '播放预警视频',
                area: '700px',
                content: $('#video-views'),
                btn: '点击确认',
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
}
)
;
}
;


$(function () {
    var warn = new Warn();
    warn.run();
});