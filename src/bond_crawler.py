import os

# 在导入requests之前清除代理环境变量
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)

import requests
import pandas as pd
from typing import List, Dict


class BondCrawler:
    """
    债券数据爬虫类
    
    从中国货币网获取债券数据，支持自动分页、数据转换和CSV导出
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.chinamoney.com.cn/english/bdInfo/',
            'Origin': 'https://www.chinamoney.com.cn'
        }
        self.session = requests.Session()
        self.session.trust_env = False
    
    def _initialize_session(self) -> None:
        """
        初始化会话：先访问主页面获取必要的cookie和状态
        """
        try:
            self.session.get('https://www.chinamoney.com.cn/english/bdInfo/', headers=self.headers, timeout=30)
            print('Session initialized successfully')
        except Exception as e:
            print(f'Warning: Failed to initialize session: {e}')
    
    def fetch_page(self, page_no: int, page_size: int = 50, bond_type_code: str = '100001', issue_year: str = '2023') -> List[Dict]:
        """
        获取单页债券数据
        
        Args:
            page_no: 页码
            page_size: 每页记录数
            bond_type_code: 债券类型代码
            issue_year: 发行年份
        
        Returns:
            债券记录列表
        """
        url = f'https://www.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN?pageNo={page_no}&pageSize={page_size}&bondTypeCode={bond_type_code}&issueYear={issue_year}'
        
        try:
            resp = self.session.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return data.get('data', {}).get('resultList', [])
        except requests.exceptions.HTTPError as e:
            print(f'HTTP Error fetching page {page_no}: {e}')
            return []
        except Exception as e:
            print(f'Error fetching page {page_no}: {e}')
            return []
    
    def fetch_all(self, bond_type_code: str = '100001', issue_year: str = '2023') -> List[Dict]:
        """
        获取所有债券数据（自动分页）
        
        Args:
            bond_type_code: 债券类型代码
            issue_year: 发行年份
        
        Returns:
            所有债券记录列表
        """
        self._initialize_session()
        
        all_records = []
        page_no = 1
        
        while True:
            records = self.fetch_page(page_no, bond_type_code=bond_type_code, issue_year=issue_year)
            if not records:
                break
            all_records.extend(records)
            print(f'Page {page_no}: {len(records)} records')
            page_no += 1
        
        return all_records
    
    def transform(self, records: List[Dict]) -> List[Dict]:
        """
        转换数据格式
        
        Args:
            records: 原始债券记录列表
        
        Returns:
            转换后的记录列表，包含指定字段
        """
        rows = []
        for item in records:
            row = {
                'ISIN': item.get('isin', ''),
                'Bond Code': item.get('bondCode', ''),
                'Issuer': item.get('entyFullName', ''),
                'Bond Type': item.get('bondType', ''),
                'Issue Date': item.get('issueStartDate', ''),
                'Latest Rating': item.get('debtRtng', '')
            }
            rows.append(row)
        return rows
    
    def save_csv(self, rows: List[Dict], path: str) -> None:
        """
        保存数据为CSV文件
        
        Args:
            rows: 记录列表
            path: CSV文件路径
        """
        df = pd.DataFrame(rows)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False, encoding='utf-8-sig')
        print(f'Data saved to {path}')


def fetch_bond_data(bond_type_code='100001', issue_year='2023') -> pd.DataFrame:
    """
    从中国货币网获取债券数据（函数式接口）
    
    Args:
        bond_type_code: 债券类型代码 (Treasury Bond = 100001)
        issue_year: 发行年份
    
    Returns:
        DataFrame: 包含ISIN, Bond Code, Issuer, Bond Type, Issue Date, Latest Rating的数据集
    """
    crawler = BondCrawler()
    records = crawler.fetch_all(bond_type_code, issue_year)
    rows = crawler.transform(records)
    return pd.DataFrame(rows)


def main():
    """
    主函数：执行债券数据抓取
    """
    print('Fetching bond data...')
    df = fetch_bond_data()
    print(f'Total records: {len(df)}')
    
    # 保存CSV
    output_path = 'output/treasury_bond_2023.csv'
    os.makedirs('output', exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f'Data saved to {output_path}')
    
    # 显示前5条记录
    print('\nSample data:')
    print(df.head())


if __name__ == '__main__':
    main()
