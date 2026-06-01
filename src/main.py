import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bond_crawler import BondCrawler
from src.utils import ensure_dir


def run(max_pages: int = 5, page_size: int = 10):
    """
    Main entry point for bond data crawling.
    
    Args:
        max_pages: 最大抓取页数（默认5页，避免运行时间过长）
        page_size: 每页记录数（默认10，避免触发反爬）
    """
    crawler = BondCrawler()

    print("Starting bond data fetch...")
    print(f"Max pages: {max_pages}, Page size: {page_size}")
    
    all_records = []
    page_no = 1
    
    while page_no <= max_pages:
        print(f"Fetching page {page_no}/{max_pages}...")
        
        try:
            records = crawler.fetch_page(page_no, page_size)
            
            if not records:
                print(f"No more records found at page {page_no}")
                break
                
            all_records.extend(records)
            print(f"Page {page_no}: {len(records)} records fetched")
            
            # 添加请求间隔，避免触发反爬
            if page_no < max_pages:
                time.sleep(1)
                
        except Exception as e:
            print(f"Error fetching page {page_no}: {e}")
            break
            
        page_no += 1

    if not all_records:
        print("No records fetched. Please verify the API endpoint and parameters.")
        return

    print(f"\nTotal records fetched: {len(all_records)}")

    rows = crawler.transform(all_records)

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    ensure_dir(output_dir)

    output_path = os.path.join(output_dir, "treasury_bond_2023.csv")
    crawler.save_csv(rows, output_path)

    print("\nCrawling completed successfully!")
    print(f"Data saved to: {output_path}")


if __name__ == "__main__":
    # 可以通过命令行参数指定最大页数和每页大小
    max_pages = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    page_size = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    run(max_pages, page_size)
