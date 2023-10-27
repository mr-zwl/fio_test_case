# fio_test_case
fio自动化压测
# 用于压测存储集群 使用方式如下


run.sh
执行脚本，控制io深度和线程数 ， 可自行添加需要的case（即io深度和线程数）

single-disk.sh
执行 fio 的 case  



执行方式 ： 
预设文件参数调整完毕后，执行   ./run.sh  

result.py
用于读取日志数据格式化输出  
执行 ： python3 result.py 
