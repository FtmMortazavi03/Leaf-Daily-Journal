# -*- coding: utf-8 -*-
import sys, os, shutil
from datetime import datetime

SRC = os.path.join("src", "index.html")

OLD = """  merged.sessions = (Array.isArray(parsed.sessions) ? parsed.sessions : []).map(s => ({
    id: String(s.id || cryptoId()),
    subjectId: String(s.subjectId || ''),
    durationMinutes: clamp(toInt(s.durationMinutes), 1, MAX_DAILY_MINUTES),
    date: /^\\d{4}-\\d{2}-\\d{2}$/.test(s.date || '') ? s.date : today(),
    createdAt: toInt(s.createdAt) || Date.now(),
    note: typeof s.note === 'string' ? s.note.slice(0, 200) : '',
  })).filter(s => s.subjectId && merged.subjects.some(x => x.id === s.subjectId));"""

NEW = """  merged.sessions = (Array.isArray(parsed.sessions) ? parsed.sessions : []).map(s => ({
    id: String(s.id || cryptoId()),
    subjectId: String(s.subjectId || ''),
    durationMinutes: clamp(toInt(s.durationMinutes), 1, MAX_DAILY_MINUTES),
    date: /^\\d{4}-\\d{2}-\\d{2}$/.test(s.date || '') ? s.date : today(),
    createdAt: toInt(s.createdAt) || Date.now(),
    note: typeof s.note === 'string' ? s.note.slice(0, 200) : '',
  })).filter(s => s.subjectId && merged.subjects.some(x => x.id === s.subjectId));"""

def main():
    if not os.path.isfile(SRC):
        print(f"[ERROR] File not found: {SRC}"); sys.exit(1)
    
    with open(SRC, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Just print the current sanitizeState block for debugging
    idx = text.find("merged.sessions = (Array.isArray(parsed.sessions)")
    if idx == -1:
        print("[ERROR] Could not find sessions mapping")
        sys.exit(1)
    
    end = text.find("}));", idx) + 4
    print("[CURRENT BLOCK]:")
    print(text[idx:end])
    print("[END BLOCK]")

if __name__ == "__main__":
    main()