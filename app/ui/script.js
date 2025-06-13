let ws;

window.addEventListener("load", () => {
  if (
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
  ) {
    // User prefers dark mode
    document.body.classList.add("dark");
  }
  const apiKey = localStorage.getItem("apiKey");
  if (apiKey) {
    document.getElementById("api-key").value = apiKey;
  }
});

function getContainers() {
  const apiKey = document.getElementById("api-key").value.trim();
  if (!apiKey) {
    alert("Please enter a valid API key.");
    return;
  }

  fetch("./containers", {
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": apiKey,
    },
  })
    .then((response) => {
      if (!response.ok) {
        console.error("Failed to fetch containers:", response.statusText);
        alert("Failed to fetch containers. Check console for details.");
        throw new Error("Failed to fetch containers");
      }
      return response.json();
    })
    .then((data) => {
      const containerSelect = document.getElementById("container");
      containerSelect.innerHTML = ""; // Clear previous options
      const defaultOption = document.createElement("option");
      defaultOption.value = "";
      defaultOption.textContent = "Select a container";
      containerSelect.appendChild(defaultOption);
      if (data.length === 0) {
        alert("No containers found on server.");
        return;
      }
      data
        .sort((a, b) => {
          if (a.status === "running" && b.status !== "running") return -1;
          if (b.status === "running" && a.status !== "running") return 1;
          return a.name.localeCompare(b.name);
        })
        .forEach((container) => {
          const option = document.createElement("option");
          option.value = container.id;
          option.textContent = `${
            container.name || container.id
          } (${container.status.toUpperCase()})`;
          containerSelect.appendChild(option);
        });
      document.getElementById("auth-container").style.display = "none";
      document.getElementById("selector-container").style.display = "block";
    })
    .catch((error) => {
      console.error("Error fetching containers:", error);
      alert("Failed to fetch containers. Check console for details.");
    });
}

function getContainerLog() {
  const apiKey = document.getElementById("api-key").value.trim();
  if (!apiKey) {
    alert("Please enter a valid API key.");
    return;
  }
  const tail = document.getElementById("tail").value;
  const containerId = document.getElementById("container").value;
  if (!containerId) {
    alert("Please select a container.");
    return;
  }
  const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsHost = window.location.host;
  const wsPath = `/ws/logs/${containerId}?tail=${tail}&api_key=${apiKey}`;
  ws = new WebSocket(`${wsProtocol}//${wsHost}${wsPath}`);

  ws.onopen = () => {
    console.log("WebSocket connection established.");
    document.getElementById("connect-btn").style.display = "none";
    document.getElementById("close-btn").style.display = "inline";
    document.getElementById("clear-btn").style.display = "inline";
    document.getElementById("container").disabled = true;
    document.getElementById("tail").disabled = true;
    clearLogs();
  };
  ws.onmessage = (event) => {
    appendLog(event.data);
  };
  ws.onerror = (error) => {
    console.error("WebSocket error:", error);
  };
  ws.onclose = (event) => {
    console.log("WebSocket connection closed:", event);
    document.getElementById("connect-btn").style.display = "inline";
    document.getElementById("close-btn").style.display = "none";
    document.getElementById("clear-btn").style.display = "none";
    document.getElementById("container").disabled = false;
    document.getElementById("tail").disabled = false;
  };
}

function appendLog(logLine) {
  const logsDiv = document.getElementById("logs");
  logEntry = formatLine(logLine);
  logsDiv.appendChild(logEntry);
  logsDiv.scrollTop = logsDiv.scrollHeight; // Auto-scroll to the bottom
}

function formatLine(logLine) {
  const logEntry = document.createElement("div");
  logEntry.classList.add("log-entry");
  const timestampMatch = logLine
    .trim()
    .match(/^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)\s+(.*)$/);
  if (timestampMatch) {
    const timestamp = timestampMatch[1];
    const message = timestampMatch[2];

    const timestampSpan = document.createElement("span");
    timestampSpan.classList.add("timestamp");
    timestampSpan.textContent = new Date(timestamp)
      .toLocaleString("hu-HU", {})
      .replace(". ", ".")
      .replace(". ", ".");

    const messageSpan = document.createElement("span");
    messageSpan.classList.add("message");

    const levelMatch = message.match(/^(INFO|WARNING|ERROR)\b\s*(.*)$/);
    if (levelMatch) {
      const level = levelMatch[1];
      const rest = levelMatch[2];

      const levelSpan = document.createElement("span");
      levelSpan.classList.add("level", level.toLowerCase());
      levelSpan.textContent = level;

      messageSpan.appendChild(levelSpan);
      messageSpan.appendChild(document.createTextNode(rest));
    } else {
      messageSpan.textContent = message;
    }

    logEntry.appendChild(timestampSpan);
    logEntry.appendChild(messageSpan);
  } else {
    logEntry.textContent = logLine; // Fallback for lines without a timestamp
  }
  return logEntry;
}

function clearLogs() {
  const logsDiv = document.getElementById("logs");
  logsDiv.innerHTML = ""; // Clear all logs
}

function close() {
  console.log("Closing WebSocket connection...");
  if (!ws || ws.readyState !== WebSocket.OPEN) {
    console.warn("WebSocket is not open. Cannot close.");
    return;
  }
  ws.close(1000, "User closed the connection");
}

function toggleTheme() {
  const body = document.body;
  body.classList.toggle("dark");
}

window.addEventListener("beforeunload", () => {
  ws.close(1000, "Tab closed or page reloaded");
});
document.getElementById("close-btn").addEventListener("click", close);
