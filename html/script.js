var ROBOT_URL = "http://192.168.1.136:9000/?do=";

var isRecording = false;
var recordedSequence = [];
var moves = {
    "spinRight":  "R,F,100,2.3|L,B,100,2.3",
    "spinLeft":  "R,B,100,2.3|L,F,100,2.3",
    "turnRight":  "R,F,100,0.65|L,B,100,0.65",
    "turnLeft":  "R,B,100,0.65|L,F,100,0.65",
    "walkForward":  "L,F,100,0.5>R,F,100,0.5>L,F,100,0.5>R,F,100,0.5",
    "walkBack":  "L,B,100,0.5>R,B,100,0.5>L,B,100,0.5>R,B,100,0.5",
    "slideForward":  "L,F,100,1|R,F,100,1",
    "slideBack":  "L,B,100,1|R,B,100,1"
};

function toggleRecording(){
    isRecording = !isRecording;
    $(this).toggleClass("record-on");
}

function bigButtonClick(){
    console.log(this.id + " clicked!");
    if(isRecording){
        addCommandToSequence(this.id);
        addCommandIconToStage(this.id);
    } else {
        sendCommandSequence(moves[this.id]);
    }
}

function addCommandIconToStage(id){
    var icon = $(document.createElement('div')).addClass("icon " + id + "-icon");
    $("#stage").append(icon);
}

function addCommandToSequence(id){
    recordedSequence.push(moves[id]);
}

function playRecordedSequence(){
    sendCommandSequence(recordedSequence.join(">"));
}

function sendCommandSequence(seqStr){
    $.ajax({
        url: ROBOT_URL + seqStr
    });
}

function clearSequence(){
    recordedSequence = [];
    $("#stage").empty();
}

$(function(){
    // Big buttons click events
    $(".big-button").click(bigButtonClick);

    // Record button
    $("#record-button").click(toggleRecording);
    $("#record-button").dblclick(clearSequence);

    // Play button
    $("#play-button").click(playRecordedSequence);

    // Fullscreen
    $("body").click(function(){
        var el = document.documentElement
        var rfs =
            el.requestFullScreen
         || el.webkitRequestFullScreen
         || el.mozRequestFullScreen;
    rfs.call(el);
    });
});