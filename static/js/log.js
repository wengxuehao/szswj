function Log() {

}


Log.prototype.run = function (params) {
    var self = this;
    self.LogEvent();
};


Log.prototype.LogEvent = function () {

    // 操作日志页引入相应模块
    layui.use(['table', 'laypage', 'layer'], function () {
        var table = layui.table,
            layer = layui.layer;

        // 表格
        table.render({
            elem: '#user-log',
            height: 'full', // 表格高度始终填满
            even: true, //　列表隔行颜色
            size: 'lg',
            method: 'get', // 请求方法
            url: '/public/user_log/', // 数据接口
            page: true, // 开启分页　可传入laypage参数
            toolbar: '#log-tool',
            limit: 12,
            text: '暂无数据...',
            cols: [
                [ // 表头　需要显示的数据列
                    {
                        type: 'checkbox',
                        fixed: 'left'
                    },
                    {
                        field: 'user',
                        title: '用户名',
                        sort: true,
                        width: 200
                    },
                    {
                        field: 'ip_address',
                        title: 'ip地址',
                        sort: true,
                        width: 200
                    },
                    {
                        field: 'user_type',
                        title: '操作类型',
                        sort: true,
                        width: 200
                    },
                    {
                        field: 'desc',
                        title: '操作描述',
                        sort: true
                    },
                    {
                        field: 'add_time',
                        title: '添加时间',
                        sort: true,
                        width: 200
                    },
                ]
            ]
        });

        // 多选框处理
        table.on('toolbar(userlog)', function (obj) {
            switch (obj.event) {
                case 'log-del':
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
                            content: '确认删除吗？',
                            btn: ['确认', '取消'],
                            yes: function (index) {
                                $.ajax({
                                    type: 'post',
                                    url: '/public/user_log/',
                                    data: {
                                        'data_list': data_str,
                                    },
                                    success: function (result) {
                                        if (result['code'] === 200) {
                                            layer.alert('删除成功~');
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
                            },
                            btn2: function (index) {
                                layer.close(index);
                                parent.location.reload();
                            }
                        })
                    }
                    break;
            }
        });
    });
};


$(function () {
    var log = new Log();
    log.run();
});