// var allBtn = $('#all-view');
// allBtn.click(function () {
//     if (document.documentElement.RequestFullScreen) {
//         document.documentElement.RequestFullScreen();
//     }
//     //兼容火狐
//     if (document.documentElement.mozRequestFullScreen) {
//         document.documentElement.mozRequestFullScreen();
//     }
//     //兼容谷歌等可以webkitRequestFullScreen也可以webkitRequestFullscreen
//     if (document.documentElement.webkitRequestFullScreen) {
//         document.documentElement.webkitRequestFullScreen();
//     }
//     //兼容IE,只能写msRequestFullscreen
//     if (document.documentElement.msRequestFullscreen) {
//         document.documentElement.msRequestFullscreen();
//     }
// });
//
// var escBtn = $('#esc-view');
// escBtn.click(function () {
//     if (document.exitFullScreen) {
//         document.exitFullscreen()
//     }
//     //兼容火狐
//     if (document.mozCancelFullScreen) {
//         document.mozCancelFullScreen()
//     }
//     //兼容谷歌等
//     if (document.webkitExitFullscreen) {
//         document.webkitExitFullscreen()
//     }
//     //兼容IE
//     if (document.msExitFullscreen) {
//         document.msExitFullscreen()
//     }
// });

// *****************************************************************

// 来源统计

$(function () {
    var myChart = echarts.init(document.getElementById('echarts-bang'));
    $.ajax({
        type: 'get',
        url: '/public/warn_type/',
        data: {},
        success: function (result) {
            if (result['code'] === 200) {
                var data = result['data']['sum_data'];
                var count = result['data']['count'];
                var name = result['data']['name'];
                var html = template('sum-data1', {'count': count});
                document.getElementById('sum-1').innerHTML = html;
                var html = template('sum-data2', {'name': name});
                document.getElementById('sum-2').innerHTML = html;
                myChart.setOption({
                    title: {},
                    tooltip: {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'right',
                        top: '8%',
                        data: [{
                            name: '智能预警',
                            textStyle: {
                                color: '#AAAEAA'
                            }
                        },
                            {
                                name: '手动预警',
                                textStyle: {
                                    color: '#AAAEAA'
                                }
                            }],

                        color: ['#CED642', '#39CF78']
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
                            radius: '80%',
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
                    color: ['#53B7A3', '#214398']
                });
            }
        }
    });
});


// 高发监控区
// *****************************************************************

    $(function () {
        var myChart = echarts.init(document.getElementById('echarts-column'));

        $.ajax({
            type: 'get',
            url: '/public/top_three/',
            data: {},
            success: function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    myChart.setOption({
                        tooltip: {
                            trigger: 'item',
                            formatter: "{a} <br/>{b}: {c} ({d}%)"
                        },
                        legend: {
                            orient: 'vertical',
                            x: 'left',
                            textStyle: {
                                color: '#AAAEAA'  // 图例文字颜色
                            },

                            data: [data[0]['name'], data[1]['name'], data[2]['name']]
                        },
                        series: [
                            {
                                name: '数据详情',
                                type: 'pie',
                                radius: ['50%', '60%'],
                                center: ['65%', '50%'],
                                avoidLabelOverlap: false,
                                label: {
                                    color: 'red',
                                    normal: {
                                        show: false,
                                        position: 'center'
                                    },
                                    emphasis: {
                                        show: true,
                                        textStyle: {
                                            fontSize: '12',
                                            color: 'white'
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
                        ],
                        color: ['#214398', '#53B7A3', '#63869E']
                    });
                }
            }
        });
    });

// *****************************************************************


// 高发事件
// *****************************************************************

    $(function () {
        var myChart = echarts.init(document.getElementById('echarts-cake'));
        $.ajax({
            type: 'get',
            url: '/public/cake_data/',
            data: {},
            success: function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var data_Spilling = data['Spilling'];
                    var data_water = data['water'];
                    myChart.setOption({
                        angleAxis: {
                            type: 'category',
                            data: ['清晨', '上午', '下午', '傍晚', '夜晚'],
                            z: 10,
                            axisLine: {
                                lineStyle: {
                                    color: '#AAAEAA',
                                },
                            },
                            axisTick: {
                                lineStyle: {
                                    color: '#53B7A3',
                                }
                            },
                        },
                        radiusAxis: {
                            axisLabel: {
                                color: '#AAAEAA',
                            }
                        },
                        polar: {
                            center: ['60%', '50%'],
                            radius: '56%',
                            tooltip: {
                                textStyle: {
                                    color: 'green',
                                },
                            }
                        },
                        series: [
                            {
                                type: 'bar',
                                data: data_Spilling,
                                coordinateSystem: 'polar',
                                name: '抛物预警',
                                stack: 'a',
                                itemStyle: {
                                    color: '#214398',
                                },
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
                            color: 'white',
                            data: ['抛物预警', '泼水预警'],
                            textStyle: {
                                color: '#AAAEAA',  // 图例文字颜色
                                fontSize: '12',
                            }
                        },
                        color: ['#53B7A3', '#214398']
                    });
                }
            }
        });
    });
// *****************************************************************


// 本周操作统计

// *****************************************************************

    $(function () {
        var myChart = echarts.init(document.getElementById('cols'));
        $.ajax({
            type: 'get',
            url: '/public/line_data/',
            data: {
                'index': 1
            },
            success: function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    myChart.setOption(
                        {
                            legend: {
                                textStyle: {
                                    color: '#AAAEAA',  // 图例文字颜色
                                    fontSize: '10',
                                }
                            },
                            tooltip: {},
                            dataset: {
                                // 这里指定了维度名的顺序，从而可以利用默认的维度到坐标轴的映射。
                                // 如果不指定 dimensions，也可以通过指定 series.encode 完成映射，参见后文。
                                dimensions: ['product', '已完成', '已丢弃'],
                                source: data
                            },
                            xAxis: {
                                type: 'category',
                                axisLine: {
                                    lineStyle: {
                                        color: '#AAAEAA',
                                    }
                                }
                            },
                            yAxis: {
                                axisLine: {
                                    lineStyle: {
                                        color: '#AAAEAA',
                                    }
                                }
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
                            color: ['#214398', '#53B7A3']
                        }
                    )
                }
            }
        });
    });

// *****************************************************************

// 地图

// *****************************************************************

var styleJson = [{
    "featureType": "land",
    "elementType": "geometry",
    "stylers": {
        "visibility": "on",
        "color": "#242f3eff"
    }
}, {
    "featureType": "water",
    "elementType": "geometry",
    "stylers": {
        "visibility": "on",
        "color": "#17263cff",
    }
}, {
    "featureType": "green",
    "elementType": "geometry",
    "stylers": {
        "visibility": "on",
        "color": "#263b3eff"
    }
}, {
    "featureType": "building",
    "elementType": "geometry",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "building",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#2a3341ff"
    }
}, {
    "featureType": "building",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#1a212eff"
    }
}, {
    "featureType": "subwaystation",
    "elementType": "geometry",
    "stylers": {
        "visibility": "off",
        "color": "#b15454B2"
    }
}, {
    "featureType": "education",
    "elementType": "geometry",
    "stylers": {
        "visibility": "off",
        "color": "#e4f1f1ff"
    }
}, {
    "featureType": "medical",
    "elementType": "geometry",
    "stylers": {
        "visibility": "off",
        "color": "#f0dedeff"
    }
}, {
    "featureType": "scenicspots",
    "elementType": "geometry",
    "stylers": {
        "visibility": "off",
        "color": "#4c61ffff"
    }
}, {
    "featureType": "highway",
    "elementType": "geometry",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "highway",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#9e7d60ff"
    }
}, {
    "featureType": "highway",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#554631ff"
    }
}, {
    "featureType": "highway",
    "elementType": "labels",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "highway",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#759879ff"
    }
}, {
    "featureType": "highway",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#1a2e1cff"
    }
}, {
    "featureType": "highway",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "arterial",
    "elementType": "geometry",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "arterial",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#9e7d60ff"
    }
}, {
    "featureType": "arterial",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#554631fa"
    }
}, {
    "featureType": "arterial",
    "elementType": "labels",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "arterial",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#759879ff"
    }
}, {
    "featureType": "arterial",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#1a2e1cff"
    }
}, {
    "featureType": "local",
    "elementType": "geometry",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "local",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#38414eff"
    }
}, {
    "featureType": "local",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "local",
    "elementType": "labels",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "local",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#979c9aff"
    }
}, {
    "featureType": "local",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffffff"
    }
}, {
    "featureType": "railway",
    "elementType": "geometry",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "railway",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#123c52ff"
    }
}, {
    "featureType": "railway",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#12223dff"
    }
}, {
    "featureType": "subway",
    "elementType": "geometry",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "subway",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#d8d8d8ff"
    }
}, {
    "featureType": "subway",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#ffffff00"
    }
}, {
    "featureType": "subway",
    "elementType": "labels",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "subway",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#979c9aff"
    }
}, {
    "featureType": "subway",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffffff"
    }
}, {
    "featureType": "continent",
    "elementType": "labels",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "continent",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "continent",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#0e4dffff"
    }
}, {
    "featureType": "continent",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffcb7cff"
    }
}, {
    "featureType": "city",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "city",
    "elementType": "labels",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "city",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#d69563ff",
        "weight": 50
    }
}, {
    "featureType": "city",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#17263cff",
        "weight": 3
    }
}, {
    "featureType": "town",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "town",
    "elementType": "labels",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "town",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#454d50ff"
    }
}, {
    "featureType": "town",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#ffffffff"
    }
}, {
    "featureType": "road",
    "elementType": "geometry.fill",
    "stylers": {
        "color": "#9e7d60ff"
    }
}, {
    "featureType": "poilabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "districtlabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "road",
    "elementType": "geometry",
    "stylers": {
        "visibility": "on"
    }
}, {
    "featureType": "road",
    "elementType": "labels",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "road",
    "elementType": "geometry.stroke",
    "stylers": {
        "color": "#554631ff"
    }
}, {
    "featureType": "district",
    "elementType": "labels",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "poilabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "poilabel",
    "elementType": "labels.text.fill",
    "stylers": {
        "color": "#d69563ff"
    }
}, {
    "featureType": "poilabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#17263cff",
        "weight": 3
    }
}, {
    "featureType": "manmade",
    "elementType": "geometry",
    "stylers": {
        "color": "#242f3eff",
        "visibility": "on"
    }
}, {
    "featureType": "districtlabel",
    "elementType": "labels.text.stroke",
    "stylers": {
        "color": "#17263cff"
    }
}, {
    "featureType": "entertainment",
    "elementType": "geometry",
    "stylers": {
        "color": "#ffffffff",
        "visibility": "off"
    }
}, {
    "featureType": "shopping",
    "elementType": "geometry",
    "stylers": {
        "color": "#12223dff",
        "visibility": "off"
    }
}, {
    "featureType": "estate",
    "elementType": "geometry",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "highwaysign",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "nationalwaysign",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "provincialwaysign",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "tertiarywaysign",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "subwaylabel",
    "elementType": "labels.icon",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "subwaylabel",
    "elementType": "labels",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "tertiarywaysign",
    "elementType": "labels",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "provincialwaysign",
    "elementType": "labels",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "nationalwaysign",
    "elementType": "labels",
    "stylers": {
        "visibility": "off"
    }
}, {
    "featureType": "highwaysign",
    "elementType": "labels",
    "stylers": {
        "visibility": "off"
    }
}];

    $(function () {
        $.ajax({
            type: 'get',
            url: '/public/bdmap/',
            data: {},
            success: function (result) {
                if (result['code'] === 200) {

                    var data = result['data'];
                    // 百度地图API功能
                    var map = new BMap.Map("map"); // 创建Map实例
                    //添加地图类型控件
                    map.centerAndZoom(new BMap.Point(120.639921, 31.322263), 16); //  初始化地图,设置中心点坐标和地图级别
                    map.enableScrollWheelZoom(true); // 设置鼠标滚轮缩放
                    map.setMapStyle({styleJson:styleJson});

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
                    }
                } else {
                    alert('获取失败...');
                }
            }
        });
    });

// *****************************************************************

// 地图主题json
