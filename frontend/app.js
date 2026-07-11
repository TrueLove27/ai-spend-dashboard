const API = "http://localhost:8000";

async function fetchJSON(path) {
  const res = await fetch(`${API}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

function renderSummary(s) {
  document.getElementById("summary-cards").innerHTML = `
    <div class="card"><div class="label">Total Spend</div><div class="value">$${s.total_spend.toLocaleString()}</div></div>
    <div class="card"><div class="label">Connected Calls</div><div class="value">${s.total_calls.toLocaleString()}</div></div>
    <div class="card"><div class="label">Avg Cost / Call</div><div class="value green">$${s.avg_cost_per_call}</div></div>
    <div class="card"><div class="label">Days Tracked</div><div class="value">${s.days_tracked}</div></div>
  `;
}

function renderTable(rows) {
  const tbody = document.querySelector("#daily-table tbody");
  tbody.innerHTML = rows.map(r => {
    const cpc = r.calls ? (r.total / r.calls).toFixed(4) : "0";
    return `<tr>
      <td>${r.date}</td><td>$${r.openai}</td><td>$${r.anthropic}</td>
      <td>$${r.elevenlabs}</td><td>$${r.deepgram}</td>
      <td>${r.calls}</td><td>$${r.total}</td><td>$${cpc}</td>
    </tr>`;
  }).join("");
}

function renderDailyChart(rows) {
  new Chart(document.getElementById("dailyChart"), {
    type: "bar",
    data: {
      labels: rows.map(r => r.date.slice(5)),
      datasets: [
        { label: "OpenAI", data: rows.map(r => r.openai), backgroundColor: "#10b981" },
        { label: "Anthropic", data: rows.map(r => r.anthropic), backgroundColor: "#f59e0b" },
        { label: "ElevenLabs", data: rows.map(r => r.elevenlabs), backgroundColor: "#8b5cf6" },
        { label: "Deepgram", data: rows.map(r => r.deepgram), backgroundColor: "#3b82f6" },
      ],
    },
    options: {
      responsive: true,
      plugins: { legend: { labels: { color: "#8b9cb3" } } },
      scales: {
        x: { stacked: true, ticks: { color: "#8b9cb3" }, grid: { color: "#2d3a4f" } },
        y: { stacked: true, ticks: { color: "#8b9cb3" }, grid: { color: "#2d3a4f" } },
      },
    },
  });
}

function renderCategoryChart(cats) {
  new Chart(document.getElementById("categoryChart"), {
    type: "doughnut",
    data: {
      labels: cats.map(c => c.name),
      datasets: [{ data: cats.map(c => c.amount), backgroundColor: ["#3b82f6","#8b5cf6","#10b981","#f59e0b","#ef4444"] }],
    },
    options: {
      responsive: true,
      plugins: { legend: { position: "bottom", labels: { color: "#8b9cb3", boxWidth: 12 } } },
    },
  });
}

async function init() {
  try {
    const [summary, daily, categories] = await Promise.all([
      fetchJSON("/api/summary"),
      fetchJSON("/api/daily"),
      fetchJSON("/api/categories"),
    ]);
    renderSummary(summary);
    renderTable(daily);
    renderDailyChart(daily);
    renderCategoryChart(categories);
  } catch (e) {
    document.body.innerHTML = `<p style="color:#ef4444;padding:2rem">Could not reach API at ${API}. Start backend: <code>cd backend && uvicorn main:app --reload</code></p>`;
  }
}

init();
