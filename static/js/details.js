//var x_data1 = ['2019-1', '2019-2', '2019-3', '2019-4', '2019-5', '2019-6', '2019-7', '2019-8', '2019-9', '2019-10', '2019-11', '2019-12'];
var x_data2 = ['2020-1', '2020-2', '2020-3', '2020-4', '2020-5', '2020-6', '2020-7', '2020-8', '2020-9', '2020-10', '2020-11', '2020-12'];
// var y_data1 = [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3];
var y_data2 = [3.9, 5.9, 11.1, 18.7, 48.3, 69.2, 231.6, 46.6, 55.4, 18.4, 10.3, 0.7];

// 图表设置
option = {
    title: {
        text: '数据折线图',
        // subtext:'在此测试',
        x: 'center',
        y: 'top',
        textAlign:'center'

    },
    tooltip : {
        trigger: 'axis',
        // axisPointer: {
        //     type: 'cross'
        // }
    },
    legend: {
        data:['最高'] //, '最低']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {readOnly:false},
            magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    dataZoom : {
        show : true,
        realtime : true,
        start : 40,
        end : 60
    },
    xAxis : [
        /*
        {
            type : 'category',
            axisTick: {
                alignWithLabel: true
            },
            axisLine: {
                // X 轴或者 Y 轴的轴线是否在另一个轴的 0 刻度上，只有在另一个轴为数值轴且包含 0 刻度时有效。
                onZero: false,
                lineStyle: {
                    color: "black"
                }
            },
            boundaryGap : true,
            data: x_data1
        },   */
        {
            type : 'category',
            axisTick: {
                alignWithLabel: true
            },
            axisLine: {
                onZero: false,
                lineStyle: {
                    color: "black"
                }
            },
            boundaryGap : true,
            data: x_data2
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        /*
        {
            name:'数据段1',
            type:'line',
            data:y_data1
        },   */
        {
            name:'数据段2',
            type:'line',
            data:y_data2
        }
    ]
};

var url_page = "http://106.14.148.241:9999";

//异步加载数据
var vm = new Vue({
    el: '#app',
    data () {
        return {
            ProjectList: [],
            SectionList:[],
            DeviceList:[],
            ProjectAttr: {},
            SectionAttr: {},
            DeviceAttr: {},
            List:[],
            projectSelected:'',
            deviceSelected:'',
            sectionSelected:''
        }
    },

    mounted () {
        axios
            .get(`${url_page}/data_display/get_details_info`)
            .then(response => {
                console.log(response);
                this.ProjectList = response.data.ProjectList;
                this.SectionList = response.data.SectionList;
                this.DeviceList = response.data.DeviceList;
                this.ProjectAttr = response.data.ProjectAttr;
                this.SectionAttr = response.data.SectionAttr;
                this.DeviceAttr = response.data.DeviceAttr;
                this.List = response.data.List;
                // 默认选中
                this.projectSelected = this.ProjectAttr.id;
                this.sectionSelected = this.SectionAttr.id;
                this.deviceSelected = this.DeviceAttr.id;
            })
            .catch(function (error) { // 请求失败处理
                console.log(error);
            });

        var myChart = echarts.init(document.getElementById("c1"));
        myChart.setOption(option);

        // 当浏览器窗口缩小时，图表自适应div
        window.addEventListener('resize',function() {myChart.resize()});

    },

    methods:{
        async projectSubmit (){
            // project按钮
            console.log(this.projectSelected);
            const{data:res} = await axios.get(`${url_page}/data_display/get_details_info?projectid=${this.projectSelected}`);
            console.log(res);
            // 更新数据
            this.ProjectAttr = res.ProjectAttr;
            this.SectionAttr = res.SectionAttr;
            this.DeviceAttr = res.DeviceAttr;
            this.ProjectList = res.ProjectList;
            this.SectionList = res.SectionList;
            this.DeviceList = res.DeviceList;
            this.List = res.List;
            // 默认选中
            this.projectSelected = this.ProjectAttr.id;
            this.sectionSelected = this.SectionAttr.id;
            this.deviceSelected = this.DeviceAttr.id;
        },
        async sectionSubmit (){
            // section按钮
            console.log(this.projectSelected);
            const{data:res} = await axios.get(`${url_page}/data_display/get_details_info?sectionid=${this.sectionSelected}`);
            console.log(res);
            // 更新数据
            this.SectionAttr = res.SectionAttr;
            this.DeviceAttr = res.DeviceAttr;
            this.SectionList = res.SectionList;
            this.DeviceList = res.DeviceList;
            this.List = res.List;
            // 默认选中
            this.projectSelected = this.ProjectAttr.id;
            this.sectionSelected = this.SectionAttr.id;
            this.deviceSelected = this.DeviceAttr.id;
        },
        async deviceSubmit (){
            // device按钮
            console.log(this.deviceSelected);
            const{data:res} = await axios.get(`${url_page}/data_display/get_details_info?deviceid=${this.deviceSelected}`);
            console.log(res);
            // 更新数据
            this.DeviceAttr = res.DeviceAttr;
            this.DeviceList = res.DeviceList;
            this.List = res.List;
            // 默认选中
            this.projectSelected = this.ProjectAttr.id;
            this.sectionSelected = this.SectionAttr.id;
            this.deviceSelected = this.DeviceAttr.id;
        },
    }
})
