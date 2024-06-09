async function getChart() {
  const protocol_response = await fetch("/protocol");
  const aggregate_response = await fetch("/aggregate");

  const protocol_data = await protocol_response.json();
  const aggregate_data = await aggregate_response.json();

  console.log("======== fetched chart data ========");
  console.log(protocol_data);
  console.log(aggregate_data);

  const protocols = [];
  const ips = [];

  aggregate_data.forEach((agg) => {
    const { key, value } = agg;

    console.log(key);
    if (key.includes("protocol")) {
      protocols.push({ name: key.split("-")[1], count: value });
    }
    if (key.includes("ip")) {
      ips.push({ name: key.split("-")[1], count: value });
    }
  });

  console.log("======== transformed chart data ========");
  console.log(protocols);
  console.log(ips);

  return { protocols, ips };
}

function initChart(data) {
  console.log("======== init chart ========");
  console.log(data);
  const { protocols, ips } = data;

  console.log(protocols);
  console.log(ips);

  const lineChartConfig = {
    type: "line",
    data: {
      labels: protocols.map((p) => p.name),
      datasets: [
        {
          label: "Protocol Count",
          data: protocols.map((p) => p.count),
          fill: false,
          borderColor: "rgb(75, 192, 192)",
          tension: 0.1,
        },
      ],
    },
    options: {
      plugins: {
        datalabels: {
          color: "red",
          align: "end",
          anchor: "end",
          font: { weight: "bold" },
        },
      },
      scales: { y: { beginAtZero: true } },
    },
  };

  const barChartConfig = {
    type: "bar",
    data: {
      labels: ips.map((p) => p.name),
      datasets: [
        {
          label: "Source_Target IP Count",
          data: ips.map((p) => p.count),
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(255, 206, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(255, 159, 64, 0.2)",
          ],
          borderColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)",
            "rgba(255, 206, 86, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(153, 102, 255, 1)",
            "rgba(255, 159, 64, 1)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      plugins: {
        datalabels: {
          color: "red",
          align: "end",
          anchor: "end",
          font: { weight: "bold" },
        },
      },
    },
  };

  return {
    barChart: new Chart(
      document.getElementById("barChart").getContext("2d"),
      lineChartConfig
    ),
    donutChart: new Chart(
      document.getElementById("lineChart").getContext("2d"),
      barChartConfig
    ),
  };
}

function updateChart(charts, data) {
  console.log("======== update chart ========");
  console.log(charts);
  console.log(data);

  const { protocols, ips } = data;
  const { lineChart, barChart } = charts;

  lineChart.data.datasets[0].data = protocols.map((p) => p.count);
  lineChart.update();
  barChart.data.datasets[0].data = ips.map((p) => p.count);
  barChart.update();
}
