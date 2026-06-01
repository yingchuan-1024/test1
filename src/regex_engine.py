import re
from typing import List, Dict, Any, Optional, Callable


class RegexEngine:
    """
    自定义正则匹配引擎
    支持多字段提取、后处理函数、日期格式化等功能
    """
    
    @classmethod
    def normalize_date(cls, date_input: Any) -> str:
        """
        日期格式化函数：将各种日期格式统一为 YYYY-MM-DD
        
        Args:
            date_input: 原始日期数据，可以是字符串或元组
        
        Returns:
            格式化后的日期字符串 YYYY-MM-DD
        """
        if not date_input:
            return ""
        
        # 如果是元组（多捕获组），提取年、月、日
        if isinstance(date_input, tuple) and len(date_input) >= 3:
            year = str(date_input[0])
            month = str(date_input[1]).zfill(2)
            day = str(date_input[2]).zfill(2)
            return f"{year}-{month}-{day}"
        
        # 如果是字符串
        date_str = str(date_input)
        
        # 移除空白字符
        date_str = ''.join(date_str.split())
        
        # 匹配各种日期格式
        patterns = [
            r'(\d{4})[年/-](\d{1,2})[月/-](\d{1,2})[日号]?',  # 2023年6月2日 或 2023-06-02
            r'(\d{4})(\d{2})(\d{2})',  # 20230602
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',  # 2023年6月2日
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_str)
            if match:
                year = match.group(1)
                month = match.group(2).zfill(2)
                day = match.group(3).zfill(2)
                return f"{year}-{month}-{day}"
        
        return date_str
    
    @classmethod
    def reg_search(cls, text: str, regex_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        自定义正则匹配函数
        
        Args:
            text: 需要正则匹配的文本内容
            regex_list: 正则表达式配置列表
                每个配置项是一个字典，key为字段名，value为匹配规则配置
                匹配规则配置可以是：
                - 字符串：直接作为正则表达式
                - 字典：包含以下字段
                    pattern: 正则表达式模式
                    group: 捕获组索引，默认为1
                    multi: 是否匹配多个结果，默认为False
                    post_process: 后处理函数
        
        Returns:
            匹配到的结果列表
        """
        result = []
        
        for config in regex_list:
            item_result = {}
            
            for field, rule in config.items():
                # 解析规则配置
                if isinstance(rule, str):
                    pattern = rule
                    group = 1
                    multi = False
                    post_process = None
                elif isinstance(rule, dict):
                    pattern = rule.get('pattern', '')
                    group = rule.get('group', 1)
                    multi = rule.get('multi', False)
                    post_process = rule.get('post_process')
                else:
                    continue
                
                if not pattern:
                    continue
                
                try:
                    if multi:
                        # 匹配多个结果
                        matches = re.findall(pattern, text)
                        if matches:
                            # 应用后处理函数
                            if post_process and callable(post_process):
                                values = [post_process(match) for match in matches]
                            else:
                                values = list(matches)
                            
                            item_result[field] = values
                        else:
                            item_result[field] = []
                    else:
                        # 匹配单个结果
                        match = re.search(pattern, text)
                        if match:
                            value = match.group(group) if group <= len(match.groups()) + 1 else ''
                            
                            # 应用后处理函数
                            if post_process and callable(post_process):
                                value = post_process(value)
                            
                            item_result[field] = value
                        else:
                            item_result[field] = ''
                except Exception as e:
                    print(f'Error matching {field}: {e}')
                    item_result[field] = ''
            
            if item_result:
                result.append(item_result)
        
        return result


# 示例使用
if __name__ == '__main__':
    text = '''
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债
券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
日至 2027 年 6 月 1 日止。
'''
    
    # 定义正则规则
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
    
    # 执行匹配
    result = RegexEngine.reg_search(text, regex_list)
    print('匹配结果：')
    print(result)
