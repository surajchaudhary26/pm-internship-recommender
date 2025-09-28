import re
from typing import List, Dict

def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", (text or "").lower()).strip()

def skills_match_score(candidate_skills: List[str], internship_skills: List[str]) -> int:
    s1 = {normalize(s) for s in candidate_skills if s}
    s2 = {normalize(s) for s in internship_skills if s}
    return len(s1 & s2)

def location_score(preferred: List[str], internship_loc: str) -> int:
    if not preferred:
        return 0
    internship_loc = normalize(internship_loc)
    preferred_norm = [normalize(p) for p in preferred]
    for i, p in enumerate(preferred_norm):
        if p and p in internship_loc:
            return len(preferred) - i
    return 0

def sector_score(preferred_sectors: List[str], internship_sector: str) -> int:
    if not preferred_sectors:
        return 0
    sec = normalize(internship_sector)
    for i, s in enumerate([normalize(x) for x in preferred_sectors]):
        if s and s in sec:
            return len(preferred_sectors) - i
    return 0

def recommend_internships(candidate: Dict, internships: List[Dict], k: int = 5) -> List[Dict]:
    scored = []
    for it in internships:
        # skills are stored as "A;B;C"
        it_skills = [s.strip() for s in (it.get("skills") or "").split(";") if s.strip()]

        sc = 0
        sc += skills_match_score(candidate.get("skills", []), it_skills) * 10
        sc += location_score(candidate.get("preferred_locations", []), it.get("location", "")) * 3
        sc += sector_score(candidate.get("sectors", []), it.get("sector", "")) * 2

        # education bonus
        desc = normalize(it.get("description", ""))
        edu = normalize(candidate.get("education") or "")
        if edu and edu in desc:
            sc += 1

        scored.append((sc, it))

    scored.sort(key=lambda x: (-x[0], x[1].get("title", "")))
    top = [s[1] for s in scored[:k]]

    out = []
    for i in top:
        out.append({
            "title": i.get("title"),
            "skills": i.get("skills"),
            "sector": i.get("sector"),
            "location": i.get("location"),
            "description": i.get("description"),
            "apply_link": i.get("apply_link", ""),
        })
    return out
