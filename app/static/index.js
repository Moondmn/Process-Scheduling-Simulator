// import {renderGanttChart} from './chart.mjs';
const comapreDataSection = document.getElementById("comapredata")
const comparedAll = document.getElementById("compare_all");
const selectedAlgoSpan = document.getElementById('selectedAlgoSpan');
const selectedAlgoSpanG = document.getElementById('selectedAlgoSpanG');

const compare_fairness = document.getElementById("compare_fairness");
const comparedWT = document.getElementById("compare_wt");
const comparedTT = document.getElementById("compare_tt");
const comparedEX = document.getElementById("compare_ex");
const comparedFT = document.getElementById("compare_ft");
pr_bool = false;
var acc = document.getElementsByClassName("accordion");
var i;
var receivedDataP = document.getElementById('recievedDataP');
var compareCheckBox = document.getElementById("compare_box")

const selectedAlgoOut = document.getElementById("selectedAlgoOut");
const selectedAlgo = document.getElementById('selectedAlgo');
const selectedAlgoLabel = document.getElementById('selectedAlgoLabel');
var mainReceivedData = ""
var reveivedProcessesDatas = ""
var receivedAvgData = ""
var receivedReady = ""


// var compareCheckBox = document.getElementById("compare").defaultValue = "0";
// receivedDataP.style.display="none";

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
}

function changeScheduler() {
    var selectOption = document.getElementById('selectedAlgo');
    var qTimeContainer = document.getElementById('qTimeContainer');
    var selectedAlgoSpan = document.getElementById('selectedAlgoSpan');
    // var qTimeInput = document.getElementById('qTime');
    // Check if the selected option is "rr" or "srtf"
    var selectedOption = selectOption.options[selectOption.selectedIndex].value;
    var isRR = selectedOption === 'rr';
    var isPr = selectedOption === 'pr';
    switch (selectedOption){
        case ('rr'):
            selectedAlgoSpanG.innerText = 'RR'
            selectedAlgoSpan.innerText = 'RR'
            break
        case ('fcfs'):
            selectedAlgoSpanG.innerText = 'FCFS'
            selectedAlgoSpan.innerText = 'FCFS'
            break
        case ('spn'):
            selectedAlgoSpan.innerText = 'SPN'
            selectedAlgoSpanG.innerText = 'SPN'
            break
        case ('srtf'):
            selectedAlgoSpanG.innerText = 'SRTF'
            selectedAlgoSpan.innerText = 'SRTF'
            break
        case ('pr'):
            selectedAlgoSpanG.innerText = 'Priority'
            selectedAlgoSpan.innerText = 'Priority'
            break
        case ('hrrn'):
            selectedAlgoSpanG.innerText = 'HRRN'
            selectedAlgoSpan.innerText = 'HRRN'
            break
        case ('sjn'):
            selectedAlgoSpanG.innerText = 'SJN'
            selectedAlgoSpan.innerText = 'SJN'
            break

    }

    
    // Toggle visibility of qTimeContainer based on the selected option
    qTimeContainer.style.display = isRR ? 'block' : 'none';
    // qTimeInput.display = isRR ? false : 'none';
    pr_bool = isPr ? true : false;
    var prtable = document.querySelectorAll('#prtable').forEach(ele=>{
        ele.style.display = isPr ? 'block' : 'none';
        // ele.style
    })
}

var numRowsInput = document.getElementById('numRows');
let ganttChart;
//var numOfPs;
numRowsInput.addEventListener("input", (event) => {
    var desiredNumRows = parseInt(numRowsInput.value, 10);
    var table = document.getElementById('dataTable');
    var currentNumRows = table.rows.length - 1;  // Subtract 1 to exclude the header row

    // Calculate the difference between current and desired rows
    var numRowsToAdd = desiredNumRows - currentNumRows;

    // Add or remove rows based on the difference
    if (numRowsToAdd > 0) {
        for (var i = 0; i < numRowsToAdd; i++) {
            var newRow = table.insertRow(table.rows.length);
            newRow.id = "trinp"
            var cellCol = newRow.insertCell(0);
            var cell1 = newRow.insertCell(1);
            var cell2 = newRow.insertCell(2);
            var cell3 = newRow.insertCell(3);
            cellCol.scope = "row"
            cell3.style.display = pr_bool ? 'block' : 'none';
            cell3.id ='prtable';
            cellCol.innerHTML = `P${(currentNumRows + i + 1)}`
            cellCol.className = 'font-bold pr-2'
            cell1.innerHTML = `<input class="h-10 w-full rounded border-gray-400 border text-center text-black font-meduim" min="0" type="number" name="${(currentNumRows + i + 1)}-at" required>`;
            cell2.innerHTML = `<input class="h-10 w-full rounded border-gray-400 border text-center text-black font-meduim" min="0" type="number" name="${(currentNumRows + i + 1)}-cbt" required>`;
            cell3.innerHTML = `<input class="h-10 lg:w-16 w-full   rounded border-gray-400 border text-center text-black font-meduim" min="0" type="number" name="${(currentNumRows + i + 1)}-pr" value=0>`;
        }
    } else if (numRowsToAdd < 0) {
        for (var i = 0; i < -numRowsToAdd; i++) {
            table.deleteRow(-1);  // Remove the last row
        }
    }
})

function checkIfAllCellsAreFilled() {
    var table = document.getElementById('dataTable');
    var rows = table.rows;
    var cellsCount = 0;
    var cellsFilled = 0;

    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].cells;

        for (var j = 0; j < cells.length; j++) {
            var input = cells[j].querySelector('input');

            if (input) {
                cellsCount++;
                if (input.value.trim() !== '') {
                    cellsFilled++;
                }
            }
        }
    }

    if (cellsCount === cellsFilled) {
        return true
    } else {
        return false
    }
}


function fillUnfilledInputs() {
    var table = document.getElementById('dataTable');
    var rows = table.rows;
    var rowsFilled = 0;
    var allCellsFilled = true;

    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].cells;

        for (var j = 0; j < cells.length; j++) {
            var input = cells[j].querySelector('input');

            if (input) {
                if (input.value.trim() === '') {
                    allCellsFilled = false;

                    console.log(j)
                    if (i-1 === 0 && j-1 === 0) {
                        // First cell in the first row should be 0
                        input.value = 0;
                    } else if (i-1 === 0) {
                        // Other cells in the first row should be random * length of table
                        input.value = Math.floor(Math.random() * table.rows.length)+5;
                    } else {
                        // Cells in other rows should be random * length of table * 1.5
                        input.value = Math.floor(Math.random() * table.rows.length * 1.5) + 1;
                    }
                    rowsFilled++;
                }
            }
        }
    }

    // Check if all cells are filled; if true, refill all cells
    if (allCellsFilled) {
        for (var i = 0; i < rows.length; i++) {
            var cells = rows[i].cells;

            for (var j = 0; j < cells.length; j++) {
                var input = cells[j].querySelector('input');

                if (input) {
                    if (i-1 == 0 && j-1 == 0) {
                        // First cell in the first row should be 0
                        input.value = 0;
                    } else if (j-1 == 0) {
                        // Other cells in the first row should be random * length of table
                        input.value = Math.floor(Math.random() * table.rows.length)+5;
                    } else {
                        // Cells in other rows should be random * length of table * 1.5
                        input.value = Math.floor(Math.random() * table.rows.length * 1.5) + 1;
                    }
                    rowsFilled++;
                }
            }
        }
    }
}


function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }




function collectRowData(row) {
    const inputs = row.querySelectorAll('input');
    console.log(inputs + "dhj")
    const rowData = {};
    inputs.forEach(input => {
        if (input.value != "") {
            rowData[input.name] = input.value;
        }
    });
    return rowData;
}

document.getElementById('myForm').addEventListener('htmx:configRequest', (event) => {
    console.log(event.detail.parameters);
    console.log("hahahah",compareCheckBox.checked)
    if (!compareCheckBox.checked){
        // compareCheckBox.value = '0'
        event.detail.parameters.compare = "0"
    }
    else{
        // compareCheckBox.value = '1'
        event.detail.parameters.compare = "1"
    }
    //const formData = {...event.detail.parameters};

    //console.log(formData)
    //event.detail.parameters = {}
    const table = document.getElementById('dataTable')
    const rows = table.querySelectorAll('tr');
    console.log(rows)
    /*if (Object.keys(event.detail.parameters).some(key => key.includes('cbt') || key.includes('at'))) {
        console.log("2-------------2")
            console.log(collectRowData(rows[1]))
            const proccessDatas = Array.from(rows).map(row => collectRowData(row))
            console.log(typeof proccessDatas)
            Object.entries(proccessDatas).forEach( v =>{
                const [key, value] = v
                console.log( value)
                event.detail.parameters[`${key}`] = value
            })
    }
    Object.keys(event.detail.parameters).forEach(key => {
        if (key.includes("at") || key.includes("cbt")){
            delete event.detail.parameters[key]
        }
    })*/

    //event.detail.parameters["prodcess"] = "proccessDatas"
    console.log(event.detail.parameters, "dammmamamama")
});

// Function to handle form submission and render the chart
// document.getElementById('receivedData').addEventListener('htmx:afterSwap', function (event) {
//     console.log("--------")
//     var receivedDataSpan = document.getElementById('receivedData');
//     var jsonData = JSON.parse(receivedDataSpan.innerText);

//     // Display received data in the span
//     receivedDataSpan.innerHTML = '<pre>' + JSON.stringify(jsonData, null, 2) + '</pre>';

//     // Render the chart with received data
//     renderGanttChart(jsonData);
// });
function togglePriorityOption() {
    const selectedAlgo = document.getElementById('selectedAlgo');
    const priorityOption = selectedAlgo.querySelector('option[value="pr"]');

    if (selectedAlgo.value === 'rr' || selectedAlgo.value === 'srtf') {
        priorityOption.style.display = 'block';  // Show "Priority" option
    } else {
        priorityOption.style.display = 'none';   // Hide "Priority" option
    }
}
function createTableHeader() {
    const existingHeader = document.querySelector('#processesTable thead');
    if (existingHeader) {
        existingHeader.remove(); // Remove existing header
    }

    const tableHeader = document.createElement('thead');
    const headerRow = document.createElement('tr');

    ['Name', 'Arrival Time', 'Burst Time', 'Turnaround Time', 'Waiting Time','Finish Time'].forEach(column => {
        const th = document.createElement('th');
        th.className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider"
        th.textContent = column;
        headerRow.appendChild(th);
    });

    tableHeader.appendChild(headerRow);
    document.querySelector('#processesTable').appendChild(tableHeader);
}

function updateTable(processesData) {
    // Sort the data based on the 'name' property
    processesData.sort((a, b) => a.name - b.name);

        // Reference to the table body
        const tableBody = document.querySelector('#processesTable tbody');
        
        // Clear existing rows
        tableBody.innerHTML = '';
        
        // Iterate through the sorted data and create table rows
        var avgtt = 0;
        var avgwt = 0;
        var avgft = 0;
        var n_cole = 0;
        processesData.forEach(process => {
            const row = document.createElement('tr');
            // row.className =""
            
            ['name', 'arrival_time', 'burst_time', 'turnaround_time', 'waiting_time', 'finish_time'].forEach(key => {
                const cell = document.createElement('td');
                cell.className="px-5 py-5 border-b border-gray-200 bg-white text-md"
                if (key === 'name'){
                    cell.textContent = "P " + process[key];
                    cell.className = "font-bold px-5 py-5 border-b border-gray-200 bg-white text-md"
                }
                else{
                    cell.textContent =  process[key];
                }
                if (key==='turnaround_time'){
                    avgtt += process['turnaround_time']
                    n_cole += 1
                }else if (key==='waiting_time'){
                    avgwt += process['waiting_time']
                }
                else if (key==='finish_time'){
                    avgft += process['finish_time']
                }
                
                row.appendChild(cell);
            });
            
            tableBody.appendChild(row);
        });
        const row = document.createElement('tr');
        const cell1 = document.createElement('td');
        const celltt = document.createElement('td');
        const cellwt = document.createElement('td');
        const cellft = document.createElement('td');
        cell1.textContent="Avarage:"
        cell1.className="px-5 py-5 border-b border-gray-200 bg-white text-md text-right"
        celltt.className="px-5 py-5 border-b border-gray-200 bg-white text-md font-semibold"
        cellwt.className="px-5 py-5 border-b border-gray-200 bg-white text-md font-semibold"
        cellft.className="px-5 py-5 border-b border-gray-200 bg-white text-md font-semibold"
        cell1.colSpan = 3
        celltt.textContent = `${avgtt} / ${n_cole} = ${(avgtt/n_cole).toFixed(1)}`
        cellwt.textContent = `${avgwt} / ${n_cole} = ${(avgwt/n_cole).toFixed(1)}`
        cellft.textContent = `${avgft} / ${n_cole} = ${(avgft/n_cole).toFixed(1)}`
        row.appendChild(cell1);  
        row.appendChild(celltt);  
        row.appendChild(cellwt);  
        row.appendChild(cellft);  
        tableBody.appendChild(row)
        return n_cole;
}
function renderGanttChart(gantt_data, process_data) {
    var ctx = document.getElementById("ganttChart").getContext("2d");
  
    // Destroy the existing chart instance if it exists
    if (ganttChart) {
      ganttChart.destroy();
    }
  
    var datasets = [];
  
    // Loop through the rows of data
    gantt_data.sort((a, b) => a.job - b.job);
    process_data.sort((a, b) => a.name - b.name);
    // Extract the "job" and "gantt_seq" data
    const jobs = gantt_data.map((entry) => entry.job);
  
    const ganttSeq = gantt_data.map((entry) => entry.gantt_seq[0]);
    const ganttSeqLenght = gantt_data.map((entry) => entry.gantt_seq.length);
    const labels = jobs.map((job) => `Job ${job}`);
  
    const arrivalTimes = process_data.map((entry) => entry.arrival_time);
  
    const maxLength = Math.max(...ganttSeqLenght);
  
    datasets = new Array();
    for (var i = 0; i < maxLength; i++) {
      g = gantt_data.map((entry) => entry.gantt_seq[i]);
      if (g.some((ele) => ele === undefined)) {
        g.forEach((ele, index, arr) => {
          arr[index] = Array.isArray(ele)
            ? ele.map((innerEle) => (innerEle === undefined ? [] : innerEle))
            : ele === undefined
              ? []
              : ele;
        });
  
        console.log("Modified Array:", g);
      } else {
        console.log("No undefined elements");
      }
      // console.log(g,"sss--------")
      datasets.push({
        type: "bar",
        label: "dd",
        data: g, // Use the duration as the data
        backgroundColor: "rgba(87, 199, 175, 0.5)",
        borderColor: getRandomColor(),
        borderRadius: 7,
        borderWidth: 2,
        borderSkipped: false,
      });
    }
    console.log(datasets, "aghaye moalem");
  
    const scatterData = jobs.map((job, index) => ({
      y: job,
      x: arrivalTimes[index],
    }));
  
    const datasets_bars = gantt_data.map((entry) => ({
      label: `Job ${entry.job}`,
      type: "bar",
      data: entry.gantt_seq.map((seq) => [seq[0], seq[1]]),
      backgroundColor: getRandomColor(), // Generate a random color for each dataset
      borderWidth: 1,
    }));
    datasets.push({
      type: "scatter",
      label: "Arrival Time",
      data: scatterData, // Use the duration as the data
      backgroundColor: "rgba(5, 109, 192, 2)",
    });
    console.log(ganttSeq, "2-------------2");
    ganttChart = new Chart(ctx, {
      data: {
        labels: labels,
        datasets: datasets,
      },
      options: {
        plugins: {
          legend: {
            display: false,
          },
        },
  
        indexAxis: "y",
        scales: {
          y: {
            stacked: true,
            beginAtZero: true,
            title: {
              display: true,
              text: "Jobs / Processes",
            },
          },
          x: {
            stacked: false,
            title: {
              display: true,
              text: "Duration",
            },
          },
        },
      },
    });
  }
  function calculateWeight(algorithmData) {
    const weights = [2, 1, 2]; // Adjust weights as needed
    const weightedSum = algorithmData.reduce(
      (sum, item, index) => sum + item * weights[index],
      0
    );
    return weightedSum;
  }
  function createDivsAndSpans(sortedData, index, docdoc, defText) {
    // Create a div element
    docdoc.innerHTML=''
    const containerDiv = document.createElement('div');
    containerDiv.className = "flex w-full justify-start gap-4	 items-center"
//     const defaultSpan = document.createElement('span');
//   defaultSpan.textContent = defText;

//   // Append the default span to the div
//   containerDiv.appendChild(defaultSpan);
    // Append spans to the div based on the sorted data
    sortedData.forEach(item => {
      const algorithmName = Object.keys(item)[0];
      const value = item[algorithmName][index];
  
      // Create a span element
      const spanElement = document.createElement('span');
      spanElement.className = "px-4 py-2  text-sm my-2 font-small bg-gray-300 rounded-md uppercase"
      if (index===0 && docdoc!==compare_fairness){
          spanElement.textContent = `${algorithmName}: ${value.toExponential(1)}`;
        }else if(docdoc===compare_fairness){
            spanElement.textContent = `${value}`;

        }
        else{
            spanElement.textContent = `${algorithmName}: ${value.toFixed(1)}`
            // spanElement.className += " ml-5"
      }
      // Append the span to the div
      containerDiv.appendChild(spanElement);
    });
  
    // Append the div to the body
    docdoc.appendChild(containerDiv);
  }
document.getElementById('myForm').addEventListener('htmx:afterRequest', event => {
     mainReceivedData = JSON.parse(event.detail.xhr.response)
     reveivedProcessesDatas = mainReceivedData.evaluation
     receivedAvgData = mainReceivedData.avgs
     receivedReady = mainReceivedData.readHandler
    

    // var receivedData_compared = JSON.parse(event.detail.xhr.response)[1]
    console.log(reveivedProcessesDatas.gantt_chart_info)
    console.log("--------")
    var receivedDataSpan = document.getElementById('receivedData');
    receivedDataP.style.display= "block";
    receivedDataSpan.innerHTML = '<pre class="font-mono text-sm">' + JSON.stringify(mainReceivedData, null, 2) + '</pre>';
    const defaultInfo = document.getElementById('defaultInfo');
    const basicReceived = document.getElementById('basicReceived');
    const ganttChart = document.getElementById('ganttChartSection');
    defaultInfo.style.display = 'none';
    basicReceived.style.display = 'block';
    ganttChart.style.display = 'block';
    if (!receivedAvgData){
        selectedAlgoOut.style.display = "none"
        createTableHeader();
        updateTable(reveivedProcessesDatas.solved_processes_info);
        renderGanttChart(reveivedProcessesDatas.gantt_chart_info, reveivedProcessesDatas.solved_processes_info);
    }
    else if(receivedAvgData){
        selectedAlgoOut.style.display = "block"
        selectedAlgoOut.value = "fcfs"
        selectedAlgoSpan.innerText = 'FCFS'
        selectedAlgoSpanG.innerText = 'FCFS'
        console.log(reveivedProcessesDatas)
        createTableHeader();
        updateTable(reveivedProcessesDatas.fcfs.solved_processes_info);
        renderGanttChart(reveivedProcessesDatas.fcfs.gantt_chart_info, reveivedProcessesDatas.fcfs.solved_processes_info);

    }

    // Render the chart with received data

    // ---------------

// mamad = [comparedTT,comparedWT,comparedFT]
// const comparedqAll = document.getElementById("compare_ft");
// if (!compareCheckBox.checked){
//     // for(var ele in [comparedAll,comparedTT,comparedWT,comparedFT]){
// [comparedAll,comparedTT,comparedWT,comparedFT].forEach(ele=>{
//         if (ele.hasChildNodes){
//             while (ele.firstChild) {
//                 ele.removeChild(ele.firstChild);
//             }
//         }
//     })
// }

    

comapreDataSection.style.display = receivedAvgData ?'block' : 'none'
if (receivedAvgData !==null ){

    // receivedAvgData.sort((a, b) => a[Object.keys(a)[0]][0] - b[Object.keys(b)[0]][0]);
    // console.log(receivedAvgData)
    // // if (!compareCheckBox.checked){
    //     [comparedAll,comparedTT,comparedWT,comparedFT].forEach(ele=>{
    //         if (ele.hasChildNodes){
    //             while (ele.firstChild) {
    //                 ele.removeChild(ele.firstChild);
    //             }
    //         }
    //     })
        // }

    // receivedAvgData.forEach((item,index) => {
    //     const span_all = document.createElement("div");
    //     span_all.className = "flex my-5 items-center	";
        
    //     const indexDiv_all = document.createElement("span");
    //     indexDiv_all.className = "block text-md mr-2 font-small text-gray-700";
    //     indexDiv_all.textContent = index + 1;
        
    //     const contentDiv_all = document.createElement("span");
    //     contentDiv_all.className = " px-4 py-2 block text-md my-2 font-small bg-gray-300 rounded-md uppercase";
    //     contentDiv_all.textContent = item[1];

    //     // span_all.textContent = item[1];
    //     span_all.appendChild(indexDiv_all);
    //     span_all.appendChild(contentDiv_all);

    //     comparedAll.appendChild(span_all);
    // });
    const jj = ["tt","wt","ft"]
    // mamad.forEach((haha,indexx)=>{
    //     receivedAvgData[jj[indexx]].forEach((ele, index) => {
    //         const span_all = document.createElement("div");
    //         span_all.className = "flex my-5 items-center";
        
    //         const indexDiv_all = document.createElement("span");
    //         indexDiv_all.className = "block text-md mr-2 font-small test-sm text-gray-700";
    //         indexDiv_all.textContent = index + 1;
        
    //         const contentDiv_all = document.createElement("span");
    //         contentDiv_all.className = "px-4 py-2 block text-md my-2 font-small text-sm bg-gray-300 rounded-md uppercase";
        
    //         // Access the keys (algorithm names) in ele[1]
    //         const algorithmNames = Object.keys(ele[1]);
        
    //         // Iterate through algorithm names and set the content
    //         algorithmNames.forEach(algorithmName => {
    //             const algorithmValues = ele[1][algorithmName];
    //             contentDiv_all.textContent += `${algorithmName}`;
    //             if (indexx===0){
    //                 contentDiv_all.textContent += `-${(algorithmValues.tt).toFixed(1)}`;
    //             }else if(indexx===1){
    //                 contentDiv_all.textContent += `-${(algorithmValues.wt).toFixed(1)}`;
    //             }else if(indexx===2){
    //                 contentDiv_all.textContent += `-${(algorithmValues.ft).toFixed(1)}`;

    //             }
                
    //         });
        
    //         span_all.appendChild(indexDiv_all);
    //         span_all.appendChild(contentDiv_all);
    //         haha.appendChild(span_all);
    //     });
    // })
const sortedFirst = receivedAvgData.sort((a, b) => (a[Object.keys(a)[0]][0] - b[Object.keys(b)[0]][0]));
  const sortedSecond = receivedAvgData.sort((a, b) => (a[Object.keys(a)[0]][1] - b[Object.keys(b)[0]][1]).toFixed(1));
  const sortedThird = receivedAvgData.sort((a, b) => (a[Object.keys(a)[0]][2] - b[Object.keys(b)[0]][2]).toFixed(1));
  const sortedFourth = receivedAvgData.sort((a, b) => (a[Object.keys(a)[0]][3] - b[Object.keys(b)[0]][3]).toFixed(1));
  
  // Create divs and spans for each sorted element
  createDivsAndSpans(sortedFirst, 0,comparedEX, "ET"); // First element
  createDivsAndSpans(sortedSecond, 1,comparedTT, "TT"); // Second element
  createDivsAndSpans(sortedThird, 2,comparedWT,"WT"); // Third element
  createDivsAndSpans(sortedFourth, 3,comparedFT,"FT");

  const weightedData = receivedAvgData.map((item) => ({
    algorithm: Object.keys(item),
    weight: calculateWeight(item[Object.keys(item)[0]]),
  }));
  
  // Sort based on weights
  const sortedWeighted = weightedData.sort(
    (a, b) => a.weight - b.weight
  );
  
  // Create divs and spans for each sorted element
  createDivsAndSpans(sortedWeighted, 0,compare_fairness,"ff");
    
    
}
// ---------------------

    
    
})

function compareOpt(){
    const learnrini = document.getElementById("compareLearn")
    if (compareCheckBox.checked){
        learnrini.style.display = "block"
        qTimeContainer.style.display = "block"
        selectedAlgo.style.display = "none"
        selectedAlgoLabel.style.display = "none"
    }else{
        
        learnrini.style.display = "none"
        qTimeContainer.style.display = "none"
        selectedAlgo.style.display = "block"
        selectedAlgoLabel.style.display = "block"
    }
}

function changeSchedulerOut(){
    var selectedOption = selectedAlgoOut.options[selectedAlgoOut.selectedIndex].value;
    switch (selectedOption){
        case ('rr'):
            selectedAlgoSpan.innerText = 'FCFS'
            selectedAlgoSpanG.innerText = 'FCFS'
            updateTable(reveivedProcessesDatas.rr.solved_processes_info)
            renderGanttChart(reveivedProcessesDatas.rr.gantt_chart_info, reveivedProcessesDatas.rr.solved_processes_info);

            break
        case ('fcfs'):
            selectedAlgoSpan.innerText = 'FCFS'
            selectedAlgoSpanG.innerText = 'FCFS'
            updateTable(reveivedProcessesDatas.fcfs.solved_processes_info)
            renderGanttChart(reveivedProcessesDatas.fcfs.gantt_chart_info, reveivedProcessesDatas.fcfs.solved_processes_info);

            break
        case ('spn'):
            selectedAlgoSpan.innerText = 'SPN'
            selectedAlgoSpanG.innerText = 'SPN'
            updateTable(reveivedProcessesDatas.spn.solved_processes_info)
            renderGanttChart(reveivedProcessesDatas.spn.gantt_chart_info, reveivedProcessesDatas.spn.solved_processes_info);

            break
        case ('srtf'):
            selectedAlgoSpan.innerText = 'SRTF'
            selectedAlgoSpanG.innerText = 'SRTF'
            updateTable(reveivedProcessesDatas.srtf.solved_processes_info)
            renderGanttChart(reveivedProcessesDatas.srtf.gantt_chart_info, reveivedProcessesDatas.srtf.solved_processes_info);

            break
        case ('hrrn'):
            selectedAlgoSpan.innerText = 'HRRN'
            selectedAlgoSpanG.innerText = 'HRRN'
            updateTable(reveivedProcessesDatas.hrrn.solved_processes_info)
            renderGanttChart(reveivedProcessesDatas.hrrn.gantt_chart_info, reveivedProcessesDatas.hrrn.solved_processes_info);

            break
        case ('sjn'):
            selectedAlgoSpan.innerText = 'SJN'
            selectedAlgoSpanG.innerText = 'SJN'
            updateTable(reveivedProcessesDatas.sjn.solved_processes_info)
            renderGanttChart(reveivedProcessesDatas.sjn.gantt_chart_info, reveivedProcessesDatas.fcfs.solved_processes_info);
            break

    }
}