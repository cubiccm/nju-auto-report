# Customize your default settings below
# Example:
'''
auth_string = "MOD_AUTH_ST-xxxxxxxxxxx-cas"
report_location = "中华人民共和国"
'''
auth_string = None
report_location = None
# Customize your default settings above

def showHelp():
  print("nju-auto-report Version 1.0")
  print("Usage: ")
  print("  python3 nju-auto-report.py [-l location] [-a auth-string] [-s] [-f] [-h]", end = "\n\n")
  print("  -l  --location  Specify the location of report.")
  print("  -a  --auth  --auth-string  Set the authentication string for login.")
  print("  -s  --scan-only  Scan for reports without submitting automatically.")
  print("  -f  --force-rewrite  Submit reports without skipping filled ones.")
  print("  -h  --help  Show this help.")

def getAuthString():
  print("Please open the following link in your browser: ")
  print("http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do")
  input("Press Enter to continue...")
  print("Log into your account if required, then check the \"Application\" panel in developer tools (F12 or Option-Command-I)")
  print("Expand \"Cookies\" in the sidebar, then select the website.")
  print("Copy the value of MOD_AUTH_CAS (starting with MOD_AUTH_ST) and paste here:")

import sys, getopt

def showSubmitResult(r, f, t):
  if f:
    if r:
      printStatus("rewrite success", t)
    else:
      printStatus("rewrite failed", t)
  if r:
    printStatus("success", t)
  else:
    printStatus("failed", t)

def printStatus(r, t):
  print(" ...%s (%s)" % (r, t))

def main(auth_string, report_location, scan_only = False, force_rewrite = False):
  if auth_string == None or auth_string == "":
    print("If you have the authentication string (start with MOD_AUTH_ST), please input below; to get the authentication string, just press Enter.")
    auth_string = input()
    while auth_string == None or auth_string == "":
      getAuthString()
      auth_string = input()
  if report_location == None and scan_only == False:
    print("Please input the location below (optional):")
    report_location = input()

  import requests, json

  query_url = "http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do"
  submit_url = "http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do"

  # Send query request
  login_cookies = dict(MOD_AUTH_CAS = auth_string)
  try:
    query_request = requests.get(query_url, cookies = login_cookies)
  except:
    raise Exception("Failed to fetch data from ehallapp.nju.edu.cn .")
  try:
    report_info = json.loads(query_request.text)
  except:
    raise Exception("Failed to parse data. There may be problems in your login information.")

  if not 'data' in report_info:
    raise Exception("Failed to parse data: no reports found.")

  print(str(len(report_info['data'])) + " report(s) found.")
  user_id_showed = False

  # Traverse all reports
  for item in report_info['data']:
    if user_id_showed == False and 'USER_ID' in item:
      print("User ID: " + item['USER_ID'])
      user_id_showed = True
    report_id = item['WID']
    print("Report ID: " + report_id, end = '')

    is_report_filled = ('TJSJ' in item and item['TJSJ'] != '');
    time_detail = ""
    if 'TBRQ' in item:
      time_detail = 'Date: ' + item['TBRQ']
    if is_report_filled:
      time_detail = time_detail + ' Last Fill: ' + item['TJSJ']

    if scan_only:
      if is_report_filled:
        printStatus("filled", time_detail)
      else:
        printStatus("not filled", time_detail)
      continue
    if force_rewrite == False and is_report_filled:
      printStatus("skipped", time_detail)
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
      showSubmitResult(False, force_rewrite and is_report_filled, time_detail)
    else:
      try:
        submit_info = json.loads(submit_request.text)
      except:
        showSubmitResult(False, force_rewrite and is_report_filled, time_detail)
      else:
        if "msg" in submit_info and submit_info["msg"] == "成功":
          showSubmitResult(True, force_rewrite and is_report_filled, time_detail)
        else:
          showSubmitResult(False, force_rewrite and is_report_filled, time_detail)

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




