

var citys = [{"lnglat":[116.258446,37.686622],"name":"景县","style":2},
    {"lnglat":[113.559954,22.124049],"name":"圣方济各堂区","style":2},
    {"lnglat":[116.366794,39.915309],"name":"西城区","style":2}]


// 窗体自定义
var infoWin;
var tableDom;
function openInfoWin(map, event, content) {
    if (!infoWin) {
        infoWin = new AMap.InfoWindow({
            autoMove:false,
            isCustom: true,  //使用自定义窗体
            offset: new AMap.Pixel(130, 100)
        });
    }

    var x = event.offsetX;
    var y = event.offsetY;
    var lngLat = map.containerToLngLat(new AMap.Pixel(x, y));

    if (!tableDom) {
        let infoDom = document.createElement('div');
        infoDom.className = 'info';
        tableDom = document.createElement('table');
        infoDom.appendChild(tableDom);
        infoWin.setContent(infoDom);
    }

    var trStr = '';
    for (var name in content) {
        var val = content[name];
        trStr +=
            '<tr>' +
            '<td class="label">' + name + '</td>' +
            '<td>&nbsp;</td>' +
            '<td class="content">' + val + '</td>' +
            '</tr>'
    }
    // todo: 加一个图表链接
    trStr += '<a href="http://www.baidu.com" target="_blank">查看数据详情</a>'
    tableDom.innerHTML = trStr;
    infoWin.open(map, lngLat);
    // infoTitle: '<strong>这里是标题</strong>',
    //         infoBody: '<p class="my-desc"><strong>这里是内容。</strong> <br/> 高德地图 JavaScript API，是由 JavaScript 语言编写的应用程序接口，' +
    //             '它能够帮助您在网站或移动端中构建功能丰富、交互性强的地图应用程序</p>',
}

function closeInfoWin() {
    if (infoWin) {
        infoWin.close();
    }
}


// 单独amap
var map = new AMap.Map('map-chart',{
    mapStyle: "amap://styles/dark",
    zoom : 5,
    center : [103.83178711, 36.12012759],
    roam: true,
    viewMode: '3D'
});

var scale = new AMap.Scale({
    // 后续添加
});
var toolbar = new AMap.ToolBar({
    // 后续添加
});

// 散点图----------------------------------------
// var layer = new Loca.ScatterPointLayer({
var layer = new Loca.PointLayer({
    // map: map,
    eventSupport: true,
    // fitView: true
});

// 添加控件
map.addControl(scale);
map.addControl(toolbar);
map.add(layer);

// 鼠标事件----------------------------------------
layer.on('mousemove', function (ev) {
    console.log("mousemove");
    // window.alert(ev.rawData);
    // 事件类型
    var type = ev.type;
    // 当前元素的原始数据
    var rawData = ev.rawData;
    // 原始鼠标事件
    var originalEvent = ev.originalEvent;

    openInfoWin(map, originalEvent, {
        '名称': rawData.name,
        '位置': rawData.lnglat,
        '风格': rawData.style
    });

    setTimeout(closeInfoWin, 8000);
});

// layer.on('mouseleave', function (ev) {
//   closeInfoWin();
// });

layer.on('click', function(ev){
    console.log("click");
    var lnglat = ev.rawData.lnglat;
    map.setCenter(lnglat);
    map.setZoom(8);
});


// 传入原始数据
layer.setData(citys, {
    lnglat: 'lnglat'   // 指定坐标数据的来源，数据格式: 经度在前，维度在后，数组格式。
});

// 配置样式
layer.setOptions({
    style: {
        radius: 10, // 圆形半径，单位像素
        color: '#07E8E4', // 填充颜色
        borderColor: '#07E8E4', // 边框颜色
        borderWidth: 1.5, // 边框宽度
        opacity: 0.8
    },
    selectStyle: {
        radius: 14,
        color: '#FFF684'
    }
});

layer.render();

// 由地址查经纬度坐标
// var marker = new AMap.Marker();
function geoCode() {
    // 创建地理编码查询对象
    var geocoder = new AMap.Geocoder({
        // city: "010", //城市设为北京，默认：“全国”
    });
    // 获取项目信息
    url="/data_display/get_project_info/"
    $.getJSON(url, function(data) {
        // data：[{'adress_detail': '四川成都温江', '项目名字': '隧道1左洞', '位置': '315线', '管理单位': '暂无', '数据链接': '暂无'},]
        console.log(data);
        data.forEach(item=>{
            // 查询地理坐标
            let address = item.adress_detail;
            geocoder.getLocation(address, function(status, result) {
                // let out_info = `地址信息：${result.geocodes[0].location}`
                if (status === 'complete'&&result.geocodes.length) {
                    //location:  {Q: 30.572269, R: 104.06654100000003, lng: 104.066541, lat: 30.572269}
                    var lnglat = result.geocodes[0].location;
                    lng = lnglat.lng;
                    lat = lnglat.lat;
                    item["lnglat"] = [lng, lat];
                    console.log(`${address}--${lnglat}`);
                }else{
                    console.error('根据地址查询位置失败');
                }
            });
        });
        console.log(data);
    });
}





// var script=document.createElement("script");
// script.type="text/javascript";
// script.src="jquery.js";
// var url = 'http://192.168.13.14:9999/data_display/data_project/' ;
// $.getJSON(url, function(data) {
//   window.alert(data);
// }













// function get_c2_data() {
//     $.ajax({
//         url:"/c2",
//         success: function(data) {
// 			ec_center_option.series[0].data=data.data
//             ec_center.setOption(ec_center_option)
// 		},
// 		error: function(xhr, type, errorThrown) {
//
// 		}
//     })
// }
//
// get_c2_data()
//
// setInterval(get_c2_data,10000*10)


// echart geo amap
// var my_option = {
//   amap: {
//     // See https://lbs.amap.com/api/javascript-api/reference/map#MapOption for details
//     viewMode: "3D",
//     center: [103.83178711, 36.12012759],
//     zoom: 5,
//     resizeEnable: true,
//     // customized map style, see https://lbs.amap.com/dev/mapstyle/index for details
//     mapStyle: "amap://styles/dark",
//     renderOnMoving: true,
//     // the zIndex of echarts layer for AMap, default value is 2000.
//     echartsLayerZIndex: 2019
//   },
//   tooltip: {
//     trigger: "item"
//   },
//   // geo: {
//   //     show: true,
//   //     map: 'amap',
//   //     type: 'map',
//   //     roam: true,
//   // },
//   animation: false,
//   series: [
//     // {
//     //   name: "PM2.5",
//     //   // type: "scatter",
//     //   type: "effectScatter",
//     //   // use `amap` as the coordinate system
//     //   coordinateSystem: "amap",
//     //   // data items [[lng, lat, value], [lng, lat, value], ...]
//     //   data: convertData(data),
//     //   symbolSize: function (val) {
//     //     return val[2] / 10;
//     //   },
//     //   encode: {
//     //     value: 2
//     //   },
//     //   label: {
//     //     formatter: "{b}",
//     //     position: "right",
//     //     show: false
//     //   },
//     //   itemStyle: {
//     //     color: "#00c1de"
//     //   },
//     //   emphasis: {
//     //     label: {
//     //       show: true
//     //     }
//     //   }
//     // },
//   ]
// };
// var gaode_map = echarts.init(document.getElementById("map-chart"), "dark");
// gaode_map.setOption(my_option);


// // get amap instance
// var amap = gaode_map.getModel().getComponent("amap").getAMap();
// // operations below are the same as amap
// amap.addControl(new AMap.Scale());
// amap.addControl(new AMap.ToolBar());

// add layers
// var satelliteLayer = new AMap.TileLayer.Satellite();
// var roadNetLayer = new AMap.TileLayer.RoadNet();
// amap.add([satelliteLayer, roadNetLayer]);
// amap.addEventListener("click", function(){
//     alert("您点击了地图。");
// })
























