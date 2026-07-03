const API = "/api/logs";

function closeDetails() {
    document.getElementById("details").innerText = "Click request for more info...";
}

async function load() {
    const res = await fetch(API);
    const logs = (await res.json()).slice(0, 20);

    const rows = document.getElementById("rows");
    rows.innerHTML = "";

    let total = logs.length;
    let avg = logs.reduce((a, b) => a + (b.duration_ms || 0), 0) / (total || 1);

    document.getElementById("stats").innerText =
        `Requests: ${total} | Avg latency: ${avg.toFixed(2)} ms`;

    logs.forEach(log => {
        const tr = document.createElement("tr");

        function getStatusClass(status) {
            if (status >= 500) return "status-5xx";
            if (status >= 400) return "status-4xx";
            if (status >= 300) return "status-3xx";
            if (status >= 200) return "status-2xx";
            return "status-1xx";
            }
        const statusClass = getStatusClass(log.status);

        tr.innerHTML = `
        <td>${new Date(log.timestamp).toLocaleTimeString()}</td>
        <td>${log.method}</td>
        <td>${log.path}</td>
        <td class="${statusClass}">${log.status}</td>
        <td>${log.duration_ms}</td>
        `;

        tr.onclick = () => {
        document.getElementById("details").innerText =
            JSON.stringify(log, null, 2);
        };

        rows.appendChild(tr);
    });
  }

  async function loadAnalytics() {
    const res = await fetch("/api/analytics");
    const a = await res.json();

  document.getElementById("analytics").innerHTML = `
    <div class="card"><h3>Total requests</h3><p>${a.total_requests}</p></div>
    <div class="card"><h3>Avg latency</h3><p>${a.average_latency} ms</p></div>
    <div class="card"><h3>Errors</h3><p>${a.error_rate} %</p></div>
    <div class="card"><h3>Top endpoint</h3><p>${a.most_requested_endpoint || "-"}</p></div>
    <div class="card"><h3>Fastest</h3><p>${a.fastest_request} ms</p></div>
    <div class="card"><h3>Slowest</h3><p>${a.slowest_request} ms</p></div>
    <div class="card"><h3>Peak hour</h3><p>${a.peak_hour || "-"}</p></div>
    <div class="card"><h3>Top IP</h3><p>${a.top_client_ip || "-"}</p></div>
  `;
}

load();
loadAnalytics();

setInterval(() => {
  load();
  loadAnalytics();
}, 2000);
