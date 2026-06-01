import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bond_crawler import BondCrawler
from src.utils import ensure_dir


def run():
    """
    Main entry point for bond data crawling.
    """
    crawler = BondCrawler()

    print("Starting bond data fetch...")
    records = crawler.fetch_all()

    if not records:
        print("No records fetched. Please verify the API endpoint and parameters.")
        return

    print(f"Total records fetched: {len(records)}")

    rows = crawler.transform(records)

    output_dir = os.path.join(os.path.dirname(__file__), "output")
    ensure_dir(output_dir)

    output_path = os.path.join(output_dir, "treasury_bond_2023.csv")
    crawler.save_csv(rows, output_path)

    print("Crawling completed successfully!")


if __name__ == "__main__":
    run()
