// ✅ Post candidate data to backend
async function postCandidate(candidate) {
  const resp = await fetch("http://localhost:8000/recommend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(candidate),
  });
  return resp.json();
}

// ✅ Create recommendation card
function makeCard(rec) {
  let explain = "";
  if (rec.explanation) {
    if (rec.explanation.matched_skills?.length) {
      // Highlight matched skills
      const highlighted = rec.explanation.matched_skills
        .map((s) => `<span class="bg-green-100 text-green-800 px-1 rounded">${s}</span>`)
        .join(", ");
      explain += `<div>Matched skills: ${highlighted}</div>`;
    }
    if (rec.explanation.matched_location) {
      explain += `<div>📍 Location matched: ${rec.explanation.matched_location}</div>`;
    }
    if (rec.explanation.matched_sector) {
      explain += `<div>🏷️ Sector matched: ${rec.explanation.matched_sector}</div>`;
    }
    if (rec.explanation.education_bonus) {
      explain += `<div>🎓 Education matched in description</div>`;
    }
  }

  return `
    <div class="border p-3 rounded mb-3 shadow-sm bg-white">
      <h3 class="font-semibold text-lg text-blue-700">${rec.title || "Untitled"}</h3>
      
      <div class="text-sm text-gray-700 flex gap-2 mt-1">
        <span class="bg-gray-200 px-2 py-0.5 rounded">${rec.sector || "N/A"}</span>
        <span class="bg-gray-200 px-2 py-0.5 rounded">${rec.location || "N/A"}</span>
      </div>
      
      <div class="mt-2 text-sm">🛠️ <b>Required Skills:</b> ${rec.skills || "N/A"}</div>
      <p class="mt-2 text-sm text-gray-600">${rec.description || "No description available"}</p>
      
      <div class="mt-2 text-xs text-green-700">${explain}</div>
      
      ${
        rec.score
          ? `<div class="mt-2 text-xs text-gray-500">🔢 Match Score: ${rec.score}</div>`
          : ""
      }
      
      <div class="mt-3">
        <a class="inline-block bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700" 
           href="${rec.apply_link || "#"}" target="_blank">Apply Now</a>
      </div>
    </div>
  `;
}

// ✅ Form submission handler
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
