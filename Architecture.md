LangChain 作为一个框架，由许多包组成。

# langchain-core
此包包含不同组件的基本抽象以及将它们组合在一起的方法。

此处定义了 LLM、vectorstore、检索器等核心组件的接口。

此处未定义第三方集成。有意将依赖项保持为非常轻量级。

# langchain
主langchain包包含构成应用程序认知架构的链、代理和检索策略。

这些不是第三方集成。

此处的所有链、代理和检索策略都不是特定于任何一种集成的，而是所有集成的通用策略。

# langchain-community
此包包含由 LangChain 社区维护的第三方集成。

它包含各种组件（LLM、vectorstore、检索器）的所有集成。

此包中的所有依赖项都是可选的，以使包尽可能轻量。

# langgraph
langgraph是一种扩展，langchain旨在通过将步骤建模为图中的边和节点，使用 LLM 构建健壮且有状态的多参与者应用程序。

LangGraph 公开了用于创建常见代理类型的高级接口，以及用于构建更多控制的低级 API。

# langserve
一个将 LangChain 链部署为 REST API 的软件包。可轻松启动和运行可用于生产的 API。

# LangSmith
一个开发人员平台，可让您调试、测试、评估和监控 LLM 应用程序。

![这是图片](/resource/langchain_stack.svg "langchain_stack")







