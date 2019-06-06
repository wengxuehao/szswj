function WarnManage() {

}


WarnManage.prototype.run = function (params) {
    var self = this;
    self.WarnManageEvent();
};


WarnManage.prototype.WarnManageEvent = function (params) {

    // 操作日志页引入相应模块
    layui.use(['table', 'laypage', 'layer', 'tree', 'form'], function () {
        var table = layui.table,
            form = layui.form,
            laypage = layui.laypage,
            tree = layui.tree,
            layer = layui.layer;

        table.render({
            elem: '#manage-table',
            height: 'full', // 表格高度始终填满
            even: true, //　列表隔行颜色
            size: 'lg',
            method: 'get', // 请求方法
            url: '/warn_list/manage/', // 数据接口
            page: true, // 开启分页　可传入laypage参数
            toolbar: '#warnmanage-tool',
            limit: 10,
            text: '暂无数据...',
            cols: [
                [ // 表头　需要显示的数据列
                    // {
                    //     type: 'checkbox',
                    //     fixed: 'left'
                    // },
                    {
                        field: 'process_id',
                        title: '任务编号',
                        sort: true
                    },
                    {
                        field: 'type_name',
                        title: '预警类型',
                    },
                    {
                        field: 'dev_id',
                        title: '所属监控点',
                    },
                    {
                        field: 'name',
                        title: '监控点名称',
                    },
                    {
                        field: 'add_time',
                        title: '发生时间',
                        sort: true,
                    },
                    {
                        field: 'id',
                        title: '任务处理',
                        fixed: 'right',
                        align: 'center',
                        toolbar: '#warn-manage',
                        width: 200
                    },
                ]
            ]
        });

        //　监听工具条
        table.on('tool(warnmanage)', function (obj) {
            var data = obj.data; // 获取当前行数据
            var layEvent = obj.event; // lay-event的值
            var tr = obj.tr; // 获取当前行 tr 的DOM对象
            var checkStatus = table.checkStatus('manage-table');

            if (layEvent === 'manage-del') {
                var process_id = data['process_id'];
                layer.confirm('确认删除吗?', function (index) {
                    // obj.del(); //删除对应行（tr）的DOM结构，并更新缓存
                    $.ajax({
                        type: 'delete',
                        url: '/warn_list/del_manage/',
                        data: {
                            'process_id': process_id
                        },
                        success: function (result) {
                            if (result['code'] === 200) {
                                layer.alert('删除成功');
                                setTimeout('window.location.reload();', 1000);
                            }
                        }
                    });
                    layer.close(index);
                    //向服务端发送删除指令
                });
            }
        });

        // 工具条
        table.on('toolbar(warnmanage)', function (obj) {
            switch (obj.event) {
                // 点击新增任务弹窗选择
                case 'add-warnmanage': {        
                    var dev_id = '';
                    $.ajax({
                        type: 'get',
                        url: '/warn_list/search_manage/',
                        data: {
                            'dev_id': dev_id
                        },
                        success: function (result) {
                            if (result['code'] === 200) {
                                var data = result['data'];
                                var html = template('manage-list', {
                                    'data': data
                                });
                                document.getElementById('manage-desc').innerHTML = html;
                                form.render();

                                layer.open({
                                    type: 1,
                                    title: '创建处理任务',
                                    area: ['700px', '460px'],
                                    content: $('#warnmanage-tree'),
                                    btn: '点击关闭',
                                    success: function (layero, index) {
                                        // 成功弹出窗口执行　查询后端目录树
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
                                                        skin: 'demo',

                                                        //　树节点 - 点击
                                                        click: function (node) {
                                                            //　点击树节点获取数值操作
                                                            var dev_id = node['id'];
                                                            var resource_id = node['resource_id'];
                                                            var city_id = node['city'];
                                                            if (resource_id != null) {
                                                                // 点击监控点创建视频流任务
                                                                $.ajax({
                                                                    type: 'post',
                                                                    url: '/warn_list/stream/',
                                                                    data: {
                                                                        resource_id: resource_id
                                                                    },
                                                                    success: function (result) {
                                                                        if (result['code'] === 200) {
                                                                            // 查询监控点已经创建的分析任务
                                                                            var data = result['data'];
                                                                            var json_data = JSON.parse(data);
                                                                            console.log(json_data);
                                                                            var stream_id = json_data['stream_id'];

                                                                            var manageBtn = $('#rec-manage');
                                                                            manageBtn.click(function () {
                                                                                var type_id = new Array();
                                                                                $('input[name="manage"]:checked').each(function () {
                                                                                    type_id.push($(this).val()); //向数组中添加元素  
                                                                                });
                                                                                var idstr = type_id.join(','); //将数组元素连接起来以构建一个字符串  

                                                                                $.ajax({
                                                                                    type: 'post',
                                                                                    url: '/warn_list/new_manage/',
                                                                                    data: {
                                                                                        'type_id': idstr,
                                                                                        'stream_id': stream_id,
                                                                                        'resource_id': resource_id
                                                                                    },
                                                                                    success: function (result) {
                                                                                        if (result['code'] === 200) {
                                                                                            layer.alert(result['message']);
                                                                                        }
                                                                                    }
                                                                                });
                                                                            });
                                                                        } else {
                                                                            layer.alert('创建视频流失败，请重试...');
                                                                        }
                                                                    }
                                                                });
                                                            } else {
                                                                layer.msg('请点击具体监控点.');
                                                            }
                                                        }
                                                    });
                                                } else {
                                                    alert('获取数据失败...');
                                                }
                                            }
                                        });
                                    },
                                    yes: function (index) {
                                        layer.close(index);
                                        parent.location.reload();
                                    },
                                    cancel: function (index, layero) {
                                        layer.close(index);
                                        parent.location.reload();
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
                        }
                    });
                }
                break;
            }
        });
    });
};


$(function (param) {
    var warn_manage = new WarnManage();
    warn_manage.run();
});