async function get_interfaces() {
  console.log("======== fetching interfaces ========");
  return await api.get(`/edge/`);
}

async function start_edge(i) {
  if (i == -1) {
    alert("Please select an interface to start the edge.");
    return;
  }
  return await api.get(`/edge/start?i=${i}`);
}

async function stop_edge() {
  try {
    return await api.get(`/edge/stop`);
  } catch (e) {
    alert("Sniffer is not running.");
  }
}
