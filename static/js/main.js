// 预留：后续可以添加图表联动、鼠标悬停详情等
console.log("栋梁之观可视化平台已加载");
// 如果 pyecharts 生成的图表未自动适配容器大小，可以手动监听resize
window.addEventListener('resize', () => {
    // 可选：触发所有echarts实例重绘（pyecharts生成的已自动处理，此处留空）
});