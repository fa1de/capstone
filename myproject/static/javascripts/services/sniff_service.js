async function get_interfaces() {
  console.log("======== fetching interfaces ========");
  return await api.get(`/sniff/`);
}

async function start_sniff(i) {
  if (i == -1) {
    alert("Please select an interface to start the sniff.");
    return;
  }
  const response = await api.get(`/sniff/start?i=${i}`);
  alert("Sniffer started.");
  return response;
}

async function stop_sniff() {
  try {
    return await api.get(`/sniff/stop`);
  } catch (e) {
    alert("Sniffer is not running.");
  }
}
