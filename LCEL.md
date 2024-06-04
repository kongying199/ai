# LangChain 表达语言 (LCEL)
LangChain 表达式语言 (LCEL) 是一种声明式的链接 LangChain 组件的方法。LCEL 从第一天开始就被设计为支持将原型投入生产，无需更改代码，从最简单的“prompt + LLM”链到最复杂的链（我们已经看到人们在生产中成功运行了包含 100 多个步骤的 LCEL 链）。以下是您可能想要使用 LCEL 的几个原因：

一流的流式支持 当您使用 LCEL 构建链时，您将获得最佳的第一个令牌时间（直到第一个输出块出现为止所经过的时间）。对于某些链，这意味着例如我们将令牌直接从 LLM 流式传输到流式输出解析器，然后您会以与 LLM 提供程序输出原始令牌相同的速率获得解析后的增量输出块。

异步支持 使用 LCEL 构建的任何链都可以使用同步 API（例如在原型设计时在 Jupyter 笔记本中）以及异步 API（例如在LangServe服务器中）调用。这使得原型和生产中使用相同的代码成为可能，具有出色的性能，并且能够在同一服务器中处理许多并发请求。

优化并行执行 每当您的 LCEL 链具有可以并行执行的步骤时（例如，如果您从多个检索器获取文档），我们都会在同步和异步接口中自动执行此操作，以尽可能减少延迟。

重试和回退 为 LCEL 链的任何部分配置重试和回退。这是让您的链在规模上更可靠的好方法。我们目前正在努力添加对重试/回退的流式支持，这样您就可以获得额外的可靠性而无需任何延迟成本。

访问中间结果 对于更复杂的链，在产生最终输出之前访问中间步骤的结果通常非常有用。这可用于让最终用户知道正在发生的事情，甚至只是调试您的链。您可以流式传输中间结果，并且它在每个LangServe服务器上都可用。

输入和输出模式 输入和输出模式为每个 LCEL 链提供从链结构推断出的 Pydantic 和 JSONSchema 模式。这可用于验证输入和输出，是 LangServe 不可或缺的一部分。

无缝 LangSmith 跟踪 随着您的链条变得越来越复杂，了解每一步究竟发生了什么变得越来越重要。使用 LCEL，所有步骤都会自动记录到LangSmith，以实现最大的可观察性和可调试性。

无缝 LangServe 部署 使用 LCEL 创建的任何链都可以使用LangServe轻松部署。

## Runnable interface
为了尽可能轻松地创建自定义链，我们实现了“Runnable”协议。许多 LangChain 组件都实现了该Runnable协议，包括聊天模型、LLM、输出解析器、检索器、提示模板等。还有几个用于处理 Runnable 的有用原语，您可以在下面阅读。

这是一个标准接口，可以轻松定义自定义链并以标准方式调用它们。标准接口包括：

stream：流回响应块
invoke：在输入上调用链
batch：在输入列表上调用链
它们还具有相应的异步方法，应与asyncio await语法一起使用以实现并发：

astream：异步流回响应块
ainvoke：在输入异步时调用链
abatch：异步调用输入列表上的链
astream_log：除了最终响应之外，还流回中间步骤的发生
astream_events：链中发生的betalangchain-core流事件（在0.1.14 中引入）


The input type and output type varies by component

| Component	    | Input Type                                            | Output Type           |
|---------------|-------------------------------------------------------|-----------------------| 
| Prompt        | Dictionary                                            | PromptValue           |
| ChatModel     | Single string, list of chat messages or a PromptValue | ChatMessage           |
| LLM           | Single string, list of chat messages or a PromptValue | String                |           
| OutputParser	 | The output of an LLM or ChatModel	                    | Depends on the parser |       
| Retriever     | Single string                                         | 	List of Documents    |                                  
| Tool          | Single string or dictionary, depending on the tool    | 	Depends on the tool  | 

所有可运行对象都公开输入和输出模式以检查输入和输出：
input_schema：从 Runnable 结构自动生成的输入 Pydantic 模型
output_schema：从 Runnable 结构自动生成的输出 Pydantic 模型