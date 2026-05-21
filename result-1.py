import json
import os
import sys
import glob


def parse_json_result(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    job = data["jobs"][0]
    job_name = job["jobname"]

    parts = job_name.split("_")
    # iscsi_libaio_{numjobs}_{iodepth}_{rw}_{bs}
    if len(parts) != 6:
        return None

    _, _, numjobs, iodepth, rw, bs = parts

    if rw in ("randrw", "rw"):
        return None

    if rw in ("randread", "read"):
        stats = job["read"]
    else:
        stats = job["write"]

    iops = stats["iops"]
    bw_kib = stats["bw"]
    bw_mib = bw_kib / 1024.0

    clat_ns = stats["clat_ns"]
    avg_usec = clat_ns["mean"] / 1000.0

    percentiles = clat_ns.get("percentile", {})
    p99_usec = percentiles.get("99.000000", 0) / 1000.0
    p999_usec = percentiles.get("99.900000", 0) / 1000.0

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
        "numjobs": int(numjobs),
        "iodepth": int(iodepth),
        "iops": iops,
        "bw_mib": bw_mib,
        "avg_usec": avg_usec,
        "p99_usec": p99_usec,
        "p999_usec": p999_usec,
    }


def main():
    search_dir = sys.argv[1] if len(sys.argv) > 1 else "."

    json_files = glob.glob(os.path.join(search_dir, "iscsi_libaio_*_*.json"))
    log_files = glob.glob(os.path.join(search_dir, "iscsi_libaio_*_*.log"))

    files = json_files or log_files
    if not files:
        print("No result files found.")
        return

    if json_files:
        results = []
        for f in json_files:
            try:
                r = parse_json_result(f)
                if r:
                    results.append(r)
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                print(f"Warning: failed to parse {f}: {e}", file=sys.stderr)
    else:
        print("No JSON files found. Please re-run fio with --output-format=json")
        return

    results.sort(key=lambda x: (x["bs_num"], x["rw"], x["numjobs"], x["iodepth"]))

    header = f"{'BS':<8} {'BS(K)':<8} {'IO_Type':<12} {'Jobs':<6} {'Depth':<6} {'IOPS':<12} {'BW(MiB/s)':<12} {'Avg_Lat(us)':<14} {'P99(us)':<12} {'P99.9(us)':<12}"
    print(header)
    print("-" * len(header))

    for r in results:
        print(
            f"{r['bs']:<8} {r['bs_num']:<8.0f} {r['rw']:<12} {r['numjobs']:<6} {r['iodepth']:<6} "
            f"{r['iops']:<12.2f} {r['bw_mib']:<12.2f} {r['avg_usec']:<14.2f} "
            f"{r['p99_usec']:<12.2f} {r['p999_usec']:<12.2f}"
        )

    print(f"\nTotal: {len(results)} test(s)")


if __name__ == "__main__":
    main()
