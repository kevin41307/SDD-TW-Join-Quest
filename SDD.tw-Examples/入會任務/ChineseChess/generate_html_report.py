#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成 Behave HTML 報告的腳本
"""
import sys
import os

# 確保 behave_html_formatter 被載入
try:
    import behave_html_formatter
except ImportError:
    print("錯誤: 請先安裝 behave-html-formatter: pip install behave-html-formatter")
    sys.exit(1)

from behave import __main__ as behave_main

if __name__ == "__main__":
    # 確保 reports 目錄存在
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # 設定命令行參數
    report_file = os.path.join(reports_dir, "behave_report.html")
    
    # 執行 behave 並生成 HTML 報告
    # 使用 behave_html_formatter.html 格式
    sys.argv = [
        "behave",
        "-f", "behave_html_formatter:HTMLFormatter",
        "-o", report_file
    ]
    
    try:
        behave_main.main()
        print(f"\n報告已生成: {report_file}")
    except SystemExit as e:
        # behave 會以 SystemExit 退出，這是正常的
        if os.path.exists(report_file):
            print(f"\n報告已生成: {report_file}")
        else:
            print(f"\n警告: 報告檔案未生成")
            sys.exit(e.code)

