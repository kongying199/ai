# Techniques

## Function/tool calling
工具调用允许模型通过生成与用户定义的架构相匹配的输出来响应给定的提示。虽然名称暗示模型正在执行某些操作，但事实并非如此！模型会提出工具的参数，而实际运行该工具（或不运行）则取决于用户 - 例如，如果您想从非结构化文本中提取与某些架构相匹配的输出 ，您可以为模型提供一个“提取”工具，该工具采用与所需架构相匹配的参数，然后将生成的输出视为最终结果。

工具调用包括名称、参数字典和可选标识符。参数字典是结构化的{argument_name: argument_value}。

许多 LLM 提供商（包括Anthropic、 Cohere、Google、 Mistral、OpenAI等）都支持工具调用功能的变体。这些功能通常允许对 LLM 的请求包含可用的工具及其模式，并允许响应包含对这些工具的调用。例如，给定一个搜索引擎工具，LLM 可能会通过首先向搜索引擎发出调用来处理查询。调用 LLM 的系统可以接收工具调用、执行它，并将输出返回给 LLM 以通知其响应。LangChain 包含一套内置工具 ，并支持多种定义您自己的自定义工具的方法。

LangChain提供了标准化的工具调用接口，保证不同模型之间的一致性。

标准接口包括：

ChatModel.bind_tools()：一种指定模型可以调用哪些工具的方法。
AIMessage.tool_calls：从模型返回的属性AIMessage，用于访问模型请求的工具调用。
函数/工具调用主要有两种用例：

如何从 LLM 返回结构化数据
如何使用模型调用工具

## Retrieval
LangChain 提供了几种高级检索类型。完整列表如下，以及以下信息：

**Name**：检索算法的名称。

**Index Type**：依赖哪种索引类型（如果有）。

**Uses an LLM**：此检索方法是否使用 LLM。

**When to Use**：我们对何时应考虑使用此检索方法的评论。

**Description**：描述此检索算法正在做什么。

## Text splitting
LangChain 提供多种不同类型的text splitters。这些都包含在langchain-text-splitters包中。

Table columns:

Name：文本分割器的名称

Classes：实现此文本分割器的类

Splits On:：此文本拆分器如何拆分文本

Adds Metadata：此文本分割器是否添加有关每个块来源的元数据。

Description：分离器的描述，包括何时使用它的建议。
