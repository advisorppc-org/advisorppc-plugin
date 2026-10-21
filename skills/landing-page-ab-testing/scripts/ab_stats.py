#!/usr/bin/env python3
"""A/B test math for landing and pricing pages. Stdlib only (no scipy).

Usage:
  ab_stats.py size  --p 0.04 --mde 0.20 [--alpha 0.05] [--power 0.8] [--daily 600] [--arms 2]
  ab_stats.py test  --na 10400 --xa 416 --nb 10380 --xb 502 [--alpha 0.05]
  ab_stats.py srm   --na 10400 --nb 9800 [--ratio 0.5]

--mde is RELATIVE (0.20 = +20% over baseline). --daily is eligible visitors per day, all arms.
"""
import argparse
import math
from statistics import NormalDist

N = NormalDist()


def sample_size(p: float, mde_rel: float, alpha: float = 0.05, power: float = 0.8) -> int:
    """Visitors needed PER ARM, two-sided two-proportion z-test."""
    p2 = p * (1 + mde_rel)
    pbar = (p + p2) / 2
    za, zb = N.inv_cdf(1 - alpha / 2), N.inv_cdf(power)
    num = (za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p * (1 - p) + p2 * (1 - p2))) ** 2
    return math.ceil(num / (p2 - p) ** 2)


def two_prop_test(na: int, xa: int, nb: int, xb: int, alpha: float = 0.05) -> dict:
    """Pooled z-test for B vs A, plus unpooled CI on the absolute difference."""
    pa, pb = xa / na, xb / nb
    pool = (xa + xb) / (na + nb)
    se_pool = math.sqrt(pool * (1 - pool) * (1 / na + 1 / nb))
    z = (pb - pa) / se_pool
    p_value = 2 * (1 - N.cdf(abs(z)))
    se = math.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb)
    zc = N.inv_cdf(1 - alpha / 2)
    diff = pb - pa
    return {
        "rate_a": pa, "rate_b": pb, "abs_diff": diff,
        "rel_lift": diff / pa if pa else float("nan"),
        "ci_abs": (diff - zc * se, diff + zc * se),
        "z": z, "p_value": p_value, "significant": p_value < alpha,
    }


def srm(na: int, nb: int, ratio_a: float = 0.5) -> dict:
    """Chi-square goodness of fit, 2 arms (1 df). p < 0.001 = sample ratio mismatch."""
    n = na + nb
    ea, eb = n * ratio_a, n * (1 - ratio_a)
    chi2 = (na - ea) ** 2 / ea + (nb - eb) ** 2 / eb
    p_value = math.erfc(math.sqrt(chi2 / 2))  # survival of chi-square with 1 df
    return {"chi2": chi2, "p_value": p_value, "srm": p_value < 0.001}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("size")
    s.add_argument("--p", type=float, required=True)
    s.add_argument("--mde", type=float, required=True)
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--power", type=float, default=0.8)
    s.add_argument("--daily", type=float, default=0)
    s.add_argument("--arms", type=int, default=2)
    t = sub.add_parser("test")
    for k in ("na", "xa", "nb", "xb"):
        t.add_argument(f"--{k}", type=int, required=True)
    t.add_argument("--alpha", type=float, default=0.05)
    r = sub.add_parser("srm")
    r.add_argument("--na", type=int, required=True)
    r.add_argument("--nb", type=int, required=True)
    r.add_argument("--ratio", type=float, default=0.5)
    a = ap.parse_args()

    if a.cmd == "size":
        n = sample_size(a.p, a.mde, a.alpha, a.power)
        print(f"per arm: {n:,}   total: {n * a.arms:,}")
        if a.daily:
            days = n * a.arms / a.daily
            weeks = math.ceil(days / 7)
            print(f"~{days:.0f} days at {a.daily:,.0f}/day -> run {weeks} full week(s) ({weeks * 7} days)")
    elif a.cmd == "test":
        res = two_prop_test(a.na, a.xa, a.nb, a.xb, a.alpha)
        lo, hi = res["ci_abs"]
        print(f"A {res['rate_a']:.4%}  B {res['rate_b']:.4%}  lift {res['rel_lift']:+.1%}")
        print(f"abs diff {res['abs_diff']:+.4%}  CI [{lo:+.4%}, {hi:+.4%}]  z {res['z']:.2f}  p {res['p_value']:.4f}")
        print("SIGNIFICANT" if res["significant"] else "not significant")
    else:
        res = srm(a.na, a.nb, a.ratio)
        print(f"chi2 {res['chi2']:.2f}  p {res['p_value']:.6f}  ->", "SRM: STOP, debug assignment" if res["srm"] else "ok")


if __name__ == "__main__":
    main()
