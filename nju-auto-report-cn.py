# 您可以在下方自定义默认设置
# 样例：
'''
auth_string = "MOD_AMP_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
report_location = "中华人民共和国"
'''
auth_string = None
report_location = None
# 您可以在上方自定义默认设置

def showHelp():
  print("nju-auto-report Version 1.0 zh-CN")
  print("用法：")
  print("  python3 nju-auto-report-cn.py [-l location] [-a auth-string] [-s] [-f] [-h]", end = "\n\n")
  print("  -l  --location  设定打卡位置")
  print("  -a  --auth  --auth-string  设定登录认证串")
  print("  -s  --scan-only  只读模式，不会自动打卡")
  print("  -f  --force-rewrite  强制打卡，不会略过已经打卡的项目")
  print("  -h  --help  显示帮助")

def getAuthString():
  print("请在浏览器中打开一下链接：")
  print("http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do")
  input("按Enter键继续...")
  print("登录你的账号（如果需要的话），然后在开发者工具（按F12 或 Option-Command-I 打开）中转至“Application”一栏")
  print("展开侧边栏中的“Cookies”，然后选中网站。")
  print("复制MOD_AMP_AUTH的对应值（以MOD_AMP开头），然后粘贴到这里：")

import sys, getopt

def main(auth_string, report_location, scan_only = False, force_rewrite = False):
  if auth_string == None or auth_string == "":
    print("如果你有以MOD_AMP开头的登录认证串，请在下方输入；如没有，请直接按Enter。")
    auth_string = input()
    while auth_string == None or auth_string == "":
      getAuthString()
      auth_string = input()
  if report_location == None:
    print("请输入打卡地点（可选）：")
    report_location = input()

  import requests, json

  query_url = "http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do"
  submit_url = "http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do"

  # Send query request
  login_cookies = dict(MOD_AMP_AUTH = auth_string)
  try:
    query_request = requests.get(query_url, cookies = login_cookies)
  except:
    raise Exception("无法从 ehallapp.nju.edu.cn 取得数据.")
  try:
    report_info = json.loads(query_request.text)
  except:
    raise Exception("无法解析数据，请检查您的登录认证串。")

  if not 'data' in report_info:
    raise Exception("无法解析数据：未发现打卡报告。")

  print("找到 " + str(len(report_info['data'])) + " 份报告。")
  user_id_showed = False

  # Traverse all reports
  for item in report_info['data']:
    if user_id_showed == False and 'USER_ID' in item:
      print("用户ID: " + item['USER_ID'])
      user_id_showed = True
    report_id = item['WID']
    print("报告ID: " + report_id, end = '')

    is_report_filled = ('TJSJ' in item and item['TJSJ'] != '');
    if scan_only:
      if is_report_filled:
        print("  ...已填写（" + item['TJSJ'] + "）")
      else:
        print("  ...未填写")
      continue
    if force_rewrite == False and is_report_filled:
      print("  ...跳过（" + item['TJSJ'] + "）")
      continue
    payload = {
      'WID': report_id,
      'CURR_LOCATION' : report_location,
      'IS_TWZC' : 1,
      'IS_HAS_JKQK' : 1,
      'JRSKMYS' : 1,
      'JZRJRSKMYS' : 1
    }
    try:
      submit_request = requests.get(submit_url, cookies = login_cookies, params = payload)
    except:
      if force_rewrite:
        print("  ...重新打卡失败")
      else:
        print("  ...失败")
    else:
      if force_rewrite:
        print("  ...重新打卡成功")
      else:
        print("  ...成功")

if __name__ == "__main__":
  scan_only = False
  force_rewrite = False
  opts, arg = getopt.getopt(sys.argv[1:], '-s-f-l:-a:-h', ['scan-only', 'force-rewrite', 'location=', 'auth-string=', 'auth=', 'help'])
  for opt_name, opt_value in opts:
    if opt_name in ('-s', '--scan-only'):
      scan_only = True
    if opt_name in ('-f', '--force-rewrite'):
      force_rewrite = True
    if opt_name in ('-l', '--location'):
      report_location = opt_value
    if opt_name in ('-a', '--auth-string', '--auth'):
      auth_string = opt_value
    if opt_name in ('-h', '--help'):
      showHelp()
      exit()

  main(
    auth_string = auth_string,
    report_location = report_location,
    scan_only = scan_only,
    force_rewrite = force_rewrite
  )




