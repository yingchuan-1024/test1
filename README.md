# Bond Data Crawler Project

债券数据抓取与正则解析引擎

## 项目简介

本项目实现了从中国货币网获取债券数据的功能，并提供了通用正则匹配引擎。

## 项目结构

```
bond_project
├── README.md
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── bond_crawler.py    # 债券数据抓取模块
│   ├── regex_engine.py    # 通用正则引擎
│   ├── utils.py           # 工具函数
│   └── main.py            # 主入口
├── output
│   └── treasury_bond_2023.csv
└── tests
    ├── __init__.py
    └── test_regex.py      # 单元测试（需安装pytest）
```

## 项目特点

1. **自动分页抓取** - 支持大页面数据自动翻页获取
2. **异常处理** - 完整的异常捕获与错误提示
3. **CSV导出** - 支持UTF-8-BOM编码的CSV输出
4. **通用正则匹配引擎** - 配置化设计，灵活扩展
5. **支持后处理函数** - 提取后可自定义处理逻辑
6. **支持多结果提取** - 单次匹配/多次匹配模式
7. **面向对象设计** - 模块化、可维护
8. **符合PEP8规范** - 代码风格统一
9. **易扩展至其他债券类型** - 配置驱动

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 一、债券数据抓取

#### 方法1：直接运行测试脚本

```bash
python test_single_page.py
```

#### 方法2：编程调用

```python
from src.bond_crawler import BondCrawler

crawler = BondCrawler()
records = crawler.fetch_all()
rows = crawler.transform(records)
crawler.save_csv(rows, "output/treasury_bond_2023.csv")
```

#### 抓取条件

- Bond Type: Treasury Bond (债券类型代码: 100001)
- Issue Year: 2023

#### 输出字段

| 字段 | 说明 |
|------|------|
| ISIN | 国际证券识别号 |
| Bond Code | 债券代码 |
| Issuer | 发行人 |
| Bond Type | 债券类型 |
| Issue Date | 发行日期 |
| Latest Rating | 最新评级 |

### 二、正则引擎使用

```python
from src.regex_engine import RegexEngine

text = '''
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债券。
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
# 输出: [{'标的证券': '600900.SH', '换股期限': ['2023-06-02', '2027-06-01']}]
```

### 正则规则配置说明

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| pattern | str | 正则表达式模式 | 必填 |
| group | int | 捕获组索引 | 1 |
| multi | bool | 是否匹配多个结果 | False |
| post_process | callable | 后处理函数 | None |

## 运行测试

```bash
# 需先安装pytest
pip install pytest
pytest tests/ -v
```

## 注意事项

### 代理环境设置

如果系统配置了代理环境变量，可能导致访问被拒绝。可在运行前清理代理：

```bash
# Windows PowerShell
[Environment]::SetEnvironmentVariable("HTTP_PROXY", $null, "Process")
[Environment]::SetEnvironmentVariable("HTTPS_PROXY", $null, "Process")

# Windows Command Prompt
set HTTP_PROXY=
set HTTPS_PROXY=

# Linux/Mac
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy
```

### 接口说明

- 接口URL: `https://www.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN`
- 请求方式: GET
- 查询参数: pageNo, pageSize, bondTypeCode, issueYear
- 注意: pageSize最大支持50（pageSize=100会触发403错误）

### 数据来源

数据来源于中国货币网：[https://www.chinamoney.com.cn/english/bdInfo/](https://www.chinamoney.com.cn/english/bdInfo/)

### 访问限制

- 中国货币网接口可能存在访问频率限制
- 建议添加适当的请求间隔以避免被封禁
- 建议在非高峰期进行数据抓取

## 许可证

MIT License

## 更新日志

- **v1.0** - 初始版本，支持债券数据抓取和正则匹配引擎
- **修复** - 解决代理环境变量导致的403错误
- **修复** - 解决pageSize=100触发的403错误（限制为50）
