# fio_test_case

fio 自动化压测工具，用于压测存储集群（iSCSI 块设备等）。

## 依赖

- fio
- python3
- docker（可选，用于容器化测试）

## 文件说明

| 文件 | 说明 |
|------|------|
| `run.sh` | 主入口，遍历多组 iodepth/numjobs 组合调用 single-disk.sh，最后自动解析结果 |
| `single-disk.sh` | 核心压测脚本，执行 fio 测试并输出 JSON 格式结果 |
| `result-1.py` | 解析纯读/纯写测试结果（randwrite/randread/write/read） |
| `result-rw-1.py` | 解析混合读写测试结果（randrw/rw） |
| `docker-test.sh` | Docker 黑盒测试脚本，用小参数快速验证整个流程 |
| `Dockerfile` | 构建包含 fio + python3 的测试镜像 |
| `.env.example` | 环境变量配置示例，复制为 `.env` 后修改 |

## 快速开始

```bash
# 1. 复制配置文件并按需修改
cp .env.example .env

# 2. 编辑 .env 设置测试参数
vim .env

# 3. 执行压测
./run.sh
```

`run.sh` 启动时会自动加载同目录下的 `.env` 文件。也可以不使用 `.env`，直接通过命令行传参：

```bash
# 指定设备
FILE_NAME=/dev/sdb ./run.sh

# 指定普通文件（非块设备，自动关闭 direct IO）
FILE_NAME=/tmp/fio_testfile ./run.sh
```

命令行传入的环境变量优先级高于 `.env` 文件。

## 环境变量

所有参数均可通过 `.env` 文件或命令行环境变量配置：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `FILE_NAME` | `/dev/cbd3` | 测试目标，支持块设备或普通文件路径 |
| `CASES` | `1:1 2:2 4:4 8:4 16:4 8:8 16:8 32:8` | iodepth:numjobs 组合，空格分隔 |
| `SIZE` | `260g` | fio 测试文件大小 |
| `RUNTIME` | `90` | 每个测试运行时长（秒） |
| `RAMP_TIME` | `10` | 预热时间（秒），不计入统计 |
| `COOLDOWN` | `5` | 测试间冷却时间（秒） |

## 测试矩阵

**IO 模式**：randwrite, randread, write, read, randrw (70% read), rw (70% read)

**块大小**：4k, 8k, 16k, 32k, 64k, 128k

每轮 36 个测试（4 种纯 IO × 6 种块大小 + 2 种混合 IO × 6 种块大小），默认 8 轮共 288 个测试。

## 自定义测试组合

通过环境变量 `CASES` 覆盖，格式为 `iodepth:numjobs`，空格分隔：

```bash
CASES="1:1 4:4 16:8" ./run.sh
```

## 单独使用 single-disk.sh

```bash
IODEPTH=16 NUMJOBS=4 FILE_NAME=/dev/sdb ./single-disk.sh
```

## 解析结果

测试完成后 `run.sh` 会自动调用解析脚本，也可以手动执行：

```bash
# 解析当前目录下的 JSON 结果
python3 result-1.py
python3 result-rw-1.py

# 解析指定目录
python3 result-1.py /path/to/results
python3 result-rw-1.py /path/to/results
```

## Docker 测试

无需真实块设备，使用 Docker 容器 + 普通文件快速验证整个流程：

```bash
./docker-test.sh
```

默认使用小参数（SIZE=64m, RUNTIME=3s, 2 组 CASES），约 5 分钟完成 72 个测试并输出解析结果。

也可以手动调整参数运行：

```bash
docker build -t fio-test .
docker run --rm \
    -e FILE_NAME=/tmp/fio_testfile \
    -e SIZE=128m \
    -e RUNTIME=10 \
    -e RAMP_TIME=3 \
    -e COOLDOWN=2 \
    -e CASES="1:1 4:4 8:8" \
    fio-test /test/run.sh
```
