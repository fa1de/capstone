const api = {
  get: async (url, params) => {
    const queryParams = params
      ? "?" + new URLSearchParams(params).toString()
      : "";
    const response = await fetch(`${url}${queryParams}`);
    const data = await response.json();
    return data;
  },
  post: async (url, body) => {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    const data = await response.json();
    return data;
  },
  put: async (url, body) => {
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    const data = await response.json();
    return data;
  },
  delete: async (url) => {
    const response = await fetch(url, {
      method: "DELETE",
    });
    const data = await response.json();
    return data;
  },
};
