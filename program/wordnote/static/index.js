// 查找操作
function findWord(){
    $.ajax({
        url: "findWord",
        type: "POST",
        dataType: "json",
        data : {word: $(".word").val(), // 从输入文本框中取值
                tip:$(".tip").val(),
                usage:$(".usage").val(),
            },
        success: function (data) { // 查找结果
            if (data.word == ""){
                $(".states").html("word '" + $(".word").val() + "' is not exists")
            }
            else{ // 更新输入框数据
                $(".word").val(data.word)
                $(".tip").val(data.tip)
                $(".usage").val(data.usage)
                $(".states").html("word '" + $(".word").val() + "' is find") //更新状态
            }
        }
    })
}

// 更新操作
function changeUsage(){
    // include usage and tip
    // 根据单词更新tip和usage

    $.ajax({
        url: "changeUsage",
        type: "POST",
        dataType: "json",
        data : {word: $(".word").val(), // 从输入文本框中取值
                tip:$(".tip").val(),
                usage:$(".usage").val(),
            },
        success: function (data) { //更新状态
            $(".states").html("change word'" + $(".word").val() + "' successfully")
        }
    })
}

// 删除操作
function deleteWord(){
    $.ajax({
        url: "deleteWord",
        type: "POST",
        dataType: "json",
        data : {word: $(".word").val()},
        success: function (data) { //更新状态
            $(".states").html("delete word'" + $(".word").val() + "' successfully")
        }
    })
}

// 撤销操作
function breakChange(){
    $.ajax({
        url: "breakChange",
        type: "POST",
        dataType: "json",
        data : {},
        success: function (data) { //更新状态
            $(".states").html("break " + data.op + ": " + data.word)
        }
    })
}

var textindex = 0 // 文本框焦点index
var texttag = new Array(".word", ".tip", ".usage")
$(".word").click(function(event){
    textindex = 0
})
$(".tip").click(function(event){
    textindex = 1
})
$(".usage").click(function(event){
    textindex = 2
})

var hostkeys = {102:".changeUsage", 119:".findWord", 112:".deleteWord", 117:".breakChange"}
var hostkeys_focus = {49:".word", 50:".tip", 51:".usage"}
// 快捷键
var buttons = false;
$(window).keypress(function (event) {
    // change inputbox focus
    if (event.keyCode == 91){
        event.preventDefault()
        textindex = textindex - 1
        if (textindex < 0){textindex = 2}
        $(texttag[textindex]).focus()
    }
    else if (event.keyCode == 93){
        event.preventDefault()
        textindex = textindex + 1
        if (textindex > 2){textindex = 0}
        $(texttag[textindex]).focus()
    }

    // combine key
    if (event.keyCode == 92){ // prekey
        event.preventDefault()
        buttons = true
        return
    }
    if (buttons){
        event.preventDefault()
        // 快捷键
        for (var key in hostkeys){
            if (event.keyCode == key){
                buttons = false
                $(hostkeys[key]).click()
                return
            }
        }

        // 文本框焦点
        for (var key in hostkeys_focus){
            if (event.keyCode == key){
                buttons = false
                $(hostkeys_focus[key]).focus()
                return
            }
        }

    }
    
})
