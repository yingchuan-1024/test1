# run_crawler.py - 简化版运行脚本
import os

# 清除代理环境变量
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

import requests
import pandas as pd

def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://www.chinamoney.com.cn/english/bdInfo/',
        'Origin': 'https://www.chinamoney.com.cn'
    }

    session = requests.Session()
    session.trust_env = False
    
    # 先访问主页面获取cookie
    session.get('https://www.chinamoney.com.cn/english/bdInfo/', headers=headers, timeout=30)
    
    all_records = []
    page_no = 1
    page_size = 50
    
    while True:
        url = f'https://www.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN?pageNo={page_no}&pageSize={page_size}&bondTypeCode=100001&issueYear=2023'
        response = session.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            break
        
        data = response.json()
        records = data.get('data', {}).get('resultList', [])
        
        if not records:
            break
        
        all_records.extend(records)
        page_no += 1

    # 转换并保存
    if all_records:
        df = pd.DataFrame(all_records)
        df = df[['isin', 'bondCode', 'entyFullName', 'bondType', 'issueStartDate', 'debtRtng']]
        df.columns = ['ISIN', 'Bond Code', 'Issuer', 'Bond Type', 'Issue Date', 'Latest Rating']
        os.makedirs('output', exist_ok=True)
        df.to_csv('output/treasury_bond_2023.csv', index=False, encoding='utf-8-sig')
        print(f'Success! Total records: {len(all_records)}')
    else:
        print('No records found')

if __name__ == '__main__':
    main()
