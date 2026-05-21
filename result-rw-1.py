import json
import os
import sys
import glob


def extract_direction_metrics(job, direction):
    stats = job[direction]
    iops = stats["iops"]
    bw_kib = stats["bw"]
    bw_mib = bw_kib / 1024.0

    clat_ns = stats["clat_ns"]
    avg_usec = clat_ns["mean"] / 1000.0

    percentiles = clat_ns.get("percentile", {})
    p99_usec = percentiles.get("99.000000", 0) / 1000.0
    p999_usec = percentiles.get("99.900000", 0) / 1000.0

    return {
        "iops": iops,
        "bw_mib": bw_mib,
        "avg_usec": avg_usec,
        "p99_usec": p99_usec,
        "p999_usec": p999_usec,
    }


def parse_json_result(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    job = data["jobs"][0]
    job_name = job["jobname"]

    parts = job_name.split("_")
    # iscsi_libaio_{numjobs}_{iodepth}_{rw}_{rwmixread}_{bs}
    if len(parts) != 7:
        return None

    _, _, numjobs, iodepth, rw, rwmixread, bs = parts

    if rw not in ("randrw", "rw"):
        return None

    read_metrics = extract_direction_metrics(job, "read")
    write_metrics = extract_direction_metrics(job, "write")

    bs_convert = bs.lower()
    if bs_convert.endswith("k"):
        bs_num = float(bs_convert[:-1])
    elif bs_convert.endswith("m"):
        bs_num = float(bs_convert[:-1]) * 1024
    else:
        bs_num = float(bs_convert) / 1024

    return {
        "bs": bs,
        "bs_num": bs_num,
        "rw": rw,
        "rwmixread": rwmixread,
        "numjobs": int(numjobs),
        "iodepth": int(iodepth),
        "read": read_metrics,
        "write": write_metrics,
    }


def main():
    search_dir = sys.argv[1] if len(sys.argv) > 1 else "."

    json_files = glob.glob(os.path.join(search_dir, "iscsi_libaio_*_*.json"))
    if not json_files:
        print("No JSON result files found.")
        return

    results = []
    for f in json_files:
        try:
            r = parse_json_result(f)
            if r:
                results.append(r)
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"Warning: failed to parse {f}: {e}", file=sys.stderr)

    if not results:
        print("No mixed RW results found.")
        return

    results.sort(key=lambda x: (x["bs_num"], x["rw"], x["numjobs"], x["iodepth"]))

    header = (
        f"{'BS':<7} {'BS(K)':<7} {'Type':<8} {'Mix':<5} {'Jobs':<5} {'Depth':<6} "
        f"{'R_IOPS':<10} {'R_BW(M)':<9} {'R_Avg(us)':<11} {'R_P99(us)':<11} {'R_P999(us)':<11} "
        f"{'W_IOPS':<10} {'W_BW(M)':<9} {'W_Avg(us)':<11} {'W_P99(us)':<11} {'W_P999(us)':<11}"
    )
    print(header)
    print("-" * len(header))

    for r in results:
        rd = r["read"]
        wr = r["write"]
        print(
            f"{r['bs']:<7} {r['bs_num']:<7.0f} {r['rw']:<8} {r['rwmixread']:<5} {r['numjobs']:<5} {r['iodepth']:<6} "
            f"{rd['iops']:<10.2f} {rd['bw_mib']:<9.2f} {rd['avg_usec']:<11.2f} {rd['p99_usec']:<11.2f} {rd['p999_usec']:<11.2f} "
            f"{wr['iops']:<10.2f} {wr['bw_mib']:<9.2f} {wr['avg_usec']:<11.2f} {wr['p99_usec']:<11.2f} {wr['p999_usec']:<11.2f}"
        )

    print(f"\nTotal: {len(results)} test(s)")


if __name__ == "__main__":
    main()
