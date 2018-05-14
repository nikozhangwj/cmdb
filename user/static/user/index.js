var time = document.getElementById("time");

var th = setInterval(function() {
    time.innerText = new Date();
},1000);