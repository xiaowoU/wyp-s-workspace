// todo: 数据，js的中文字符串编码不一致
let data_all = ['315线', '嗯1814线', '大门隧道', '成都'];
// 逻辑： 1 展示区域的显示或隐藏
let input = document.getElementById('search-val');
let show = document.getElementById('show');

input.onclick = function(){
    // show.style.display = 'block';
    show.style.visibility = 'visible';

    let str = '';
    data_all.forEach((item)=>
    {
        str += '<p>'+item+'</p>';
    })
    console.log(str);
    // show items
    show.innerHTML = str;
    
}

// input.onkeyup = function(){
input.oninput = function(){
    // show.style.display = 'block';
    show.style.visibility = 'visible';
    let str = '';
    data_all.forEach((item)=>
    {
        console.log(item);
        console.log("input: "+typeof(input.value)+input.value);
        // input.value 和 data的每一项进行匹配，indexOf() 匹配不到-1
        let res = item.indexOf(input.value);
        // let res = item.search(input.value);
        if(res != -1){
            // 读取连接
            str += '<p>'+item+'</p>';
        }
        console.log(item);
    })
    console.log(str);
    // 如果input.value为空或者 str为false 给用户一个提示
    if(!input.value || !str)
    {
        show.innerHTML = '<p>暂无结果</p>'
    }else{
        show.innerHTML = str;
    }
    
}

input.onmouseleave = function(){
    show.style.visibility = 'hidden';
    // input.value = '';
}






					
