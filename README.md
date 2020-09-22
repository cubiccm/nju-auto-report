# nju-auto-report
NJU每日健康打命令

Usage: 
```
python3 nju-auto-report.py [-l location] [-a auth-string] [-s] [-f] [-h]
  -l  --location  Specify the location of report.
  -a  --auth  --auth-string  Set the authentication string for login.
  -s  --scan-only  Scan for reports without submitting automatically.
  -f  --force-rewrite  Submit reports without skipping filled ones.
  -h  --help  Show this help.
```

用法：
```
python3 nju-auto-report-cn.py [-l location] [-a auth-string] [-s] [-f] [-h]
  -l  --location  设定打卡位置
  -a  --auth  --auth-string  设定登录认证串
  -s  --scan-only  只读模式，不会自动打卡
  -f  --force-rewrite  强制打卡，不会略过已经打卡的项目
  -h  --help  显示帮助
```

需要获取“登录认证串”，可通过访问 http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do 获取MOD_AUTH_CAS对应的Cookie值（按 F12 或 Option-Command-I 进入开发者工具，点击Application一栏，查看对应的值）。
