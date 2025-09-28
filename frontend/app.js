async function postCandidate(candidate) {
  const resp = await fetch("http://localhost:8000/recommend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(candidate),
  });
  return resp.json();
}

function makeCard(rec) {
  return `
    <div class="border p-3 rounded mb-3">
      <h3 class="font-semibold">${rec.title || "Untitled"}</h3>
      <div class="text-sm text-gray-700">${rec.sector || "N/A"} • ${
    rec.location || "N/A"
  }</div>
      <div class="mt-2 text-sm">Skills: ${rec.skills || "N/A"}</div>
      <p class="mt-2 text-sm text-gray-600">${
        rec.description || "No description available"
      }</p>
      <div class="mt-3">
        <a class="text-blue-600 underline" href="${
          rec.apply_link || "#"
        }" target="_blank">Apply</a>
      </div>
    </div>
  `;
}

document
  .getElementById("candidateForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const education = document.getElementById("education").value;
    const skills = document
      .getElementById("skills")
      .value.split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    const sectors = document
      .getElementById("sectors")
      .value.split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    const preferred_locations = document
      .getElementById("locations")
      .value.split(",")
      .map((s) => s.trim())
      .filter(Boolean);

    const candidate = {
      education,
      skills,
      sectors,
      preferred_locations,
      max_results: 5,
    };

    const resDiv = document.getElementById("results");
    resDiv.innerHTML =
      '<div class="text-sm text-gray-600">Searching...</div>';

    try {
      const data = await postCandidate(candidate);
      console.log("Backend response:", data); // ✅ Debugging

      if (data.recommendations && data.recommendations.length) {
        resDiv.innerHTML = data.recommendations
          .map((r) => makeCard(r))
          .join("");
      } else {
        resDiv.innerHTML =
          '<div class="text-sm text-gray-600">No recommendations found. Try different skills or locations.</div>';
      }
    } catch (err) {
      console.error("Fetch error:", err);
      resDiv.innerHTML =
        '<div class="text-sm text-red-600">Error connecting to backend. Make sure backend is running.</div>';
    }
  });

// ✅ Demo Input Auto-fill + Auto-submit
document.querySelectorAll(".demo-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.getElementById("education").value = btn.dataset.education;
    document.getElementById("skills").value = btn.dataset.skills;
    document.getElementById("sectors").value = btn.dataset.sectors;
    document.getElementById("locations").value = btn.dataset.locations;

    // Auto-submit form
    document
      .getElementById("candidateForm")
      .dispatchEvent(new Event("submit"));
  });
});
