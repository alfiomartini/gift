document.addEventListener("DOMContentLoaded", charts);

function charts(category) {
  const chart_links = document.querySelectorAll("#charts-menu a");
  chart_links.forEach((anchor) => {
    anchor.addEventListener("click", anchor_chart);
  });
}

function anchor_chart() {
  const anchor = this;
  const category = this.dataset.cat;
  console.log(category);
  // make get request
  let csrftoken = getCookie("csrftoken");
  fetch(`/charts/${category}`, {
    method: "GET",
    headers: {
      "X-CSRFToken": csrftoken,
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    credentials: "same-origin",
  })
    .then((response) => {
      // console.log(response.status);
      return response.json();
    })
    .then((chart) => {
      // console.log(chart);
      drawChart(chart);
    })
    .catch((error) => {
      console.log(error);
    });
}

function drawChart(chart) {
  const main = document.querySelector(".main");
  main.innerHTML = `<div class="chart-container">
                       <canvas id="myChart"></canvas>
                    </div>`;

  let ctx = document.getElementById("myChart");
  let myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: chart["labels"],
      datasets: [
        {
          data: chart["data"],
          label: chart["label"],
          fill: false,
          // borderColor: "lighsteelblue",
          backgroundColor: [
            "blue",
            "yellow",
            "green",
            "red",
            "orange",
            "violet",
          ],
        },
      ],
    },
    options: {
      // https://stackoverflow.com/questions/31631354/how-to-display-data-values-on-chart-js
      plugins: {
        datalabels: {
          anchor: 'end',
          align: 'top',
          color: 'white',
          // formatter: Math.round,
          // font: {
          //   weight: 'bold'
          // }
        }
      },
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        labels: {
          fontColor: "white",
          fontSize: 14,
        },
      },
      scales: {
        xAxes: [
          {
            ticks: {
              fontColor: "limegreen",
            },
            gridLines: {
              zeroLineColor: "limegreen",
            },
          },
        ],
        yAxes: [
          {
            ticks: {
              fontColor: "limegreen",
              beginAtZero: true,
              // https://stackoverflow.com/questions/15751571/change-the-y-axis-values-from-real-numbers-to-integers-in-chart-js
              precision:0,
            },
            gridLines: {
              zeroLineColor: "limegreen",
              color: "limegreen",
            },
          },
        ],
      },
    },
  });
  const chart_container = document.querySelector(".chart-container");
  const anchor_elem = document.createElement("a");
  anchor_elem.href = "/";
  anchor_elem.className = "btn-home";
  const btn_elem = `<div class = "d-flex justify-content-center">
      <button type="button" class="btn btn-dark mt-3">Back Home</button>
     </div>`;
  anchor_elem.innerHTML = btn_elem;
  chart_container.append(anchor_elem);
}
