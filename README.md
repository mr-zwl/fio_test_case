# fio_test_case

fio 自动化压测工具，用于压测存储集群（iSCSI 块设备等）。

## 依赖

- fio
- python3

## 文件说明

| 文件 | 说明 |
|------|------|
| `run.sh` | 主入口，遍历多组 iodepth/numjobs 组合调用 single-disk.sh，最后自动解析结果 |
| `single-disk.sh` | 核心压测脚本，执行 fio 测试并输出 JSON 格式结果 |
| `result-1.py` | 解析纯读/纯写测试结果（randwrite/randread/write/read） |
| `result-rw-1.py` | 解析混合读写测试结果（randrw/rw） |

## 快速开始

```bash
# 使用默认设备 /dev/cbd3
./run.sh

# 指定设备
FILE_NAME=/dev/sdb ./run.sh
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `FILE_NAME` | `/dev/cbd3` | 测试目标块设备 |
| `IODEPTH` | 由 run.sh 控制 | IO 队列深度 |
| `NUMJOBS` | 由 run.sh 控制 | 并发线程数 |
| `RUNTIME` | `90` | 每个测试运行时长（秒） |
| `RAMP_TIME` | `10` | 预热时间（秒），不计入统计 |
| `COOLDOWN` | `5` | 测试间冷却时间（秒） |

## 测试矩阵

**IO 模式**：randwrite, randread, write, read, randrw (70% read), rw (70% read)

**块大小**：4k, 8k, 16k, 32k, 64k, 128k

**默认 iodepth:numjobs 组合**（可在 run.sh 中修改 CASES 数组）：

```
1:1  2:2  4:4  8:4  16:4  8:8  16:8  32:8
```

每轮 36 个测试，8 轮共 288 个测试。

## 单独使用 single-disk.sh

```bash
IODEPTH=16 NUMJOBS=4 FILE_NAME=/dev/sdb ./single-disk.sh
```

## 解析结果

测试完成后 run.sh 会自动调用解析脚本。也可以手动执行：

```bash
# 解析当前目录下的结果
python3 result-1.py
python3 result-rw-1.py

# 解析指定目录
python3 result-1.py /path/to/results
python3 result-rw-1.py /path/to/results
```

## 自定义测试组合

编辑 `run.sh` 中的 `CASES` 数组：

```bash
CASES=(
    "1:1"
    "4:4"
    "16:8"
    "32:16"
)
```

格式为 `iodepth:numjobs`。
