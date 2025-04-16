# Zaka Media Push

一个自动化的学术论文推送系统，用于爬取arxiv等学术网站的论文，生成摘要和解读，并自动生成适合微信公众号和小红书发布的内容。

## 功能特点

- 📚 自动爬取arxiv最新论文
- 🤖 使用AI生成论文摘要和解读
- 📱 自动生成适合不同平台的内容格式
- ⏰ 定时任务自动执行
- 📝 完善的日志系统
- 🛠️ 模块化设计，易于扩展
- 🔒 完善的错误处理机制

## 系统要求

- Python 3.8+
- pip 20.0+
- OpenAI API密钥

## 安装说明

1. 克隆项目
```bash
git clone https://github.com/Wheeeeeeeeels/zaka-media-push.git
cd zaka-media-push
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，填入必要的配置信息
```

## 配置说明

在`.env`文件中可以配置以下参数：

```ini
# OpenAI配置
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
TEMPERATURE=0.7
SUMMARY_LENGTH=1000

# 爬虫配置
MAX_PAPERS_PER_DAY=5
DAYS_TO_CRAWL=7

# 定时任务配置
SCHEDULE_TIME=10:00

# 输出配置
OUTPUT_DIR=output
WECHAT_TEMPLATE=templates/wechat.md
XIAOHONGSHU_TEMPLATE=templates/xiaohongshu.md
```

## 使用方法

1. 直接运行主程序
```bash
python src/main.py
```

2. 程序会自动：
   - 每天上午10点执行爬取任务
   - 生成论文摘要和解读
   - 生成适合不同平台的内容
   - 将内容保存到output目录

## 项目结构

```
.
├── src/
│   ├── paper_crawler.py    # 论文爬取模块
│   ├── summary_generator.py # 摘要生成模块
│   ├── content_formatter.py # 内容格式化模块
│   ├── main.py             # 主程序
│   └── utils/              # 工具模块
│       ├── __init__.py
│       ├── logger.py       # 日志模块
│       ├── error_handler.py # 错误处理模块
│       └── config.py       # 配置模块
├── templates/              # 内容模板
│   ├── wechat.md          # 微信公众号模板
│   └── xiaohongshu.md     # 小红书模板
├── tests/                  # 测试文件
├── output/                 # 输出目录
├── logs/                   # 日志目录
├── requirements.txt        # 项目依赖
├── .env.example           # 环境变量示例
├── .gitignore             # Git忽略文件
├── LICENSE                # 许可证
└── README.md              # 项目说明
```

## 开发指南

### 添加新的论文来源

1. 在`paper_crawler.py`中添加新的爬取方法
2. 实现相应的错误处理
3. 更新配置系统

### 自定义内容模板

1. 在`templates`目录下创建新的模板文件
2. 在`content_formatter.py`中添加相应的格式化方法
3. 更新配置系统

### 添加新的AI模型

1. 在`summary_generator.py`中添加新的模型支持
2. 更新配置系统

## 错误处理

系统使用自定义异常类处理不同类型的错误：

- `ZakaError`: 基础异常类
- `PaperCrawlError`: 论文爬取错误
- `SummaryGenerationError`: 摘要生成错误
- `ContentFormatError`: 内容格式化错误

## 日志系统

系统使用Python的logging模块记录日志，日志文件保存在`logs`目录下，按日期命名。

## 贡献指南

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证 - 详情请参阅 [LICENSE](LICENSE) 文件

## 联系方式

如有任何问题或建议，请通过以下方式联系：

- 提交Issue
- 发送邮件至 [your-email@example.com](mailto:your-email@example.com)

## 致谢

- [arxiv](https://arxiv.org/) - 论文来源
- [OpenAI](https://openai.com/) - AI模型支持

