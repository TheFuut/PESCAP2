#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
solver.py
Lee todos los archivos cases/subtarea-*.in y genera cases/subtarea-*.out
Cada .out contiene la respuesta (un entero) para el caso correspondiente.
"""

import os
import glob
import sys
from collections import defaultdict, deque

INF_NEG = -10**30

def solve_instance(n, L, a, edges):
    # Build adjacency
    g = [[] for _ in range(n+1)]
    for u,v in edges:
        g[u].append(v)
        g[v].append(u)

    sys.setrecursionlimit(10000)

    # We'll do a rooted tree at 1
    parent = [0]*(n+1)
    order = []
    stack = [1]
    parent[1] = -1
    while stack:
        u = stack.pop()
        order.append(u)
        for v in g[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            stack.append(v)

    # postorder
    order = order[::-1]

    # subtree sizes
    size = [1]*(n+1)
    for u in order:
        p = parent[u]
        if p > 0:
            size[p] += size[u]

    # dpR[u] and dpNR[u] will be lists length up to L+1
    # We'll store only up to feasible moves: for a subtree of size s, the maximum useful moves
    # when returning is at most 2*(s-1) (go and come back along all edges), and when not returning at most 2*(s-1)+? but safe to use 2*(s-1)
    max_moves_sub = [0]*(n+1)
    for u in range(1, n+1):
        s = size[u]
        max_moves_sub[u] = min(L, 2*(s))  # safe upper bound

    dpR = [None]*(n+1)
    dpNR = [None]*(n+1)

    for u in order:
        # initialize: using 0 moves inside subtree, we still collect a[u]
        maxm = max_moves_sub[u]
        curR = [INF_NEG] * (maxm+1)
        curNR = [INF_NEG] * (maxm+1)
        curR[0] = a[u-1]
        curNR[0] = a[u-1]

        # process children
        for v in g[u]:
            if v == parent[u]:
                continue
            childR = dpR[v]
            childNR = dpNR[v]
            max_child = len(childR)-1
            # cost to go into child and return: 2 + t (t moves inside child)
            # cost to go into child and not return: 1 + t (t moves inside child, end somewhere inside)
            new_max = min(maxm, len(curR)-1 + max_moves_sub[v])  # conservative
            newR = [INF_NEG] * (maxm+1)
            newNR = [INF_NEG] * (maxm+1)

            # Precompute valid ranges for child usage to avoid iterating useless indices
            # childR[t] valid for t in [0..max_child]
            # When used with return, total added moves = t + 2 (if t>=0)
            # When used with non-return, total added moves = t + 1

            # Merge for newR: previous curR combined with child return options (or skip child)
            for used_prev in range(0, len(curR)):
                if curR[used_prev] <= INF_NEG//2:
                    continue
                # skip child
                if newR[used_prev] < curR[used_prev]:
                    newR[used_prev] = curR[used_prev]
                # try using child and returning
                # allocate t moves inside child (0..max_child)
                max_t = max_child
                # we need used_prev + (t+2) <= maxm
                max_t_allowed = min(max_t, maxm - used_prev - 2)
                for t in range(0, max_t_allowed+1):
                    val = childR[t]
                    if val <= INF_NEG//2:
                        continue
                    idx = used_prev + t + 2
                    # sum values: curR[used_prev] already includes a[u] and other children processed
                    cand = curR[used_prev] + val
                    if cand > newR[idx]:
                        newR[idx] = cand

            # Merge for newNR:
            # Two possibilities:
            # 1) non-return already used earlier: curNR combined with child return options (or skip)
            for used_prev in range(0, len(curNR)):
                if curNR[used_prev] <= INF_NEG//2:
                    continue
                # skip child
                if newNR[used_prev] < curNR[used_prev]:
                    newNR[used_prev] = curNR[used_prev]
                # use child but must return (since non-return already used)
                max_t_allowed = min(max_child, maxm - used_prev - 2)
                for t in range(0, max_t_allowed+1):
                    val = childR[t]
                    if val <= INF_NEG//2:
                        continue
                    idx = used_prev + t + 2
                    cand = curNR[used_prev] + val
                    if cand > newNR[idx]:
                        newNR[idx] = cand

            # 2) use this child as the one non-return child: combine curR (no non-return yet) with childNR
            for used_prev in range(0, len(curR)):
                if curR[used_prev] <= INF_NEG//2:
                    continue
                # skip child (already handled above into newR but for newNR we also can skip)
                if newNR[used_prev] < curR[used_prev]:
                    newNR[used_prev] = curR[used_prev]
                # use child as non-return: cost t+1
                max_t_allowed = min(max_child, maxm - used_prev - 1)
                for t in range(0, max_t_allowed+1):
                    val = childNR[t]
                    if val <= INF_NEG//2:
                        continue
                    idx = used_prev + t + 1
                    cand = curR[used_prev] + val
                    if cand > newNR[idx]:
                        newNR[idx] = cand

            # After merging this child, update curR and curNR
            curR = newR
            curNR = newNR

        # Truncate arrays to length maxm+1 (already sized)
        dpR[u] = curR
        dpNR[u] = curNR

    # root is 1. We can use at most L moves; dpNR[1][k] gives value using exactly k moves.
    root_dp = dpNR[1]
    ans = 0
    # It's allowed to use at most L moves, so take max over k<=L
    for k in range(0, min(L, len(root_dp)-1)+1):
        if root_dp[k] > ans:
            ans = root_dp[k]
    return ans

def process_all_cases(cases_dir="cases"):
    files = sorted(glob.glob(os.path.join(cases_dir, "subtarea-*.in")))
    if not files:
        print("No input files found in 'cases/' matching 'subtarea-*.in'.")
        return
    for infile in files:
        try:
            with open(infile, "r", encoding="utf-8") as f:
                data = f.read().strip().split()
            if not data:
                print(f"Empty file {infile}, skipping.")
                continue
            it = iter(data)
            n = int(next(it))
            L = int(next(it))
            a = []
            for _ in range(n):
                a.append(int(next(it)))
            edges = []
            for _ in range(n-1):
                u = int(next(it)); v = int(next(it))
                edges.append((u,v))
        except Exception as e:
            print(f"Error reading {infile}: {e}")
            continue

        # Solve
        ans = solve_instance(n, L, a, edges)

        # Write output file with same base name but .out
        outfile = infile[:-3] + ".out" if infile.endswith(".in") else infile + ".out"
        try:
            with open(outfile, "w", encoding="utf-8") as fo:
                fo.write(str(ans) + "\n")
            print(f"Wrote {outfile}: {ans}")
        except Exception as e:
            print(f"Error writing {outfile}: {e}")

if __name__ == "__main__":
    process_all_cases("cases")
