
// todo: 加载页面时，加载出项目数据
$(document).ready(function(){
    geoCode();
});

$(document).ready(function(){
    $("#search-btn").click(function(){
        // 获取值了就不能提示了
        var val=document.getElementById("search-val").value;

        // citys.forEach((item)=>{
        //   if (item.name == val){
        //     var setlnglat = item.lnglat;
        //     // window.alert(setlnglat);
        //     map.setCenter(setlnglat);
        //     map.setZoom(8);
        //     break;
        //   }
        // });
        var info = `${val}No match!!!!`
        window.alert(info);

    });
});
