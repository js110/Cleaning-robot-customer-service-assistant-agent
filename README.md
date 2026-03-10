# 清洁机器人智能客服助手

这是一个面向清洁机器人场景的智能客服助手项目，基于 `Streamlit`、`LangChain`、RAG 和 DashScope 模型构建，适合演示智能问答、知识库检索、外部工具调用与报告生成等能力。

## 项目特点

- 基于 `Streamlit` 的对话式客服界面
- 支持产品问答、故障排查、维护保养、选购建议等知识检索
- 通过 Agent 工具调用天气查询、用户定位、用户使用数据读取等能力
- 支持根据场景动态切换提示词
- 使用本地 `Chroma` 向量库进行知识索引与召回

## 目录结构

```text
.
+-- app.py                  # Streamlit 应用入口
+-- react_agent.py          # Agent 组装与流式输出
+-- model/                  # 模型工厂与 API Key 读取
+-- rag/                    # 检索增强生成与向量库逻辑
+-- tools/                  # 工具定义与中间件
+-- utils/                  # 配置、日志、文件处理、天气服务等通用模块
+-- config/                 # YAML 配置文件
+-- prompts/                # 提示词模板
+-- data/                   # 知识库文档与外部业务数据
```

## 运行环境

- 推荐 Python 3.11 及以上版本
- 需要可用的 DashScope API Key

## 快速开始

1. 创建并激活虚拟环境
2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置模型密钥

```bash
copy .env.example .env
```

然后在终端环境变量或你自己的 `.env` 加载流程中设置：

```bash
DASHSCOPE_API_KEY=your_dashscope_api_key
```

仓库中不会保存真实密钥。

4. 初始化或刷新向量库

```bash
python rag/vector_store.py
```

5. 启动应用

```bash
streamlit run app.py
```

## 配置说明

- `config/rag.yml`：大模型与向量模型名称配置
- `config/chroma.yml`：向量库目录、召回条数、文本切分参数
- `config/agent.yml`：外部 CSV 数据路径
- `config/prompts.yml`：提示词文件路径映射

## 数据来源

当前知识数据主要来自 `data/` 目录，包括：

- 清洁机器人常见问题文档
- 故障排除文档
- 维护保养文档
- 选购指南文档
- `data/external/records.csv` 中的用户外部使用记录

## 安全说明

- 不要提交 `.env`、日志文件、本地向量库和缓存文件
- 优先通过环境变量 `DASHSCOPE_API_KEY` 提供密钥
- 对外分享仓库前，确认测试代码和配置中没有残留真实密钥

## 后续可扩展方向

- 接入真实订单、售后、设备状态等业务系统
- 增加多轮会话记忆与用户画像能力
- 增加知识库增量更新与后台管理能力
- 增加部署说明，例如云服务器或容器化部署

## License

如果项目需要开源或对外分发，建议补充 `LICENSE` 文件。
