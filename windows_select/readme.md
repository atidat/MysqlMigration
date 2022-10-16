## Description
基于MySQL v8.0.25的Windows版本的全量数据迁移方案，通过配置主从机系统登录和db登录信息，一键迁移数据。基于select into outfile && load load local infile实现。



## Precondition
Python V3.10、paramiko、pymysql和主从机免密登录



## Features
1. 支持生成自定义数据库和全表映射关系
2. 支持建数据库和数据表
3. 支持全表数据的导出
4. 支持全表数据的导入



## TODO
1. 解决bugs
2. 性能测试、分析与提高
3. 保证资源回收可靠性
4. 支持跨平台
5. 支持迁移过程选择（即省略流程中的前置步骤）
6. 支持主、从机备份文件免密传输
7. 支持回滚
8. 支持增量同步
9. 日志打印
10. 测试代码
11. 定义状态码
12. 打包成二进制
