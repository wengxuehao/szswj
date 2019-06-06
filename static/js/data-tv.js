function Echarts() {

}

Echarts.prototype.run = function (param) {
    var self = this;
    self.InitEchartsEvent();
};


// 渲染图表主逻辑
Echarts.prototype.InitEchartsEvent = function (params) {
    layui.use(['layer', 'form', 'element'], function (param) {
        var layer = layui.layer,
            element = layui.element,
            form = layui.form;

        // ************************************************************************************************

        //　初始化实例 1
        var myChart1 = echarts.init(document.getElementById('echarts-bar'), 'demo');
        $.ajax({
            type: 'get',
            url: '/public/cake_data/',
            data: {},
            success: function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var data_Spilling = data['Spilling'];
                    var data_water = data['water'];
                    myChart1.setOption({
                        angleAxis: {
                            type: 'category',
                            data: ['清晨', '上午', '下午', '傍晚', '夜晚'],
                            z: 10
                        },
                        radiusAxis: {},
                        polar: {},
                        series: [{
                            type: 'bar',
                            data: data_Spilling,
                            coordinateSystem: 'polar',
                            name: '抛物预警',
                            stack: 'a'
                        }, {
                            type: 'bar',
                            data: data_water,
                            coordinateSystem: 'polar',
                            name: '泼水预警',
                            stack: 'a'
                        }],
                        legend: {
                            orient: 'vertical',
                            left: 'left',
                            show: true,
                            data: ['抛物预警', '泼水预警']
                        },
                        color: ['#2F4554']
                    });
                }
            }
        });

        // ************************************************************************************************

        //　初始化实例 2
        var myChart2 = echarts.init(document.getElementById('echarts-broken'), 'demo');

        // 渲染前端页面
        $.ajax({
            type: 'get',
            url: '/public/top_five/',
            data: {},
            success: function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    myChart2.setOption({
                        title: {
                            text: '预警TOP5',
                            x: 'center'
                        },
                        tooltip: {
                            trigger: 'item',
                            formatter: "{a} <br/>{b}: {c} ({d}%)"
                        },
                        legend: {
                            orient: 'vertical',
                            x: 'left',
                            data: [data[0]['name'], data[1]['name'], data[2]['name'], data[3]['name'], data[4]['name']]
                        },
                        series: [
                            {
                                name: '数据详情',
                                type: 'pie',
                                radius: ['50%', '70%'],
                                avoidLabelOverlap: false,
                                label: {
                                    normal: {
                                        show: false,
                                        position: 'center'
                                    },
                                    emphasis: {
                                        show: true,
                                        textStyle: {
                                            fontSize: '14',
                                            fontWeight: 'bold'
                                        }
                                    }
                                },
                                labelLine: {
                                    normal: {
                                        show: false
                                    }
                                },
                                data: data
                            }
                        ]
                    });
                }
            }
        });

        // ************************************************************************************************

        //　初始化实例 3
        var myChart3 = echarts.init(document.getElementById('echarts-pillar'));

        // 渲染前端页面
        $.ajax({
            type: 'get',
            url: '/public/warn_type/',
            data: {},
            success: function (result) {
                if (result['code'] === 200) {
                    var data = result['data']['sum_data'];
                    myChart3.setOption({
                        title: {
                            text: '预警分类统计',
                            x: 'center'
                        },
                        tooltip: {
                            trigger: 'item',
                            formatter: "{a} <br/>{b} : {c} ({d}%)"
                        },
                        legend: {
                            orient: 'vertical',
                            left: 'left',
                            data: ['智能预警', '手动预警']
                        },
                        grid: {
                            left: '6%',
                            right: '1%',
                            bottom: '5%',
                            containLabel: true
                        },
                        series: [
                            {
                                name: '访问来源',
                                type: 'pie',
                                radius: '55%',
                                center: ['50%', '60%'],
                                data: data,
                                itemStyle: {
                                    emphasis: {
                                        shadowBlur: 10,
                                        shadowOffsetX: 0,
                                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                                    }
                                }
                            }
                        ],
                        color: ['#0098D9', '#E6B600']
                    });
                }
            }
        });

        // ************************************************************************************************

         element.on('tab(line-echarts)', function (data) {
            var index = data.index;
            echarts.dispose(document.getElementById("echarts-line" + index)); // 再次加载时 刷新dom
            var myChart4 = echarts.init(document.getElementById('echarts-line' + index), 'demo');
            $.ajax({
                type: 'get',
                url: '/public/line_data/',
                data: {
                    'index': index
                },
                success: function (result) {
                    if (result['code'] === 200) {
                        var data = result['data'];
                        myChart4.setOption(
                            {
                                legend: {},
                                tooltip: {},
                                dataset: {
                                    // 这里指定了维度名的顺序，从而可以利用默认的维度到坐标轴的映射。
                                    // 如果不指定 dimensions，也可以通过指定 series.encode 完成映射，参见后文。
                                    dimensions: ['product', '已完成', '已丢弃'],
                                    source: data
                                },
                                xAxis: {
                                    type: 'category',
                                    name: ''
                                },
                                yAxis: {
                                    name: ''
                                },
                                grid: {
                                    left: '2%',
                                    right: '2%',
                                    bottom: '5%',
                                    containLabel: true
                                },
                                series: [{
                                    type: 'bar'
                                },
                                    {
                                        type: 'bar'
                                    }
                                ],
                                color: ['#E6B600', '#39CF78']
                            }
                        )
                    }
                }
            });
        });

        // ************************************************************************************************

        //　柱状图　初始化实例
        element.on('tab(column-echarts)', function (data) {
            var index = data.index;
            echarts.dispose(document.getElementById("echarts-column" + index)); // 再次加载时 刷新dom
            var myChart5 = echarts.init(document.getElementById('echarts-column' + index), 'demo');
            $.ajax({
                type: 'get',
                url: '/public/column_data/',
                data: {
                    'index': index
                },
                success: function (result) {
                    if (result['code'] === 200) {
                        var data = result['data'];
                        myChart5.setOption(
                            {
                                legend: {},
                                tooltip: {},
                                dataset: {
                                    // 这里指定了维度名的顺序，从而可以利用默认的维度到坐标轴的映射。
                                    // 如果不指定 dimensions，也可以通过指定 series.encode 完成映射，参见后文。
                                    dimensions: ['product', '抛物预警', '泼水预警'],
                                    source: data
                                },
                                xAxis: {
                                    type: 'category',
                                    name: ''
                                },
                                yAxis: {
                                    name: ''
                                },
                                grid: {
                                    left: '2%',
                                    right: '2%',
                                    bottom: '5%',
                                    containLabel: true
                                },
                                series: [{
                                    type: 'bar'
                                },
                                    {
                                        type: 'bar'
                                    }
                                ],
                                color: ['#0098D9', '#C12E34']
                            }
                        )
                    }
                }
            });
        });
        // ************************************************************************************************
    });
};

// ************************************************************************************************
// 首页刷新　柱状图自动加载数据
$(function () {
    echarts.dispose(document.getElementById("echarts-line0")); // 再次加载时 刷新dom
    var myChart4 = echarts.init(document.getElementById('echarts-line0'), 'demo');
    $.ajax({
        type: 'get',
        url: '/public/line_data/',
        data: {
            'index': 0
        },
        success: function (result) {
            if (result['code'] === 200) {
                var data = result['data'];
                myChart4.setOption(
                    {
                        legend: {},
                        tooltip: {},
                        dataset: {
                            // 这里指定了维度名的顺序，从而可以利用默认的维度到坐标轴的映射。
                            // 如果不指定 dimensions，也可以通过指定 series.encode 完成映射，参见后文。
                            dimensions: ['product', '已完成', '已丢弃'],
                            source: data
                        },
                        xAxis: {
                            type: 'category',
                            name: ''
                        },
                        yAxis: {
                            name: ''
                        },
                        grid: {
                            left: '2%',
                            right: '2%',
                            bottom: '2%',
                            containLabel: true
                        },
                        series: [{
                            type: 'bar'
                        },
                            {
                                type: 'bar'
                            }
                        ],
                        color: ['#E6B600', '#39CF78']
                    }
                )
            }
        }
    });
});


$(function () {
    var echarts = new Echarts();
    echarts.run();
});


// ************************************************************************************************
// 首页刷新　柱状图自动加载数据
$(function () {
    echarts.dispose(document.getElementById("echarts-column0")); // 再次加载时 刷新dom
    var myChart5 = echarts.init(document.getElementById('echarts-column0'), 'demo');
    $.ajax({
        type: 'get',
        url: '/public/column_data/',
        data: {
            'index': 0
        },
        success: function (result) {
            if (result['code'] === 200) {
                var data = result['data'];
                myChart5.setOption(
                    {
                        legend: {},
                        tooltip: {},
                        dataset: {
                            // 这里指定了维度名的顺序，从而可以利用默认的维度到坐标轴的映射。
                            // 如果不指定 dimensions，也可以通过指定 series.encode 完成映射，参见后文。
                            dimensions: ['product', '抛物预警', '泼水预警'],
                            source: data
                        },
                        xAxis: {
                            type: 'category',
                            name: ''
                        },
                        yAxis: {
                            name: ''
                        },
                        grid: {
                            left: '2%',
                            right: '2%',
                            bottom: '2%',
                            containLabel: true
                        },
                        series: [{
                            type: 'bar'
                        },
                            {
                                type: 'bar'
                            }
                        ],
                        color: ['#0098D9', '#C12E34']
                    }
                )
            }
        }
    });
});


$(function () {
    var echarts = new Echarts();
    echarts.run();
});
