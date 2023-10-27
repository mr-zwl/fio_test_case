import os

# 获取文件列表
file_list = [file for file in os.listdir() if "_randrw_" in file]
#file_list = [file for file in os.listdir() if "_rw_" in file]

# 初始化匹配文件总数的计数器
matched_file_count = 0

# 初始化列标题
header = "IO_Size(k), IO_Size_Convert(k), IO_Type, Jobs, IO_Depth, Read_IOPS, Read_BW(MiB/s), Read_Avg_Latency(usec), Read_99.00th_Latency(usec), Read_99.90th_Latency(usec), Write_IOPS, Write_BW(MiB/s), Write_Avg_Latency(usec), Write_99.00th_Latency(usec), Write_99.90th_Latency(usec)"

# 遍历文件列表，找到每列的最大宽度
max_column_widths = [len(column) for column in header.split(", ")]

# 用于存储结果行的列表
result_rows = []

print(header)
# 遍历文件列表
for file_name in file_list:
    # 从文件名中提取信息
    file_name_parts = file_name.split("_")
    if len(file_name_parts) == 7:

        jobs = file_name_parts[2]
        io_depth= file_name_parts[3]
        io_type = file_name_parts[4]
        read_percentage = file_name_parts[5]
        io_size = file_name_parts[6]
        # 仅保留k.log前面的数字
        io_size_convert = io_size.split(".")[0]
        io_size_convert = ''.join(filter(str.isdigit, io_size))

        #print(io_size, io_type, jobs, io_depth, read_percentage)

        # 读取文件内容
        with open(file_name, 'r') as file:
            content = file.read()

            # 提取读取和写入的信息
            read_iops_start = content.find("read: IOPS=")
            if read_iops_start != -1:
                content = content[read_iops_start:]
                read_iops_end = content.find(",")
                if read_iops_end != -1:
                    read_iops = content[11:read_iops_end]
                    content = content[read_iops_end+1:]
                    read_iops_convert = read_iops
                    if 'k' in read_iops:
                        read_iops_convert = str(float(read_iops.replace('k', '')) * 1000)

            read_bw_start = content.find("BW=")
            if read_bw_start != -1:
                content = content[read_bw_start:]
                read_bw_end = content.find("(")
                if read_bw_end != -1:
                    read_bw = content[3:read_bw_end]
                    content = content[read_bw_end+1:]
                    # 删除MiB/s并保留前面的数字
                    read_bw = read_bw.replace("MiB/s", "").strip()
            
            read_slat_agv_latency = content.find("avg=")
            if read_slat_agv_latency != -1:
                content = content[read_slat_agv_latency:]
                read_slat_agv_latency_end = content.find(",")
                if read_slat_agv_latency_end != -1:
                    read_slat_agv_latency = content[4:read_slat_agv_latency_end]
                    content = content[read_slat_agv_latency_end:]
            
            read_clat_avg_latency = content.find("avg=")
            if read_clat_avg_latency != -1:
                content = content[read_clat_avg_latency:]
                read_clat_avg_latency_end = content.find(",")
                if read_clat_avg_latency_end != -1:
                    read_clat_avg_latency = content[4:read_clat_avg_latency_end]
                    content = content[read_clat_avg_latency_end+1:]

            read_clat_99_00_latency = content.find("99.00th=[")
            if read_clat_99_00_latency != -1:
                content = content[read_clat_99_00_latency+1:]
                read_clat_99_00_latency_end = content.find("]")
                if read_clat_99_00_latency_end != -1:
                    read_clat_99_00_latency = content[8:read_clat_99_00_latency_end]
                    content = content[read_clat_99_00_latency_end+1:]
            
            read_clat_99_90_latency = content.find("99.90th=[")
            if read_clat_99_90_latency != -1:
                content = content[read_clat_99_90_latency+1:]
                read_clat_99_90_latency_end = content.find("]")
                if read_clat_99_90_latency_end != -1:
                    read_clat_99_90_latency = content[8:read_clat_99_90_latency_end]
                    content = content[read_clat_99_90_latency_end+1:]

            write_iops_start = content.find("write: IOPS=")
            if write_iops_start != -1:
                content = content[write_iops_start:]
                write_iops_end = content.find(",")
                if write_iops_end != -1:
                    write_iops = content[12:write_iops_end]
                    content = content[write_iops_end+1:]
                    write_iops_convert = write_iops
                    if 'k' in write_iops:
                        write_iops_convert = str(float(write_iops.replace('k', '')) * 1000)
            
            write_bw_start = content.find("BW=")
            if write_bw_start != -1:
                content = content[write_bw_start:]
                write_bw_end = content.find("(")
                if write_bw_end != -1:
                    write_bw = content[3:write_bw_end]
                    content = content[write_bw_end+1:]
                    # 删除MiB/s并保留前面的数字
                    write_bw = write_bw.replace("MiB/s", "").strip()

            write_slat_agv_latency = content.find("avg=")
            if write_slat_agv_latency != -1:
                content = content[write_slat_agv_latency:]
                write_slat_agv_latency_end = content.find(",")
                if write_slat_agv_latency_end != -1:
                    write_slat_agv_latency = content[4:write_slat_agv_latency_end]
                    content = content[write_slat_agv_latency_end+1:]

            write_clat_avg_latency = content.find("avg=")
            if write_clat_avg_latency != -1:
                content = content[write_clat_avg_latency:]
                write_clat_avg_latency_end = content.find(",")
                if write_clat_avg_latency_end != -1:
                    write_clat_avg_latency = content[4:write_clat_avg_latency_end]
                    content = content[write_clat_avg_latency_end+1:]

            write_clat_99_00_latency = content.find("99.00th=[")
            if write_clat_99_00_latency != -1:
                content = content[write_clat_99_00_latency+1:]
                write_clat_99_00_latency_end = content.find("]")
                if write_clat_99_00_latency_end != -1:
                    write_clat_99_00_latency = content[8:write_clat_99_00_latency_end]
                    content = content[write_clat_99_00_latency_end+1:]

            write_clat_99_90_latency = content.find("99.90th=[")
            if write_clat_99_90_latency != -1:
                content = content[write_clat_99_90_latency+1:]
                write_clat_99_90_latency_end = content.find("]")
                if write_clat_99_90_latency_end != -1:
                    write_clat_99_90_latency = content[8:write_clat_99_90_latency_end]
                    content = content[write_clat_99_90_latency_end+1:]
            
            # 统计文件数
            matched_file_count += 1
            
            # 与header对应打印
            # IO_Size_Convert(k), IO_Size(k), IO_Type, Jobs, IO_Depth, Read_IOPS, Read_BW(MiB/s), Read_Avg_Latency(usec), Read_99.00th_Latency(usec), Read_99.90th_Latency(usec), Write_IOPS, Write_BW(MiB/s), Write_Avg_Latency(usec), Write_99.00th_Latency(usec), Write_99.90th_Latency(usec)
            # 使用字符串格式化，确保对齐
            row = "{:<10}, {:<10}, {:<8}, {:<6}, {:<9}, {:<9}, {:<12}, {:<19}, {:<19}, {:<19}, {:<9}, {:<12}, {:<19}, {:<19}, {:<19}".format(
                io_size, io_size_convert, io_type, jobs, io_depth, read_iops_convert, read_bw, read_clat_avg_latency, read_clat_99_00_latency, read_clat_99_90_latency, write_iops_convert, write_bw, write_clat_avg_latency, write_clat_99_00_latency, write_clat_99_90_latency
            )
            
            print(row)


# 打印匹配到的文件总数
print(f"Total matched files: {matched_file_count}")
