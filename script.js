// get json from http://localhost:8081/data using jquery

var discCharts = [];
var ramChartNameToCheck = null;
var swapChartNameToCheck = null;

var runningChartNameToCheck = null;
var sleepingChartNameToCheck = null;
var stoppedChartNameToCheck = null;
var zombieChartNameToCheck = null;

var panels = []

var data = "";

function isPanels(panel) {
    for (var i = 0; i < panels.length; i++) {
        if (panels[i] == panel) {
            return true
        }
    }
    return false
}
function letUpdate(){

    return ramChartNameToCheck != null || swapChartNameToCheck != null || runningChartNameToCheck != null || sleepingChartNameToCheck != null || stoppedChartNameToCheck != null || zombieChartNameToCheck != null
}
function changePanel(){
    //alert("hash changed")
    var frag = location.hash.substr(1);
    // hide all panels from panels array
    for (var i = 0; i < panels.length; i++) {
        var el = document.getElementById(panels[i] + "panel");
        if (el) {
            //console.log(el)
            // remove hidden class
            el.classList.remove("show")
            el.classList.add("hidden")
        }
    }
    if (isPanels(frag)) {
      var el = document.getElementById(frag + "panel");
      if (el) {
        //console.log(el)
        // remove hidden class
        el.classList.remove("hidden")
        el.classList.add("show")
      }
    } else {
        alert("Panel not found")
    }
}
window.addEventListener('hashchange', function() {
    changePanel()

}, false);
function UpdateRamChart(nameee, ramtotal, ramused) {
    if(letUpdate()){
    const chart = nameee.getContext('2d');
    //console.log(chart);
    //console.log(chart.chart);
    //console.log(chart.chart.config)
    chart.chart.config.data.datasets.pop();
    chart.chart.config.data.datasets.push({
        label: ['Free', 'Used'],
        backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)'
        ],
        data: [ramtotal, ramused]
    });
    ramChartNameToCheck.update();
    }
}
function ramChart(nameee, ramtotal, ramused) {
    const ctx = nameee.getContext('2d');
    const name = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Free', 'Used'],
            datasets: [{
                label: '# of bytes used',
                data: [ramtotal, ramused],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 0
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    return name;
}
function lineChart(nameee, datab, label) {
    const labels = [0];
    const datae = {
      labels: labels,
      datasets: [{
        label: label,
        data: [datab],
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }]
    };
    const ctx = nameee.getContext('2d');
    const name = new Chart(ctx, datae);
    return name;
}
function UpdateLineChart(nameee, dateea) {
    if(letUpdate()){
        const chart = nameee.getContext('2d');
        //console.log(chart);
        //console.log(chart.chart);
        //console.log(chart.chart.config)
        chart.chart.config._config.datasets[0].data.push(dateea);
        chart.chart.config._config.labels.push(chart.chart.config._config.length);
        console.log(chart)
        chart.update();
    }
}
function updateData(){
    $.getJSON("http://localhost:8081/data", function(data) {
        console.log(data);
        //for x in data["disk"]["drives"] {
        //    ramChart("diskChart" + x, data['disk'][x].free, data['disk'][x].used);
        //}

        UpdateRamChart(ramChartNameToCheck, data["ram"]["available_bytes"], data["ram"]["used_bytes"]);
        document.getElementById("ramtotal").innerHTML = "Total RAM: " + data["ram"]["total"];
        document.getElementById("ramused").innerHTML = "Total Used: " + data["ram"]["used"];
        document.getElementById("ramfree").innerHTML = "Total Available: " + data["ram"]["available"];

        discCharts.forEach(function(chart, index) {
            //console.log(chart)
            UpdateRamChart(chart, data['disk'][index].free, data['disk'][index].used);
        });
        //UpdateRamChart("diskChart" + x, data['disk'][x]["free"], data['disk'][x]["used"]);
        //data["disk"]["drives"].forEach(function(x){
            //console.log(x);

        //});
    });
}
function createDiskData(){
    /* <div class="center">
        <img id="diskicon" src="icons/hhd.png", width="36">
            <h2 id="disk">Hard Disc</h2>
            <h3 id="disktotal">Hard Disc Total - 0GB</h3>
            <h3 id="diskused">Hard Disc Used - 0GB</h3>
            <h3 id="diskfree">Hard Disc Free - 0GB</h3>
            <canvas id="diskChart" width="100" height="100"></canvas>
            </details>
        </div> */
    discCharts = [];
    //$.getJSON("http://localhost:8081/data", function(data) {
        data["disk"]["drives"].forEach(function(x){
            try{
                var center = document.createElement("div");
                center.className = "center";
                var index = data["disk"]["drives"].indexOf(x);
                center.id = "disk" + index + "panel";
                var diskicon = document.createElement("img");
                diskicon.src = "icons/hhd.png";
                diskicon.width = "36";
                //disk.innerHTML = x + " hard drive";
                var diskSumH2 = document.createElement("h2");
                diskSumH2.innerHTML = "(" + x + ") hard drive";
                center.appendChild(diskSumH2);
                var disktotal = document.createElement("h3");
                var diskused = document.createElement("h3");
                var diskfree = document.createElement("h3");
                disktotal.id = "disktotal" + x;
                diskused.id = "diskused" + x;
                diskfree.id = "diskfree" + x;
                disktotal.innerHTML = "Hard Disc Total - " + data['disk'][x].total_formated;
                diskused.innerHTML = "Hard Disc Used - " + data['disk'][x].used_formated;
                diskfree.innerHTML = "Hard Disc Free - " + data['disk'][x].free_formated;
                var diskChart = document.createElement("canvas");
                diskChart.id = "diskChart" + x;
                diskChart.width = "100";
                diskChart.height = "100";
                center.appendChild(diskicon);
                center.appendChild(disktotal);
                center.appendChild(diskused);
                center.appendChild(diskfree);
                center.appendChild(diskChart);
                center.classList.add("hidden")
                document.getElementById("hddpanel").appendChild(center);
                //var br = document.createElement("br");
                //document.getElementById("hddpanel").appendChild(br);
                discCharts.push(ramChart(diskChart, data['disk'][x]["free"], data['disk'][x]["used"]));

                var div = document.createElement("div");
                var a = document.createElement("a");
                // get index of x in data["disk"]["drives"]
                a.href = "#disk" + index;
                var img = document.createElement("img");
                img.src = "icons/hhd.png";
                img.width = "36";
                a.appendChild(img);
                div.appendChild(a);
                document.getElementById("diskiconsidebar").appendChild(div);
            }
            catch(err){

            }
        //});
    });
}
function generateGpuData(datalist) {
    //$.getJSON("http://localhost:8081/data", function(data) {
        // iterate through the data list and create a new object for each item
        for (var i = 0; i < datalist.length; i++) {
            var dataa = "(" + i + ") " + datalist[i];
            // create a new div for each item
            var div = document.createElement("div");
            // set the class of the div
            div.setAttribute("class", "center");
            div.id = "gpu" + i + "panel";
            // create a new h1 for each item
            var img = document.createElement("img");
            // set source of the image
            img.setAttribute("src", "icons/video-card.png");
            img.setAttribute("width", "36");
            // put img in the div
            div.appendChild(img);
            var h2 = document.createElement("h2");
            div.appendChild(h2);
            h2.innerHTML = dataa;

            //console.log("GPU WAS EXECUTED FOR " + i);

            var Driver = document.createElement("h3");
            var Model = document.createElement("h3");
            var Vendor = document.createElement("h3");
            var RAM = document.createElement("h3");
            div.appendChild(Driver);
            div.appendChild(Model);
            div.appendChild(Vendor);
            div.appendChild(RAM);
            /*console.log(data)
            console.log(data["gpu_driver"]);
            console.log(data["gpu_model"]);
            console.log(data["gpu_vendor"]);
            console.log(data["gpu_ram"]);
            console.log(i)*/
            Driver.innerHTML = "Driver - " + data["gpu_driver"][i];
            Model.innerHTML = "Model - " + data["gpu_model"][i];
            Vendor.innerHTML = "Vendor - " + data["gpu_vendor"][i];
            RAM.innerHTML = "RAM - " + data["gpu_ram"][i];

            // put div in the main div
            document.getElementById("gpupanel").appendChild(div);
            div.classList.add("hidden")

            var a = document.createElement("a");;
            a.href = "#gpu" + i;
            var img = document.createElement("img");
            img.src = "icons/video-card.png";
            img.width = "36";
            a.appendChild(img);
            document.getElementById("gpuiconsidebar").appendChild(a);
        }
    //});
}
function takeCareOfPanels(){
    panels.push("content") // normal panel

    panels.push("windows")
    panels.push("cpu")
    //panels.push("gpu")
    panels.push("ram")
    //panels.push("hdd")
    panels.push("swap")
    panels.push("processes")

    var frag = location.hash.substr(1);
    if (frag == "" || !isPanels(frag)) {
        location.hash = "#content";
    }

    $.getJSON("http://localhost:8081/data", function(tada) {
        tada["disk"]["drives"].forEach(function(x){
            // get index of drive
            var index = tada["disk"]["drives"].indexOf(x)
            panels.push("disk" + index)
        });
        tada["gpu"].forEach(function(x){
            var index = tada["gpu"].indexOf(x)
            panels.push("gpu" + index)
        });
    });
}
function getDataOneTime() {
    $.getJSON("http://localhost:8081/data", function(data) {
        takeCareOfPanels();
        setDataInCategories();
        changePanel();
        ramChartNameToCheck = ramChart(document.getElementById("ramChart"), data["ram"]["available_bytes"], data["ram"]["used_bytes"]);
        document.getElementById("ramiconsidebar").classList.remove("hidden")
        swapChartNameToCheck = ramChart(document.getElementById("swapChart"), data["ram"]["swap_free_bytes"], data["ram"]["swap_bytes"]);
        document.getElementById("swapiconsidebar").classList.remove("hidden")
        generateGpuData(data["gpu"]);
        createDiskData(data["disk"]);
        runningChartNameToCheck = lineChart(document.getElementById("runningChart"), data["processes"]["running"], "Running");
        sleepingChartNameToCheck = lineChart(document.getElementById("sleepingChart"), data["processes"]["sleeping"], "Sleeping");
        stoppedChartNameToCheck = lineChart(document.getElementById("stoppedChart"), data["processes"]["stopped"], "Stopped");
        zombieChartNameToCheck = lineChart(document.getElementById("zombieChart"), data["processes"]["zombie"], "Zombie");
        document.getElementById("processesiconsidebar").classList.remove("hidden")
    });
}
function setDataInCategories(){
    $.getJSON("http://localhost:8081/data", function(data) {
        //console.log(data)
        document.getElementById("windowsversion").innerHTML = "You are running " + data["os"] + " " + data["os_release"];
        document.getElementById("cpu").innerHTML = data["cpu"]["brand_raw"] + " x" + data["cpu"]["count"];
        document.getElementById("manufacturer").innerHTML = "Manufacturer - " + data['manufacturer']
        document.getElementById("model").innerHTML = "Model - " + data['model']
        document.getElementById("osversion").innerHTML = "OS Version - " + data['os_version']
        document.getElementById("hostname").innerHTML = "Computer name - " + data['hostname']
        document.getElementById("boot_time").innerHTML = "Boot Time - " + data['boot_time']
        // remove class hidden from id windowsiconsidebar
        document.getElementById("windowsiconsidebar").classList.remove("hidden")

        document.getElementById("cpu_arch_string_raw").innerHTML = "CPU Architecture - " + data['cpu']['arch_string_raw'] + " / " + data['cpu']['arch']
        document.getElementById("cpu_vendor_id_raw").innerHTML = "Vendor ID - " + data['cpu']['vendor_id_raw']
        document.getElementById("cpu_hz").innerHTML = "CPU Frequency - " + data['cpu']['hz_actual_friendly']
        document.getElementById("cpu_adhz").innerHTML = "Advertised Freq - " + data['cpu']['hz_advertised_friendly']
        document.getElementById("cpu_model").innerHTML = "Model - " + data['cpu']['model']
        document.getElementById("cpu_family").innerHTML = "Family - " + data['cpu']['family']
        document.getElementById("cpu_info").innerHTML = "Data CPU Ver. - " + data['cpu']['cpuinfo_version_string']
        var temp = ""
        data['cpu']['flags'].forEach(function(x){
            temp += x + "<br>"
        });
        document.getElementById("cpu_flags").innerHTML = temp

        document.getElementById("cpuiconsidebar").classList.remove("hidden")
    });
}
function getData(){
    $.getJSON("http://localhost:8081/data", function(data) {
        UpdateRamChart(swapChartNameToCheck, data["ram"]["swap_free_bytes"], data["ram"]["swap_bytes"]);
        document.getElementById("swaptotal").innerHTML = "Total SWAP: " + data["ram"]["swap_total"];
        document.getElementById("swapused").innerHTML = "Total Used: " + data["ram"]["swap"];
        document.getElementById("swapfree").innerHTML = "Total Available: " + data["ram"]["swap_free"];

        UpdateRamChart(ramChartNameToCheck, data["ram"]["available_bytes"], data["ram"]["used_bytes"]);
        document.getElementById("ramtotal").innerHTML = "Total RAM: " + data["ram"]["total"];
        document.getElementById("ramused").innerHTML = "Total Used: " + data["ram"]["used"];
        document.getElementById("ramfree").innerHTML = "Total Available: " + data["ram"]["available"];

        UpdateLineChart(runningChartNameToCheck, data["processes"]["running"]);
        UpdateLineChart(sleepingChartNameToCheck, data["processes"]["sleeping"]);
        UpdateLineChart(zombieChartNameToCheck, data["processes"]["zombie"]);
        UpdateLineChart(stoppedChartNameToCheck, data["processes"]["stopped"]);

        document.getElementById("running").innerHTML = "Running: " + data["processes"]["running"];
        document.getElementById("sleeping").innerHTML = "Sleeping: " + data["processes"]["sleeping"];
        document.getElementById("stopped").innerHTML = "Stopped: " + data["processes"]["stopped"];
        document.getElementById("zombie").innerHTML = "Zombie: " + data["processes"]["zombie"];
        document.getElementById("total").innerHTML = "Total: " + data["processes"]["total"];
    });
    try {
        updateDiskData();
    }
    catch(err){
    }
}
$.getJSON("http://localhost:8081/data", function(datae) {
    data = datae;

})

getDataOneTime();
setInterval(getData, 1000);