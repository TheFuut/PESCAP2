import os
def check_case(path, subtask):
    with open(path, 'r', encoding='utf-8') as f:
        first = f.readline().strip().split()
        N = int(first[0]); M = int(first[1])
        lines = f.readlines()
        if len(lines) != M:
            return False, f"M mismatch: header {M} vs lines {len(lines)}"
        for ln in lines:
            t,a,b = map(int, ln.split())
            if not (1 <= t <= 3): return False, "Tipo fuera de rango"
            if not (1 <= a <= N and 1 <= b <= N): return False, "Jugador fuera de rango"
            if a == b: return False, "A == B"
            if subtask == 1 and N > 20: return False, "Subtarea1 N>20"
            if subtask == 2 and t != 2: return False, "Subtarea2 contiene tipo != 2"
            if subtask == 3 and (N > 5000 or M > 5000): return False, "Subtarea3 límites"
            if subtask == 4 and (N < 2 or N > 200000 or M < 1 or M > 400000): return False, "Subtarea4 límites"
    return True, "OK"

for fname in os.listdir("cases"):
    if not fname.endswith(".in"): continue
    parts = fname[:-3].split('.')
    # filename format: subtarea-{subtask}.{case}.in
    left = parts[0]  # 'subtarea-{subtask}'
    subtask = int(left.split('-')[1])
    ok,msg = check_case(os.path.join("cases", fname), subtask)
    if not ok:
        print(fname, "ERROR:", msg)
    else:
        print(fname, "OK")
