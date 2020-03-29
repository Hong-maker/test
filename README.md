#### 项目说明

- `master`分支：C端账号相关API层和服务层测试
- `internal_account`分支：内部账号、统一权限相关测试
- `release-work`分支：作品相关接口测试
- `transaction`分支：内部账号、统一交易系统相关测试

#### 测试数据准备

- config目录用于配置测试数据
- user：普通账号配置
- db：数据库配置

#### .env配置文件

- environment表示测试环境：dev、test、staging、production
- test_phone_number表示测试的手机号，主要用于测试手机号+验证码相关。建议使用自己的手机号
- geetest_v2表示极验2.0状态，on表示开启，off表示未开启

#### 依赖包

- python版本：3.6+
- 安装所有依赖包：`pip install -r requirements.txt`

#### 运行脚本

1. `.env`文件中指定测试环境和配置测试手机号
2. 运行如下命令

```sh
# 运行某目录下的所有测试用例，选择运行环境为dev
hrun testcases/account-api --dot-env-path=dev.env

# 运行某个测试用例文件
hrun testcases/account-api/v1/login.yml --dot-env-path=dev.env

# 指定html报告的路径和名称
hrun testcases/account-api --html-report-name reports/result.html --dot-env-path=dev.env

# 自定义报告模板。默认使用：~\httprunner\templates\report_template.html
hrun testcases/account-api/v1/login.yml --report-template=templates/report_fail_only.html --dot-env-path=dev.env
hrun testcases/account-api/v1/login.yml --report-template=templates/extent_reports.html --dot-env-path=dev.env # 引入extent reports
```