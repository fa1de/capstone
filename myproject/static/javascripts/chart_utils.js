async function getChart() {
  console.log("======== getChart ========");
  const protocol_response = await fetch("/protocol");
  const aggregate_response = await fetch("/aggregate");

  const protocol_data = await protocol_response.json();
  const aggregate_data = await aggregate_response.json();

  console.log("======== fetched chart data ========");
  console.log(protocol_data);
  console.log(aggregate_data);

  const protocols = [];
  const ips = [];
  const patterns = [];

  aggregate_data.forEach((agg) => {
    const { key, value } = agg;

    console.log(key);
    if (key.startsWith("protocol")) {
      protocols.push({ name: key.split("<|start|>")[1], count: value });
    } else if (key.startsWith("ip")) {
      ips.push({ name: key.split("<|start|>")[1], count: value });
    } else if (key.startsWith("pattern")) {
      patterns.push({ name: key.split("<|start|>")[1], count: value });
    }
  });

  console.log("======== transformed chart data ========");
  console.log(protocols);
  console.log(ips);
  console.log(patterns);

  return { protocols, ips, patterns };
}

function initChart() {
  console.log("======== init chart ========");

  const lineChartConfig = {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Protocol Count",
          data: [],
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
      labels: [],
      datasets: [
        {
          label: "Source_Target IP Count",
          data: [],
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
    lineChart: new Chart(
      document.getElementById("lineChart").getContext("2d"),
      lineChartConfig
    ),
    barChart: new Chart(
      document.getElementById("barChart").getContext("2d"),
      barChartConfig
    ),
  };
}

function updateChart(charts, data) {
  console.log("======== update chart ========");
  console.log(charts);
  console.log(data);

  const { protocols, ips, patterns } = data;
  const { lineChart, barChart } = charts;

  protocols.sort((a, b) => a.name.localeCompare(b.name));
  ips.sort((a, b) => a.name.localeCompare(b.name));

  console.log(lineChart, barChart);

  barChart.data.labels = protocols.map((p) => p.name);
  barChart.data.datasets[0].data = protocols.map((p) => p.count);
  barChart.update();
  lineChart.data.labels = ips.map((p) => p.name);
  lineChart.data.datasets[0].data = ips.map((p) => p.count);
  lineChart.update();

  const tbody = document.getElementById("pattern-tbody");
  tbody.innerHTML = "";

  patterns.slice(0, 20).forEach((p) => {
    const tr = document.createElement("tr");
    const [protocol, pattern] = p.name.split("-");
    const sliceLength = 100;
    const modifiedPattern =
      pattern.length > sliceLength
        ? `${pattern.slice(0, sliceLength)}...`
        : pattern;
    tr.innerHTML = `<td>${protocol}</td><td>${modifiedPattern}</td> <td>${p.count}</td>`;
    tbody.appendChild(tr);
  });
}
