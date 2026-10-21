#!/usr/bin/env python3
"""A/B test math for landing and pricing pages. Stdlib only (no scipy).

Usage:
  ab_stats.py size  --p 0.04 --mde 0.20 [--alpha 0.05] [--power 0.8] [--daily 600] [--arms 2]
  ab_stats.py test  --na 10400 --xa 416 --nb 10380 --xb 502 [--alpha 0.05]
  ab_stats.py srm   --na 10400 --nb 9800 [--ratio 0.5]

--mde is RELATIVE (0.20 = +20% over baseline). --daily is eligible visitors per day, all arms.
`test` uses the normal approximation only when every arm expects at least 10 conversions
and 10 non-conversions; otherwise it runs Fisher's exact test. It prints the method used.
`srm` uses chi-square when both arms expect at least 5 visitors, an exact binomial test otherwise.
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


MIN_EXPECTED = 10  # expected conversions and non-conversions per arm for the normal approximation


def check_counts(na: int, xa: int, nb: int, xb: int) -> None:
    for n, x, arm in ((na, xa, "A"), (nb, xb, "B")):
        if n <= 0:
            raise ValueError(f"arm {arm}: visitors must be > 0 (got {n})")
        if not 0 <= x <= n:
            raise ValueError(f"arm {arm}: conversions must be between 0 and visitors {n} (got {x})")


def fisher_exact(na: int, xa: int, nb: int, xb: int) -> float:
    """Two-sided Fisher exact p: sum of hypergeometric tables no more likely than the observed one."""
    n, k = na + nb, xa + xb
    def log_pmf(i: int) -> float:  # P(A has i of the k conversions), log of comb(k,i)comb(n-k,na-i)/comb(n,na)
        return (math.lgamma(k + 1) - math.lgamma(i + 1) - math.lgamma(k - i + 1)
                + math.lgamma(n - k + 1) - math.lgamma(na - i + 1) - math.lgamma(n - k - na + i + 1)
                - math.lgamma(n + 1) + math.lgamma(na + 1) + math.lgamma(nb + 1))
    observed = log_pmf(xa)
    tail = sum(math.exp(log_pmf(i)) for i in range(max(0, na - (n - k)), min(k, na) + 1)
               if log_pmf(i) <= observed + 1e-7)
    return min(1.0, tail)


def two_prop_test(na: int, xa: int, nb: int, xb: int, alpha: float = 0.05) -> dict:
    """B vs A. Pooled z-test plus unpooled CI when every arm has enough expected events,
    Fisher exact otherwise; no verdict when the pooled rate is 0% or 100%."""
    check_counts(na, xa, nb, xb)
    pa, pb = xa / na, xb / nb
    diff = pb - pa
    pool = (xa + xb) / (na + nb)
    res = {"rate_a": pa, "rate_b": pb, "abs_diff": diff,
           "rel_lift": diff / pa if pa else float("nan"),
           "ci_abs": None, "z": None, "p_value": None, "significant": False}
    if pool in (0.0, 1.0):
        res["method"] = f"none: both arms converted {pool:.0%} of visitors, insufficient data for a verdict"
        return res
    expected = min(min(n * pool, n * (1 - pool)) for n in (na, nb))
    if expected < MIN_EXPECTED:
        res["p_value"] = fisher_exact(na, xa, nb, xb)
        res["method"] = (f"Fisher exact (fewest expected events per arm {expected:.1f} < {MIN_EXPECTED}; "
                         "normal approximation and CI not used)")
    else:
        se_pool = math.sqrt(pool * (1 - pool) * (1 / na + 1 / nb))
        res["z"] = diff / se_pool
        res["p_value"] = 2 * (1 - N.cdf(abs(res["z"])))
        se = math.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb)
        zc = N.inv_cdf(1 - alpha / 2)
        res["ci_abs"] = (diff - zc * se, diff + zc * se)
        res["method"] = "two-proportion z-test (normal approximation)"
    res["significant"] = res["p_value"] < alpha
    return res


SRM_MIN_EXPECTED = 5  # expected visitors per arm for the chi-square approximation


def binom_exact(na: int, n: int, ratio_a: float) -> float:
    """Two-sided exact binomial p: sum of every outcome no more likely than na of n visitors in A."""
    def log_pmf(k: int) -> float:  # log of comb(n,k) ratio_a^k (1-ratio_a)^(n-k)
        return (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
                + k * math.log(ratio_a) + (n - k) * math.log1p(-ratio_a))
    observed = log_pmf(na)
    return min(1.0, sum(math.exp(lp) for lp in map(log_pmf, range(n + 1)) if lp <= observed + 1e-7))


def srm(na: int, nb: int, ratio_a: float = 0.5) -> dict:
    """Sample ratio check, 2 arms. Chi-square goodness of fit (1 df) when both arms expect at least
    SRM_MIN_EXPECTED visitors, exact two-sided binomial otherwise. p < 0.001 = sample ratio mismatch."""
    if na < 0 or nb < 0 or na + nb == 0 or not 0 < ratio_a < 1:
        raise ValueError("srm needs visitor counts >= 0 with a positive total, and 0 < ratio < 1")
    n = na + nb
    ea, eb = n * ratio_a, n * (1 - ratio_a)
    if min(ea, eb) < SRM_MIN_EXPECTED:
        p_value = binom_exact(na, n, ratio_a)
        return {"chi2": None, "p_value": p_value, "srm": p_value < 0.001,
                "method": f"exact binomial (fewest expected visitors per arm {min(ea, eb):.1f} < {SRM_MIN_EXPECTED})"}
    chi2 = (na - ea) ** 2 / ea + (nb - eb) ** 2 / eb
    p_value = math.erfc(math.sqrt(chi2 / 2))  # survival of chi-square with 1 df
    return {"chi2": chi2, "p_value": p_value, "srm": p_value < 0.001, "method": "chi-square"}


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
        try:
            res = two_prop_test(a.na, a.xa, a.nb, a.xb, a.alpha)
        except ValueError as e:
            ap.error(str(e))
        lift = "n/a" if math.isnan(res["rel_lift"]) else f"{res['rel_lift']:+.1%}"
        print(f"A {res['rate_a']:.4%}  B {res['rate_b']:.4%}  lift {lift}")
        print(f"method: {res['method']}")
        if res["p_value"] is None:
            print("not significant: no difference measurable, keep collecting data")
        else:
            ci = f"CI [{res['ci_abs'][0]:+.4%}, {res['ci_abs'][1]:+.4%}]  z {res['z']:.2f}  " if res["ci_abs"] else ""
            print(f"abs diff {res['abs_diff']:+.4%}  {ci}p {res['p_value']:.4f}")
            print("SIGNIFICANT" if res["significant"] else "not significant")
    else:
        try:
            res = srm(a.na, a.nb, a.ratio)
        except ValueError as e:
            ap.error(str(e))
        stat = f"chi2 {res['chi2']:.2f}" if res["chi2"] is not None else res["method"]
        print(f"{stat}  p {res['p_value']:.6f}  ->", "SRM: STOP, debug assignment" if res["srm"] else "ok")


if __name__ == "__main__":
    main()
