// Warning
if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    alert("Giao diện không phù hợp cho thiết bị di động, vui lòng truy cập vào bằng thiết bị màn hình lớn!");
} else {
    //Now include js files
}

// Time
function showTime(){
    var date = new Date();
    var h = date.getHours(); // 0 - 23
    var m = date.getMinutes(); // 0 - 59
    var s = date.getSeconds();
    var session = "AM";
    
    if(h == 0){
        h = 12;
    }
    if(h > 12){
        h = h - 12;
        session = "PM";
    }
    
    h = (h < 10) ? "0" + h : h;
    m = (m < 10) ? "0" + m : m;
    s = (s < 10) ? "0" + s : s;
    
    var time = h + ":" + m + ":" + s + " " + session;
    document.getElementById("MyClockDisplay").innerText = time;
    setTimeout(showTime, 1000);
}
showTime();

// Delay

// IP Address

// Main Frame Navigation Buttons
document.getElementById("HomeButton").onclick = function HomeButtonClicked(){
    document.getElementById("ScreenFrame").src = "/Main";
}

document.getElementById("ControllerButton").onclick = function ControllerButtonClicked(){
    document.getElementById("ScreenFrame").src = "/Controller";
}

document.getElementById("SettingsButton").onclick = function SettingsButtonClicked(){
    document.getElementById("ScreenFrame").src = "/Settings";
}

document.getElementById("InforButton").onclick = function InforButtonClicked(){
    document.getElementById("ScreenFrame").src = "/Information";
}