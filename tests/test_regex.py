import pytest
from src.regex_engine import RegexEngine


class TestRegexEngine:
    """
    正则引擎测试类
    """
    
    def test_normalize_date(self):
        """测试日期格式化函数"""
        assert RegexEngine.normalize_date("2023年6月2日") == "2023-06-02"
        assert RegexEngine.normalize_date("2023-06-02") == "2023-06-02"
        assert RegexEngine.normalize_date("20230602") == "2023-06-02"
        assert RegexEngine.normalize_date(("2023", "6", "2")) == "2023-06-02"
        assert RegexEngine.normalize_date(("2023", "12", "25")) == "2023-12-25"
    
    def test_reg_search_single_match(self):
        """测试单匹配提取"""
        text = "股票代码：600900.SH"
        regex_list = [{
            '代码': {
                'pattern': r'股票代码：(\d+\.\w+)',
                'group': 1
            }
        }]
        result = RegexEngine.reg_search(text, regex_list)
        assert result == [{'代码': '600900.SH'}]
    
    def test_reg_search_multi_match(self):
        """测试多匹配提取"""
        text = "日期1：2023年1月1日，日期2：2024年12月31日"
        regex_list = [{
            '日期': {
                'pattern': r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日',
                'multi': True,
                'post_process': RegexEngine.normalize_date
            }
        }]
        result = RegexEngine.reg_search(text, regex_list)
        assert result == [{'日期': ['2023-01-01', '2024-12-31']}]
    
    def test_reg_search_example_from_test(self):
        """测试题目中的示例"""
        text = '''
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债
券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
日至 2027 年 6 月 1 日止。
'''
        
        regex_list = [{
            '标的证券': {
                'pattern': r'股票代码：(\d+\.\w+)',
                'group': 1
            },
            '换股期限': {
                'pattern': r'(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日',
                'multi': True,
                'post_process': RegexEngine.normalize_date
            }
        }]
        
        result = RegexEngine.reg_search(text, regex_list)
        expected = [{
            '标的证券': '600900.SH',
            '换股期限': ['2023-06-02', '2027-06-01']
        }]
        assert result == expected
    
    def test_reg_search_no_match(self):
        """测试无匹配情况"""
        text = "这是一段没有匹配内容的文本"
        regex_list = [{
            '代码': {
                'pattern': r'股票代码：(\d+\.\w+)',
                'group': 1
            }
        }]
        result = RegexEngine.reg_search(text, regex_list)
        assert result == [{'代码': ''}]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
