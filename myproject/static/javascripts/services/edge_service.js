async function get_interfaces() {
  return await api.get(`/edge?interface=${interface}`);
}

async function start_edge(i) {
  return await api.get(`/edge/start?i=${i}`);
}
