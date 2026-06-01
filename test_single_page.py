# test_single_page.py - 测试单页抓取
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
    session.get('https://www.chinamoney.com.cn/english/bdInfo/', headers=headers, timeout=30)

    # 只抓取第一页
    url = 'https://www.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN?pageNo=1&pageSize=10&bondTypeCode=100001&issueYear=2023'
    response = session.get(url, headers=headers, timeout=30)
    
    print(f'Response status: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        records = data.get('data', {}).get('resultList', [])
        print(f'Records found: {len(records)}')
        
        if records:
            # 创建DataFrame
            df = pd.DataFrame(records)
            print(f'DataFrame shape: {df.shape}')
            print(f'Columns: {df.columns.tolist()}')
            
            # 选择需要的列
            selected = df[['isin', 'bondCode', 'entyFullName', 'bondType', 'issueStartDate', 'debtRtng']]
            selected.columns = ['ISIN', 'Bond Code', 'Issuer', 'Bond Type', 'Issue Date', 'Latest Rating']
            
            # 保存CSV
            os.makedirs('output', exist_ok=True)
            selected.to_csv('output/treasury_bond_2023.csv', index=False, encoding='utf-8-sig')
            print('CSV saved successfully!')
            
            # 打印前3行
            print('\nSample data:')
            print(selected.head(3))
        else:
            print('No records found!')
    else:
        print(f'Failed to fetch data: {response.status_code}')

if __name__ == '__main__':
    main()
