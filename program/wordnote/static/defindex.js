// var SCREENWIDTH = window.screen.width
// var SCREENHEIGHT = window.screen.height

var alpha = []
alpha.push("n", "o", "t", "e"); // class name of image
var alphaindex = 0
var left = 20 // left坐标
var dom;
var leftTimer;
const OPACITYANIMINVAL = 10; // 透明度动画时间间隔
const ADDLEFTINTVAL = 100; // 移动动画时间间隔

function addLeft(){ // 移动动画
    dom = document.getElementsByClassName(alpha[alphaindex])[0]
    dom.style.marginLeft = left + "%"
    if (alphaindex == 4){
        clearTimeout(timer)
    }
    left = left + 13
    alphaindex = alphaindex + 1
    // opcTimer = setTimeout("opacityAnim()",10)
    opcTimer = setInterval("opacityAnim()", OPACITYANIMINVAL)
    leftTimer = setTimeout("addLeft()", ADDLEFTINTVAL)
}

addLeft()

var opc = 0
var opcTimer;
function opacityAnim(){ // 透明度动画
    if (opc > 100){
        opc = 100
        clearTimeout(opcTimer)
    }
    for (var i = 0; i <= alphaindex; i++){
        document.getElementsByClassName(alpha[i])[0].style.opacity = opc + "%"
    }
    opc = opc + 10
    // opcTimer = setTimeout("opacityAnim()",10)
}


// var uptimer;
var index = 0
// var alphatops = 0
var alphatoper = []
alphatoper.push(0,0,0,0) // 高度
var basetime = 40
function upAnim(){
    // while (index <= 3){
    //     var dom = document.getElementsByClassName(alpha[index])[0]
    //     dom.style.top = alphatops + "px"
    //     index = index + 1
    // }
    // alphatops = alphatops - 2
    // basetime = basetime - 2
    // // alert(basetime)
    // index = 0

    // if (alphatops > -200){
    //     setTimeout("upAnim()",basetime)
    // }

    // var dom = document.getElementsByClassName(alpha[index])[0]
    // dom.style.top = alphatops + "px"
    // alphatops = alphatops - 2
    // basetime = basetime - 2
    // if (alphatops > -200){
    //     setTimeout("upAnim()",basetime)
    // }else{
    //     index = index + 1
    //     alphatops = 0
    //     if (index <= 3){
    //         setTimeout("upAnim()",basetime)
    //     }
    // }

    for (var i = 0; i <= index; i++){
        var dom = document.getElementsByClassName(alpha[i])[0]
        dom.style.top = alphatoper[i] + "px"
        alphatoper[i] = alphatoper[i] - 2
    }

    if (index < 3){ // 下一个与上一个相差大于50时index + 1
        if ((alphatoper[index + 1] - alphatoper[index]) > 50){
            index = index + 1
        }
    }

    basetime = basetime - 2
    if (alphatoper[3] > -400){
        setTimeout("upAnim()",basetime)
    }else{
        setTimeout("changePage()",20) // ->切换页面
    }
}

// function endAnim(){
//     // uptimer = window.setInterval(function(){
//     // }, 100)
//     // uptimer = window.setInterval("upAnim()", 100)
// }

var backcolor = 39

// 背景渐变过渡
function changePage(){
    backcolor = backcolor + 10
    if (backcolor < 230){
        document.body.style.backgroundColor = "RGB(" + backcolor + "," + backcolor + ","+ backcolor +")"
        setTimeout("changePage()",30)
    }else{
        window.location.href="index" // 更改url
    }
}

setTimeout("upAnim()", 4 * ADDLEFTINTVAL + 100)

