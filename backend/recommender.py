import re
from typing import List, Dict

def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", (text or "").lower()).strip()

def recommend_internships(candidate: Dict, internships, k: int = 5):
    scored = []
    for _, it in internships.iterrows():
        it_skills = [s.strip() for s in (it.get("skills") or "").split(";") if s.strip()]

        # ---- Matching parts ----
        cand_skills = candidate.get("skills", [])
        matched_skills = [s for s in cand_skills if normalize(s) in {normalize(x) for x in it_skills}]

        cand_locs = candidate.get("preferred_locations", [])
        matched_location = None
        for loc in cand_locs:
            if normalize(loc) in normalize(it.get("location", "")):
                matched_location = loc
                break

        cand_secs = candidate.get("sectors", [])
        matched_sector = None
        for sec in cand_secs:
            if normalize(sec) in normalize(it.get("sector", "")):
                matched_sector = sec
                break

        # ---- Scoring ----
        sc = 0
        sc += len(matched_skills) * 10
        sc += (3 if matched_location else 0)
        sc += (2 if matched_sector else 0)

        desc = normalize(it.get("description", ""))
        edu = normalize(candidate.get("education") or "")
        edu_bonus = 1 if edu and edu in desc else 0
        sc += edu_bonus

        scored.append((sc, it, matched_skills, matched_location, matched_sector, edu_bonus))

    scored.sort(key=lambda x: (-x[0], x[1].get("title", "")))
    top = scored[:k]

    # ---- Return with explainability ----
    out = []
    for sc, i, mskills, mloc, msec, edu_bonus in top:
        out.append({
            "title": i.get("title"),
            "skills": i.get("skills"),
            "sector": i.get("sector"),
            "location": i.get("location"),
            "description": i.get("description"),
            "stipend": i.get("stipend", ""),
            "duration": i.get("duration", ""),
            "posted_date": i.get("posted_date", ""),
            "apply_link": i.get("apply_link", ""),
            "score": sc,
            "explanation": {
                "matched_skills": mskills,
                "matched_location": mloc,
                "matched_sector": msec,
                "education_bonus": bool(edu_bonus)
            }
        })
    return out
