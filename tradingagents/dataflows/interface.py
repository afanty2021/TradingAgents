"""
TradingAgents 数据流统一接口模块
====================================

这个模块是TradingAgents系统的数据基础架构的核心，提供统一的多供应商
数据接口和智能路由机制。它集成了多个优质数据源，通过抽象接口设计
为上层智能体提供可靠、高效的数据服务。

核心功能：
- 多供应商数据集成（Alpha Vantage、Yahoo Finance、Google News、OpenAI、本地数据）
- 智能路由和故障转移机制
- 统一的工具接口和标准化输出格式
- 按类别和工具级别的灵活配置
- 内置错误处理和性能优化

设计理念：
- 抽象接口设计：隐藏供应商实现细节，提供统一的数据访问接口
- 智能路由机制：支持供应商优先级配置和自动故障转移
- 数据质量保证：内置验证、限流控制和数据格式标准化
- 性能优化：支持缓存、批量处理和并发请求优化

使用示例：
    # 获取股票数据（自动路由到配置的供应商）
    stock_data = route_to_vendor("get_stock_data", "AAPL", "2024-01-01", "2024-01-31")

    # 获取技术指标
    indicators = route_to_vendor("get_indicators", "AAPL", "RSI", "2024-01-15", 30)

作者：TradingAgents团队
版本：1.0.0
"""

# ==============================================================================
# 导入必要的库和模块
# ==============================================================================

from typing import Annotated

# ==============================================================================
# 导入各供应商模块的具体实现
# ==============================================================================

# 本地数据源 - 包含各种缓存和离线数据
from .local import (
    get_YFin_data,                                        # 本地Yahoo Finance数据缓存
    get_finnhub_news,                                     # 本地Finnhub新闻数据
    get_finnhub_company_insider_sentiment,               # 本地内部人情绪数据
    get_finnhub_company_insider_transactions,             # 本地内部人交易数据
    get_simfin_balance_sheet,                            # 本地SimFin资产负债表
    get_simfin_cashflow,                                  # 本地SimFin现金流量表
    get_simfin_income_statements,                        # 本地SimFin损益表
    get_reddit_global_news,                              # 本地Reddit全球新闻
    get_reddit_company_news                              # 本地Reddit公司新闻
)

# Yahoo Finance在线数据源 - 实时市场和财务数据
from .y_finance import (
    get_YFin_data_online,                                # Yahoo Finance在线股价数据
    get_stock_stats_indicators_window,                   # Yahoo Finance技术指标计算
    get_balance_sheet as get_yfinance_balance_sheet,     # Yahoo Finance资产负债表
    get_cashflow as get_yfinance_cashflow,               # Yahoo Finance现金流量表
    get_income_statement as get_yfinance_income_statement, # Yahoo Finance损益表
    get_insider_transactions as get_yfinance_insider_transactions # Yahoo Finance内部人交易
)

# Google新闻数据源 - 新闻搜索和舆情监控
from .google import get_google_news

# OpenAI数据源 - AI驱动的分析和处理
from .openai import (
    get_stock_news_openai,                               # OpenAI股票新闻分析
    get_global_news_openai,                              # OpenAI全球新闻分析
    get_fundamentals_openai                              # OpenAI基本面分析
)

# Alpha Vantage数据源 - 专业的金融数据API
from .alpha_vantage import (
    get_stock as get_alpha_vantage_stock,                # Alpha Vantage股价数据
    get_indicator as get_alpha_vantage_indicator,        # Alpha Vantage技术指标
    get_fundamentals as get_alpha_vantage_fundamentals,  # Alpha Vantage基本面数据
    get_balance_sheet as get_alpha_vantage_balance_sheet, # Alpha Vantage资产负债表
    get_cashflow as get_alpha_vantage_cashflow,          # Alpha Vantage现金流量表
    get_income_statement as get_alpha_vantage_income_statement, # Alpha Vantage损益表
    get_insider_transactions as get_alpha_vantage_insider_transactions, # Alpha Vantage内部人交易
    get_news as get_alpha_vantage_news                   # Alpha Vantage新闻数据
)

# Alpha Vantage公共功能 - 错误处理和限流管理
from .alpha_vantage_common import AlphaVantageRateLimitError

# ==============================================================================
# 导入配置和路由逻辑模块
# ==============================================================================

from .config import get_config

# ==============================================================================
# 工具分类定义
# ==============================================================================

# 将所有数据获取工具按功能类别进行组织，便于配置管理和路由
TOOLS_CATEGORIES = {
    # 核心股票API - 提供基础的OHLCV股价数据
    "core_stock_apis": {
        "description": "OHLCV股价数据 - 开盘价、最高价、最低价、收盘价和成交量",
        "tools": [
            "get_stock_data"  # 获取股票历史价格数据的主要接口
        ]
    },

    # 技术指标 - 提供各种技术分析指标计算
    "technical_indicators": {
        "description": "技术分析指标 - RSI、MACD、布林带等技术指标",
        "tools": [
            "get_indicators"  # 获取各类技术指标的统一接口
        ]
    },

    # 基本面数据 - 提供公司财务基本面信息
    "fundamental_data": {
        "description": "公司基本面数据 - 财务报表、估值指标等",
        "tools": [
            "get_fundamentals",           # 综合基本面分析数据
            "get_balance_sheet",          # 资产负债表数据
            "get_cashflow",               # 现金流量表数据
            "get_income_statement"        # 损益表数据
        ]
    },

    # 新闻数据 - 提供各种新闻和舆情信息
    "news_data": {
        "description": "新闻数据 - 公开新闻、内部人消息、原始和处理后的新闻内容",
        "tools": [
            "get_news",                   # 公司相关新闻
            "get_global_news",            # 全球宏观新闻
            "get_insider_sentiment",
            "get_insider_transactions",
        ]
    }
}

VENDOR_LIST = [
    "local",
    "yfinance",
    "openai",
    "google"
]

# Mapping of methods to their vendor-specific implementations
VENDOR_METHODS = {
    # core_stock_apis
    "get_stock_data": {
        "alpha_vantage": get_alpha_vantage_stock,
        "yfinance": get_YFin_data_online,
        "local": get_YFin_data,
    },
    # technical_indicators
    "get_indicators": {
        "alpha_vantage": get_alpha_vantage_indicator,
        "yfinance": get_stock_stats_indicators_window,
        "local": get_stock_stats_indicators_window
    },
    # fundamental_data
    "get_fundamentals": {
        "alpha_vantage": get_alpha_vantage_fundamentals,
        "openai": get_fundamentals_openai,
    },
    "get_balance_sheet": {
        "alpha_vantage": get_alpha_vantage_balance_sheet,
        "yfinance": get_yfinance_balance_sheet,
        "local": get_simfin_balance_sheet,
    },
    "get_cashflow": {
        "alpha_vantage": get_alpha_vantage_cashflow,
        "yfinance": get_yfinance_cashflow,
        "local": get_simfin_cashflow,
    },
    "get_income_statement": {
        "alpha_vantage": get_alpha_vantage_income_statement,
        "yfinance": get_yfinance_income_statement,
        "local": get_simfin_income_statements,
    },
    # news_data
    "get_news": {
        "alpha_vantage": get_alpha_vantage_news,
        "openai": get_stock_news_openai,
        "google": get_google_news,
        "local": [get_finnhub_news, get_reddit_company_news, get_google_news],
    },
    "get_global_news": {
        "openai": get_global_news_openai,
        "local": get_reddit_global_news
    },
    "get_insider_sentiment": {
        "local": get_finnhub_company_insider_sentiment
    },
    "get_insider_transactions": {
        "alpha_vantage": get_alpha_vantage_insider_transactions,
        "yfinance": get_yfinance_insider_transactions,
        "local": get_finnhub_company_insider_transactions,
    },
}

def get_category_for_method(method: str) -> str:
    """Get the category that contains the specified method."""
    for category, info in TOOLS_CATEGORIES.items():
        if method in info["tools"]:
            return category
    raise ValueError(f"Method '{method}' not found in any category")

def get_vendor(category: str, method: str = None) -> str:
    """Get the configured vendor for a data category or specific tool method.
    Tool-level configuration takes precedence over category-level.
    """
    config = get_config()

    # Check tool-level configuration first (if method provided)
    if method:
        tool_vendors = config.get("tool_vendors", {})
        if method in tool_vendors:
            return tool_vendors[method]

    # Fall back to category-level configuration
    return config.get("data_vendors", {}).get(category, "default")

def route_to_vendor(method: str, *args, **kwargs):
    """Route method calls to appropriate vendor implementation with fallback support."""
    category = get_category_for_method(method)
    vendor_config = get_vendor(category, method)

    # Handle comma-separated vendors
    primary_vendors = [v.strip() for v in vendor_config.split(',')]

    if method not in VENDOR_METHODS:
        raise ValueError(f"Method '{method}' not supported")

    # Get all available vendors for this method for fallback
    all_available_vendors = list(VENDOR_METHODS[method].keys())
    
    # Create fallback vendor list: primary vendors first, then remaining vendors as fallbacks
    fallback_vendors = primary_vendors.copy()
    for vendor in all_available_vendors:
        if vendor not in fallback_vendors:
            fallback_vendors.append(vendor)

    # Debug: Print fallback ordering
    primary_str = " → ".join(primary_vendors)
    fallback_str = " → ".join(fallback_vendors)
    print(f"DEBUG: {method} - Primary: [{primary_str}] | Full fallback order: [{fallback_str}]")

    # Track results and execution state
    results = []
    vendor_attempt_count = 0
    any_primary_vendor_attempted = False
    successful_vendor = None

    for vendor in fallback_vendors:
        if vendor not in VENDOR_METHODS[method]:
            if vendor in primary_vendors:
                print(f"INFO: Vendor '{vendor}' not supported for method '{method}', falling back to next vendor")
            continue

        vendor_impl = VENDOR_METHODS[method][vendor]
        is_primary_vendor = vendor in primary_vendors
        vendor_attempt_count += 1

        # Track if we attempted any primary vendor
        if is_primary_vendor:
            any_primary_vendor_attempted = True

        # Debug: Print current attempt
        vendor_type = "PRIMARY" if is_primary_vendor else "FALLBACK"
        print(f"DEBUG: Attempting {vendor_type} vendor '{vendor}' for {method} (attempt #{vendor_attempt_count})")

        # Handle list of methods for a vendor
        if isinstance(vendor_impl, list):
            vendor_methods = [(impl, vendor) for impl in vendor_impl]
            print(f"DEBUG: Vendor '{vendor}' has multiple implementations: {len(vendor_methods)} functions")
        else:
            vendor_methods = [(vendor_impl, vendor)]

        # Run methods for this vendor
        vendor_results = []
        for impl_func, vendor_name in vendor_methods:
            try:
                print(f"DEBUG: Calling {impl_func.__name__} from vendor '{vendor_name}'...")
                result = impl_func(*args, **kwargs)
                vendor_results.append(result)
                print(f"SUCCESS: {impl_func.__name__} from vendor '{vendor_name}' completed successfully")
                    
            except AlphaVantageRateLimitError as e:
                if vendor == "alpha_vantage":
                    print(f"RATE_LIMIT: Alpha Vantage rate limit exceeded, falling back to next available vendor")
                    print(f"DEBUG: Rate limit details: {e}")
                # Continue to next vendor for fallback
                continue
            except Exception as e:
                # Log error but continue with other implementations
                print(f"FAILED: {impl_func.__name__} from vendor '{vendor_name}' failed: {e}")
                continue

        # Add this vendor's results
        if vendor_results:
            results.extend(vendor_results)
            successful_vendor = vendor
            result_summary = f"Got {len(vendor_results)} result(s)"
            print(f"SUCCESS: Vendor '{vendor}' succeeded - {result_summary}")
            
            # Stopping logic: Stop after first successful vendor for single-vendor configs
            # Multiple vendor configs (comma-separated) may want to collect from multiple sources
            if len(primary_vendors) == 1:
                print(f"DEBUG: Stopping after successful vendor '{vendor}' (single-vendor config)")
                break
        else:
            print(f"FAILED: Vendor '{vendor}' produced no results")

    # Final result summary
    if not results:
        print(f"FAILURE: All {vendor_attempt_count} vendor attempts failed for method '{method}'")
        raise RuntimeError(f"All vendor implementations failed for method '{method}'")
    else:
        print(f"FINAL: Method '{method}' completed with {len(results)} result(s) from {vendor_attempt_count} vendor attempt(s)")

    # Return single result if only one, otherwise concatenate as string
    if len(results) == 1:
        return results[0]
    else:
        # Convert all results to strings and concatenate
        return '\n'.join(str(result) for result in results)