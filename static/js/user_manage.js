function UserManage() {

}

UserManage.prototype.run = function () {
    var self = this;
    self.AddRoleEvent();
    // self.LoginEvent();
};

// 用户登录
// UserManage.prototype.LoginEvent = function (params) {
//     layui.use('layer', function (params) {
//         var layer = layui.layer;
//         var loginBtn = $('#login-button');
//         loginBtn.click(function () {
//             var username = $("input[name='username']").val();
//             var password = $("input[name='password']").val();
//             $.ajax({
//                 type: 'post',
//                 url: '/users/login/',
//                 data: {
//                     'username': username,
//                     'password': password
//                 },
//                 success: function (result) {
//                     if (result['code'] === 200) {
//                         window.location.href = '/'; //　跳转
//                     } else {
//                         alert('账号或密码错误,请重试!');
//                     }
//                 }
//             })
//         });
//     });
// };

//　用户点击添加用户、角色
UserManage.prototype.AddRoleEvent = function () {
    layui.use(['form', 'table', 'layer', 'laypage', 'element'], function () {
        var form = layui.form,
            table = layui.table,
            element = layui.element,
            layer = layui.layer;

        //　××××××××× 新增管理员逻辑　××××××××××

        // 点击新增按钮弹窗
        var addManage = $('#add-manage');
        addManage.click(function () {

            var group_id; // 定义组全局变量
            layer.open({
                type: 1,
                title: '添加管理员',
                content: $('#add-user'),
                btn: '点击确认',
                success: function () {
                    $.ajax({
                        type: 'get',
                        url: '/users/all_group/',
                        data: {},
                        success: function (result) {
                            if (result['code'] === 200) {
                                var html = template('add-user-perms', {'data': result['data']});
                                document.getElementById('add-userperm').innerHTML = html;
                                form.render();
                                //  下拉菜单获取选中值
                                form.on('select(select-perm)', function (data) {
                                    var id = data.value;
                                    group_id = id;
                                });

                            } else {
                                layer.alert('获取数据失败,请重试...');
                            }
                        },
                        error: function () {
                            layer.alert('获取数据失败,请重试...');
                        }
                    });
                },
                yes: function (index) {
                    var username = $("input[name='username']").val();
                    var password = $("input[name='password']").val();
                    var email = $("input[name='email']").val();
                    // var csrf = $('input[name="csrfmiddlewaretoken"]').val();
                    $.ajax({
                        type: 'post',
                        url: '/users/user_admin/',
                        data: {
                            'username': username,
                            'password': password,
                            'email': email,
                            'group_id': group_id,
                            // 'csrfmiddlewaretoken': csrf
                        },
                        success: function (result) {
                            if (result['code'] === 200) {
                                layer.close(index);
                                layer.alert('添加成功');
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
                            layer.alert('添加失败,请重试~');
                        }
                    });
                }
            });
        });

        //　××××××××× 新增角色权限逻辑　××××××××××

        // 点击新增按钮弹窗
        var AddRole = $('#create-role');
        AddRole.click(function () {
            layer.open({
                type: 1,
                title: '添加角色',
                content: $('#add-role'),
                btn: '点击确认',
                yes: function (index) {
                    var roleName = $('#role-name').val();
                    var roleDesc = $('#role-desc').val();
                    // var csrf = $('input[name="csrfmiddlewaretoken"]').val();

                    obj = document.getElementsByName('perm');
                    check_val = [];
                    for (k in obj) {
                        if (obj[k].checked) {
                            check_val.push(obj[k].value);
                        }
                    }
                    var check_val = check_val.join(',');
                    $.ajax({
                        type: 'post',
                        url: '/users/user_group/',
                        data: {
                            'name': roleName,
                            'desc': roleDesc,
                            'check_val': check_val,
                            // 'csrfmiddlewaretoken': csrf
                        },
                        success: function (result) {
                            if (result['code'] === 200) {
                                layer.close(index);
                                layer.alert('添加成功~');
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
                            layer.alert('修改失败,请重试~');
                        }
                    });
                }
            });
        });

        // ******************************************

        //选项卡切换刷新
        var layid = location.hash.replace(/^#role-tab=/, '');
        element.tabChange('role-tab', layid);

        // 监听tab切换，改变地址hash值
        element.on('tab(role-tab)', function (params) {
            location.hash = 'role-tab=' + this.getAttribute('lay-id');
        });

        // 选项卡用户管理
        table.render({
            elem: '#user-admin',
            height: 'full', // 表格高度始终填满
            even: true, //　列表隔行颜色
            size: 'lg',
            method: 'get', // 请求方法
            url: '/users/user_admin/', // 数据接口
            page: true, // 开启分页　可传入laypage参数
            toolbar: true,
            limit: 12,
            text: '暂无数据...',
            cols: [
                [ // 表头　需要显示的数据列
                    // {
                    //     type: 'checkbox',
                    //     fixed: 'left'
                    // },
                    {
                        field: 'username',
                        title: '用户名',
                        sort: true,
                    },
                    {
                        field: '',
                        title: '所属分组',
                        sort: true,
                        templet: function (d) {
                            if (d['groups'].length == 0) {
                                return '<div>' + '没有分组' + '</div>'
                            } else {
                                return '<div>' + d["groups"][0]["name"] + '</div>'
                            }
                        }
                    },
                    {
                        field: 'email',
                        title: '邮箱',
                        sort: true
                    },
                    {
                        field: 'date_joined',
                        title: '添加时间',
                        sort: true
                    },
                    {
                        field: 'id',
                        title: '事件处理',
                        fixed: 'right',
                        align: 'center',
                        toolbar: '#user-make'
                    },
                ]
            ]
        });

        //　选项卡用户管理　－　监听工具条
        table.on('tool(useradmin)', function (obj) {
            var data = obj.data; // 获取当前行数据
            var layEvent = obj.event; // lay-event的值
            var checkStatus = table.checkStatus('user-admin');

            if (layEvent === 'user-del') {
                layer.confirm('确认删除吗?', function (index) {
                    $.ajax({
                        type: 'delete',
                        url: '/users/user_admin/',
                        data: {
                            'id': data['id']
                        },
                        success: function (result) {
                            if (result['code'] === 200) {
                                layer.close(index);
                                layer.alert('删除成功~');
                                setTimeout('parent.location.reload();', 1000);
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
                            layer.alert('删除失败，请重试~');
                        }
                    });
                    layer.close(index);
                    //向服务端发送删除指令
                });
            } else if (layEvent === 'user-modify') {
                layer.open({
                    type: 1,
                    title: '修改分组信息',
                    content: $('#modify-user'),
                    btn: '点击确认',
                    success: function (layero, index) {
                        $.ajax({
                            type: 'get',
                            url: '/users/all_group/',
                            data: {},
                            success: function (result) {
                                if (result['code'] === 200) {
                                    var html = template('change-user-perms', {'data': result['data']});
                                    document.getElementById('change-userperm').innerHTML = html;
                                    form.render();
                                    //  下拉菜单获取选中值
                                    form.on('select(select-perms)', function (data) {
                                        var id = data.value;
                                        user_group_id = id;
                                    });
                                } else {
                                    layer.alert('获取数据失败,请重试...');
                                }
                            },
                            error: function () {
                                layer.alert('获取数据失败,请重试...');
                            }
                        });
                    },
                    yes: function (index, layero) {
                        if (typeof user_group_id != 'undefined') {
                            $.ajax({
                                type: 'post',
                                url: '/users/user_data/',
                                data: {
                                    'group_id': user_group_id,
                                    'id': data['id']
                                },
                                success: function (result) {
                                    if (result['code'] === 200) {
                                        layer.alert('修改成功~');
                                        setTimeout('parent.location.reload();', 1000);
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
                        } else {
                            layer.alert('请选择角色组');
                        }
                    }
                });
            }
            else if (layEvent === 'user-password') {
                layer.open({
                    type: 1,
                    title: '修改密码',
                    content: $('#modify-password'),
                    btn: '点击确认',
                    yes: function (index, layero) {
                        var password = $("input[name='password1']").val();
                        // var csrf = $('input[name="csrfmiddlewaretoken"]').val();
                        $.ajax({
                            type: 'post',
                            url: '/users/modify_password/',
                            data: {
                                'user_id': data['id'],
                                'password': password,
                                // 'csrfmiddlewaretoken': csrf
                            },
                            success: function (result) {
                                if (result['code'] === 200) {
                                    layer.alert('修改成功');
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
                    }
                })
            }
        });

        // **********************************************

        // 选项卡角色管理 － 渲染
        table.render({
            elem: '#user-role',
            height: 'full', // 表格高度始终填满
            even: true, //　列表隔行颜色
            size: 'lg',
            method: 'get', // 请求方法
            url: '/users/user_group/', // 数据接口
            page: true, // 开启分页　可传入laypage参数
            toolbar: true,
            limit: 1,
            // limits:[1],
            cols: [
                [ // 表头　需要显示的数据列
                    // {
                    //     type: 'checkbox',
                    //     fixed: 'left'
                    // },
                    {
                        field: 'group_name',
                        title: '角色名',
                        sort: true,
                    },
                    {
                        field: 'desc',
                        title: '权限描述',
                        sort: true
                    },
                    // {
                    //     field: 'id',
                    //     title: '角色权限',
                    //     templet: '#role-perm'
                    // },
                    {
                        field: 'add_time',
                        title: '添加时间',
                        sort: true
                    },
                    {
                        field: 'id',
                        title: '相关操作',
                        fixed: 'right',
                        align: 'center',
                        toolbar: '#role-make'
                    },
                ]
            ]
        });

        //　选项卡角色管理　－　监听工具条
        table.on('tool(userrole)', function (obj) {
            var data = obj.data; // 获取当前行数据
            var layEvent = obj.event; // lay-event的值
            var tr = obj.tr; // 获取当前行 tr 的DOM对象
            var checkStatus = table.checkStatus('user-role');

            if (layEvent === 'role-del') {
                layer.confirm('确认删除吗?', function (index) {
                    // obj.del(); //删除对应行（tr）的DOM结构，并更新缓存

                    $.ajax({
                        type: 'delete',
                        url: '/users/user_group/',
                        data: {
                            'id': data['id']
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
                        error: function (param) {
                            layer.alert('删除失败，请重试...');
                        }
                    });

                    layer.close(index);
                    //向服务端发送删除指令
                });
            } else if (layEvent === 'role-modify') {
                layer.open({
                    type: 1,
                    title: '修改角色信息',
                    content: $('#modify-role'),
                    btn: '点击确认',
                    yes: function (index, layero) {
                        var role_name = $('input[name="modify-name"]').val();
                        $.ajax({
                            type: 'post',
                            url: '/users/role_update/',
                            data: {
                                'name': role_name,
                                'id': data['id']
                            },
                            success: function (result) {
                                if (result['code'] === 200) {
                                    layer.alert('修改成功');
                                    setTimeout('parent.location.reload()', 1000);
                                } else {
                                    layer.alert('修改失败,请重试.');
                                }
                            }
                        });
                    }
                });
            } else if (layEvent === 'view-perm') {
                layer.open({
                    type: 1,
                    title: '角色权限信息',
                    area: '300px',
                    content: $('#view-userperm'),
                    btn: '点击关闭',
                    success: function () {
                        $.ajax({
                            type: 'get',
                            url: '/users/rec_group/',
                            data: {
                                'group_id': data['id']
                            },
                            success: function (result) {
                                if (result['code'] === 200) {
                                    var data = result['data'];
                                    var html = template('user-perms', {'data': data});
                                    document.getElementById('view-userperm').innerHTML = html;
                                } else {
                                    layer.alert('获取数据失败,请重试...');
                                }
                            },
                            error: function () {
                                layer.alert('获取数据失败,请重试...');
                            }
                        });
                    },
                    yes: function (index, layero) {
                        layer.close(index);
                    }
                });
            }
        });
    });
};


// 查看权限格式转化
// $(function () {
//     if (window.template) {
//         template.defaults.imports.newName = function (dateValue) {
//             var name_list = ['Can view', 'Can add', 'Can change','Can delete'];
//             var value_list = ['查看', '添加', '修改', '删除'];
//             for (var i=0;i<name_list.length;i++) {
//                 var view = new RegExp(name_list[i]);
//                 let bool_value = view.test(dateValue);
//                 if (bool_value) {
//                     new_name = dateValue.replace(name_list[i], value_list[i]);
//                     return new_name
//                 }else{
//                     // console.log('这是错的');
//                 }
//             }
//         }
//     }
// });


$(function () {
    var user_manage = new UserManage();
    user_manage.run();
});
