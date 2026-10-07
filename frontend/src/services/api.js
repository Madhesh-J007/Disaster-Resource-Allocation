const API_BASE = '/api';

async function handleResponse(response) {
  if (!response.ok) {
    const errorText = await response.text();
    let message = 'API Error';
    try {
      const errObj = JSON.parse(errorText);
      message = errObj.detail || errObj.message || message;
    } catch (e) {
      message = errorText || response.statusText;
    }
    throw new Error(message);
  }
  return await response.json();
}

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return handleResponse(res);
}

export async function fetchDistricts() {
  const res = await fetch(`${API_BASE}/districts`);
  return handleResponse(res);
}

export async function fetchDistrictInfo(districtName) {
  const res = await fetch(`${API_BASE}/districts/${encodeURIComponent(districtName)}`);
  return handleResponse(res);
}

export async function fetchStatistics() {
  const res = await fetch(`${API_BASE}/statistics`);
  return handleResponse(res);
}

export async function fetchDemoScenarios() {
  const res = await fetch(`${API_BASE}/demo-scenarios`);
  return handleResponse(res);
}

export async function predictDisaster(conditions) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(conditions)
  });
  return handleResponse(res);
}

export async function assessLocationImpact(payload) {
  const res = await fetch(`${API_BASE}/location-impact`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return handleResponse(res);
}

export async function allocateResources(data) {
  const res = await fetch(`${API_BASE}/resource-allocation`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return handleResponse(res);
}

export async function runSimulation(baseline, modified, location = "Chennai") {
  const res = await fetch(`${API_BASE}/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ baseline, modified, location })
  });
  return handleResponse(res);
}
