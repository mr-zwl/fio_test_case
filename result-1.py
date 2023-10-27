import re
import os

# 获取文件列表
#file_list = [file for file in os.listdir() if "_randwrite_" in file]
# file_list = [file for file in os.listdir() if "_randread_" in file]
# file_list = [file for file in os.listdir() if "_write_" in file]
#file_list = [file for file in os.listdir() if "_read_" in file]
file_list = [file for file in os.listdir() if any(keyword in file for keyword in ["_randwrite_", "_randread_", "_write_", "_read_"])]


# 初始化匹配文件总数的计数器
matched_file_count = 0

# 初始化列标题
header = "IO_Size(k), IO_Size_Convert(k), IO_Type, Jobs, IO_Depth, IOPS, IOPS_Convert, BW(MiB/s), Avg_Latency(usec), 99.00th_Latency(usec), 99.90th_Latency(usec)"

# 遍历文件列表，找到每列的最大宽度
max_column_widths = [len(column) for column in header.split(", ")]

# 用于存储结果行的列表
result_rows = []

# 遍历文件列表
for file_name in file_list:
    # 从文件名中提取信息
    match = re.match(r'iscsi_libaio_(\d+)_(\d+)_(\w+)_(\d+[kKmMbyte]+)\.log', file_name)

    if match:
        jobs, io_depth, io_type, io_size = match.groups()

        # 读取文件内容
        with open(file_name, 'r') as file:
            content = file.read()

            # 提取IOPS、BW信息
            iops_match = re.search(r'IOPS=(\d+|\d+.\d+.*),', content)
            bw_match = re.search(r'BW=([\d.]+[KMG]iB/s)', content)
            avg_match = re.search(r'clat.*avg=(.*),', content)

            # 用更通用的正则表达式匹配百分位延迟数据
            unit = re.search(r'clat percentiles (.*):', content)
            percentile_99_match = re.search(r'99\.00th=\[\s*(\d+)\]', content)
            percentile_99_90_match = re.search(r'99\.90th=\[\s*(\d+)\]', content)

            if iops_match and bw_match and percentile_99_match and unit:
                iops = iops_match.group(1)
                bw = bw_match.group(1)

                # 从 unit 中提取匹配的文本
                unit_text = unit.group(1)

                # avg
                avg = avg_match.group(1)
                avg_latency = avg + " " + unit_text

                # 从匹配的表格中提取所需的值
                percentile_99 = percentile_99_match.group(1)
                # 加上usec单位
                percentile_99_with_unit = percentile_99 + " " + unit_text

                # 从匹配的表格中提取所需的值
                percentile_99_90 = percentile_99_90_match.group(1)
                # 加上usec单位
                percentile_99_90_with_unit = percentile_99_90 + " " + unit_text

                # 处理IOPS并添加新的IOPS_Convert列
                iops_convert = iops
                if 'k' in iops:
                    iops_convert = str(float(iops.replace('k', '')) * 1000)

                # 处理IO_Size并添加新的IO_Size_Convert列
#                io_size_convert = io_size.replace('k', '')  # 去掉 'k'
                io_size_convert = io_size
                if 'k' in io_size_convert:
                    io_size_convert = str(io_size.replace('k',''))
                elif 'm' in io_size_convert:
                    io_size_convert = str(float(io_size.replace('m','')) * 1024)
                else:
                    io_size_convert = str(float(io_size.replace('byte','')) / 1024)
                # 处理BW(MiB/s)列，只保留数字部分
                bw_match = re.search(r'([\d.]+)[KMG]iB/s', bw)
                if bw_match:
                    bw = bw_match.group(1)

                # 处理 Avg_Latency(usec)、99.00th_Latency(usec) 和 99.90th_Latency(usec) 列，只保留(usec)前面的数字部分
                avg_latency_match = re.search(r'([\d.]+) \(usec\)', avg_latency)
                if avg_latency_match:
                    avg_latency = avg_latency_match.group(1)

                percentile_99_with_unit_match = re.search(r'([\d.]+) \(usec\)', percentile_99_with_unit)
                if percentile_99_with_unit_match:
                    percentile_99_with_unit = percentile_99_with_unit_match.group(1)

                percentile_99_90_with_unit_match = re.search(r'([\d.]+) \(usec\)', percentile_99_90_with_unit)
                if percentile_99_90_with_unit_match:
                    percentile_99_90_with_unit = percentile_99_90_with_unit_match.group(1)

                # 构造结果行并对齐
                result_values = [io_size, io_size_convert, io_type, jobs, io_depth, iops, iops_convert, bw, avg_latency,
                                 percentile_99_with_unit, percentile_99_90_with_unit]
                result_line = [result_values[i].ljust(max_column_widths[i]) for i in range(len(max_column_widths))]

                # 添加结果行到结果列表
                result_rows.append(result_line)

                # 增加匹配文件总数的计数器
                matched_file_count += 1

# 根据 IO_Size_Convert、Jobs 和 IO_Depth 列对结果进行排序
result_rows.sort(key=lambda x: (float(x[1]), int(x[3]), int(x[4])))  # 这里假设新列的索引是 1，Jobs 列的索引是 3，IO_Depth 列的索引是 4

# 打印标题
print(header)

# 打印分隔线
separator = ["-" * width for width in max_column_widths]
print(", ".join(separator))

# 打印排序后的结果
for result_line in result_rows:
    print(", ".join(result_line))

# 打印匹配到的文件总数
print(f"Total matched files: {matched_file_count}")
