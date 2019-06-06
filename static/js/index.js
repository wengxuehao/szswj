function Index() {

}

Index.prototype.run = function () {
    var self = this;
    self.listenNewWarnEvent();
};

// 屏幕尺寸变化,刷新页面
$(window).resize(function () {
    window.location.reload();
});

// 首页预警点击图片预览
function view_image(id) {
    layui.use(['layer'], function () {
        var layer = layui.layer;
        $.ajax({
            type: 'get',
            url: '/public/index_warn/',
            data: {
                'id': id
            },
            success: function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    // let image_sign = eval(data['image_sign']);
                    let image_url = data['image_url'];
                    json_data = {
                        'data': [
                            {'src': image_url}
                        ]
                    };
                    layer.photos({
                        photos: json_data,
                        anim: 5
                    });
                    // layer.open({
                    //     type: 1,
                    //     title: '查看图片',
                    //     content: $('#view-image'),
                    //     area: ['1550px', '920px'],
                    //     scrollbar: false,
                    //     success: function (param) {
                    //         var canvas = document.getElementById("canvasId");
                    //         var ctx = canvas.getContext("2d");
                    //         var img = new Image();
                    //         img.src = image_url;
                    //         img.onload = function () {
                    //             canvas.width = 1550;
                    //             canvas.height = 870;
                    //             ctx.strokeStyle = "#f00";
                    //             ctx.lineWidth = '5';
                    //             ctx.lineHeight = '5';
                    //             ctx.drawImage(img, 0, 0, 1920 * 0.8, 1080 * 0.8);
                    //             ctx.strokeRect(image_sign[0] * 0.8, image_sign[1] * 0.8, image_sign[2] * 0.8, image_sign[3] * 0.8);
                    //         }
                    //     }
                    // })
                } else {
                    return
                }
            },
            error: function () {
                return
            }
        });
    });
}

// 定时异步刷新主页右上方最新预警信息
Index.prototype.listenNewWarnEvent = function () {
    $(function () {
        warn();
        setInterval(function () {
            warn();
            var ChangeWarn = $('#change-warn');
            ChangeWarn.empty(); // 再次刷新前 先移除dom
        }, 10000);
    });

    function warn() {
        $.ajax({
            type: 'get',
            url: '/public/index_warn/',
            data: {},
            success: function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var html = template('index-warn', {
                        'data': data
                    });
                    document.getElementById('change-warn').innerHTML = html;
                } else {
                    return
                }
            },
            error: function () {
                return
            }
        });
    }
};

$(function () {
    var index = new Index();
    index.run();
});

// $(function () {
//    var allBtn = $('#all-view');
//    allBtn.click(function () {
//        window.location.href = '/public/index_data/';
//    })
// });

