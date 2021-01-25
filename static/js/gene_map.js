// 变量
var url="/data_display/get_project_info/"

//构建自定义信息窗体
function createInfoWindow(title, content) {
    var info = document.createElement("div");
    info.className = "c";

    //可以通过下面的方式修改自定义窗体的宽高
    info.style.width = "280px";
    info.style.background = "#bfcbd9";
    // 定义标题
    var titleD = document.createElement("div");
    titleD.innerHTML = title;

    info.appendChild(titleD);

    // 定义内容
    var middle = document.createElement("div");
    middle.innerHTML = content;
    info.appendChild(middle);

    return info;
}

//关闭信息窗体
function closeInfoWindow() {
    map.clearInfoWindow();
}

// mousemove
function moveEvent(item){
    //实例化信息窗体
    var title = `<strong style="font-size:16px;color:black;">${item.name}</strong>`;

    var content = '<div style="font-size:16px;color:black;"><table>' +
        '<tr><td width="30%">名称: ' + '</td><td width="70%">' + item.name + '</td></tr>' +
        '<tr><td>位置: ' + '</td><td>' + item.position + '</td></tr>' +
        '<tr><td>地址: ' + '</td><td>' + item.adress_detail + '</td></tr>' +
        '<tr><td>数据详情: ' + '</td><td><a href="../details_page">查看</a></td></tr>' +
        // 无法直接到达指定id处
        // '<tr><td>数据详情: ' + '</td><td><a onclick="location.href=(`../details_page?projectid=${id}`);">查看</a></td></tr>' +
        '</table></div>';

    var infoWindow = new AMap.InfoWindow({
        isCustom: true,  //使用自定义窗体
        // content: createInfoWindow(title, content.join("<br/>")),
        content: createInfoWindow(title, content),
        offset: new AMap.Pixel(16, -45)
        // offset: new AMap.Pixel(130, 100)
    });
    // 打开窗口
    infoWindow.open(map, item.lnglat);
    // 8s后自动关闭
    setTimeout(closeInfoWindow, 8000);
}

// mouseclick
function clickEvent(lnglat){
    // console.log("click");
    map.setCenter(lnglat);
    map.setZoom(8);

}


// amap实例
var map = new AMap.Map('map-chart',{
    // mapStyle: "amap://styles/dark",
    zoom : 5,
    center : [103.83178711, 36.12012759],
    // center: [111.43471, 30.5307],
    roam: true,
    // viewMode: '3D'
});
map.addControl(new AMap.Scale());
map.addControl(new AMap.ToolBar());

var vm = new Vue({
    el:'.box',
    data: {
        ProjectGeoList: [],
        valueSelected: '',
    },
    mounted() {
        axios
            .get(url)
            .then(response => {
                // console.log(response);
                var res = response.data;
                this.ProjectGeoList = res;
                res.forEach(item=>{
                    // console.log(item.lnglat);
                    var marker = new AMap.Marker({
                        position: item.lnglat,
                        offset: new AMap.Pixel(-10, -10),
                        title: item.adress_detail
                    });
                    map.add(marker);
                    // 添加事件
                    AMap.event.addListener(marker, 'mousemove', function(){
                        moveEvent(item);
                    });
                    AMap.event.addListener(marker, 'click', function(){
                        clickEvent(marker.getPosition());
                    });
                });

            })
            .catch(function (error) { // 请求失败处理
                console.log(error);
            });
    },
    methods:{
        async valueSubmit (){
            // 定位到此处
            // console.log(this.valueSelected);
            clickEvent(this.valueSelected);
        },
    }
})

