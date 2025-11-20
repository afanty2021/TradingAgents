"""
TradingAgents 系统默认配置文件
==============================

这个文件定义了TradingAgents智能交易代理系统的所有默认配置参数。
配置系统采用分层设计，支持全局默认值、类别级配置和工具级配置覆盖。

主要配置分类：
- 目录和路径配置
- 大语言模型(LLM)配置
- 智能体辩论和讨论参数
- 数据供应商配置（支持多层级配置）

配置优先级（从高到低）：
1. 工具级配置 (tool_vendors)
2. 类别级配置 (data_vendors)
3. 系统默认值

使用示例：
    from tradingagents.default_config import DEFAULT_CONFIG

    # 复制并修改配置
    config = DEFAULT_CONFIG.copy()
    config["deep_think_llm"] = "gpt-4"

    # 修改数据供应商
    config["data_vendors"]["core_stock_apis"] = "alpha_vantage"

作者：TradingAgents团队
版本：1.0.0
"""

import os

# ==============================================================================
# TradingAgents 系统默认配置
# ==============================================================================

DEFAULT_CONFIG = {
    # ========================================================================
    # 目录和路径配置
    # ========================================================================

    # 项目根目录：自动检测当前文件所在目录作为项目根目录
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),

    # 结果输出目录：存储分析结果、报告和决策文件
    # 可通过环境变量 TRADINGAGENTS_RESULTS_DIR 自定义，默认为 "./results"
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),

    # 原始数据目录：存储历史数据和训练数据
    # 注意：这是一个硬编码路径，实际使用时建议根据环境调整
    "data_dir": "/Users/yluo/Documents/Code/ScAI/FR1-data",

    # 数据缓存目录：存储API响应缓存，减少重复请求
    # 相对于项目根目录的路径：tradingagents/dataflows/data_cache
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),

    # ========================================================================
    # 大语言模型 (LLM) 配置
    # ========================================================================

    # LLM提供商：支持 openai, anthropic, google, openrouter, ollama 等
    "llm_provider": "openai",

    # 深度思考模型：用于复杂分析、决策制定和深度推理
    # 建议使用更强大的模型如 GPT-4、Claude-3 等
    "deep_think_llm": "o4-mini",

    # 快速思考模型：用于快速响应、简单处理和辅助任务
    # 建议使用快速且经济的模型如 GPT-3.5-turbo、GPT-4o-mini 等
    "quick_think_llm": "gpt-4o-mini",

    # 后端API URL：LLM服务的API端点
    # 支持自定义端点，如本地部署的模型服务
    "backend_url": "https://api.openai.com/v1",

    # ========================================================================
    # 智能体辩论和讨论设置
    # ========================================================================

    # 最大投资辩论轮数：控制看涨/看跌研究员之间的辩论深度
    # 数值越大，讨论越深入，但耗时更长
    "max_debate_rounds": 1,

    # 最大风险评估讨论轮数：控制激进/保守/中立风险评估师的讨论深度
    # 影响风险分析的全面性和准确性
    "max_risk_discuss_rounds": 1,

    # 最大递归限制：防止工作流陷入无限循环的安全机制
    # 控制整个决策流程的最大步骤数
    "max_recur_limit": 100,

    # ========================================================================
    # 数据供应商配置
    # ========================================================================

    # 类别级配置：为整个数据类别设置默认供应商
    # 这些配置会应用到对应类别下的所有工具，除非被工具级配置覆盖
    "data_vendors": {
        # 核心股票API：提供基础股价数据（OHLCV）
        # 可选供应商：
        # - yfinance: Yahoo Finance，免费且可靠，适合实时数据
        # - alpha_vantage: 功能全面但有API限制，适合历史数据
        # - local: 本地数据，离线使用
        "core_stock_apis": "yfinance",

        # 技术指标数据：提供技术分析指标（RSI、MACD、布林带等）
        # 可选供应商：yfinance, alpha_vantage, local
        "technical_indicators": "yfinance",

        # 基本面数据：提供财务报表、公司估值等基本面信息
        # 可选供应商：
        # - alpha_vantage: 传统财务数据，结构化程度高
        # - openai: AI分析的基本面数据，可能包含更深入的洞察
        # - local: 本地存储的财务数据
        "fundamental_data": "alpha_vantage",

        # 新闻数据：提供市场新闻、舆情信息
        # 可选供应商：
        # - alpha_vantage: 金融新闻数据，专业性强
        # - openai: AI处理的新闻摘要和分析
        # - google: 谷歌新闻，覆盖面广
        # - local: 本地新闻数据或缓存
        "news_data": "alpha_vantage",
    },

    # ========================================================================
    # 工具级配置（优先级高于类别级配置）
    # ========================================================================

    # 工具级配置允许为特定工具指定供应商，覆盖类别级默认设置
    # 这提供了更细粒度的控制，可以根据具体需求优化数据源选择
    "tool_vendors": {
        # 示例：为特定工具覆盖类别默认配置
        # "get_stock_data": "alpha_vantage",      # 强制使用Alpha Vantage获取股价数据
        # "get_news": "openai",                   # 使用OpenAI处理新闻数据
        # "get_indicators": "yfinance",           # 使用Yahoo Finance计算技术指标

        # 注释：当前为空配置，表示使用类别级默认设置
        # 用户可以根据需要取消注释并修改特定工具的供应商
    },

    # ========================================================================
    # 其他高级配置（预留）
    # ========================================================================

    # 以下配置项为预留项，可在未来版本中扩展
    # "cache_ttl": 3600,                    # 数据缓存生存时间（秒）
    # "rate_limiting": True,                # 是否启用API限流
    # "parallel_processing": True,          # 是否启用并行处理
    # "debug_mode": False,                  # 调试模式开关
}
