
# Components
LangChain 为各种组件提供标准、可扩展的接口和外部集成，这些组件可用于使用 LLM 进行构建。有些组件是 LangChain 实现的，有些组件我们依赖第三方集成，还有一些则是混合的。

## Chat models
语言模型使用一系列消息作为输入，并返回聊天消息作为输出（而不是使用纯文本）。聊天模型支持为对话消息分配不同的角色，帮助区分来自人工智能、用户和系统消息等指令的消息。

尽管底层模型是消息输入、消息输出，但 LangChain 包装器还允许这些模型将字符串作为输入。这意味着您可以轻松地使用聊天模型代替 LLM。

当字符串作为输入传入时，它会转换为 HumanMessage 然后传递给底层模型。

LangChain 不提供任何聊天模型，而是依赖第三方集成。

在构建ChatModel时我们有一些标准化的参数：
model：模型的名称
ChatModels 还接受特定于该集成的其他参数。

## LLMs
语言模型以字符串作为输入并返回字符串。

尽管底层模型是字符串输入、字符串输出，但 LangChain 包装器还允许这些模型将消息作为输入。这使得它们可以与 ChatModel 互换。当消息作为输入传入时，它们将在后台格式化为字符串，然后再传递给底层模型。

LangChain 不提供任何 LLM，而是依赖第三方集成。

## Messages
一些语言模型将消息列表作为输入并返回一条消息。有几种不同类型的消息。所有消息都具有role、content和response_metadata属性。

描述role谁在说这条消息。LangChain 针对不同的角色有不同的消息类别。

该content属性描述消息的内容。这可以是以下几种不同的东西：
1. A string (大多数模型处理这种类型的内容)
2. A List of dictionaries (用于多模式输入，其中字典包含有关该输入类型和输入位置的信息)

### HumanMessage
这代表来自用户的消息。

### AIMessage
这表示来自模型的消息。除了属性之外content，这些消息还具有：

response_metadata
该response_metadata属性包含有关响应的其他元数据。此处的数据通常特定于每个模型提供商。此处可能存储诸如日志问题和令牌使用情况之类的信息。

tool_calls
这些代表语言模型调用工具的决定。它们包含在输出中AIMessage。可以通过属性从那里访问它们.tool_calls。

此属性返回字典列表。每个字典都有以下键：
name：应调用的工具的名称。
args：该工具的参数。
id：该工具调用的id。

### SystemMessage
这代表一条系统消息，它告诉模型如何表现。并非每个模型提供商都支持此功能。

### FunctionMessage
这表示函数调用的结果。除了 和 之外role，content此消息还有一个name参数，用于传达产生此结果所调用的函数的名称。

### ToolMessage
这表示工具调用的结果。这与 FunctionMessage 不同，以便与 OpenAI function和tool消息类型相匹配。除了和之外role，content此消息还有一个tool_call_id参数，该参数将调用的 ID 传达给调用以产生此结果的工具

## Prompt templates
提示模板有助于将用户输入和参数转换为语言模型的指令。这可用于指导模型的响应，帮助其理解上下文并生成相关且连贯的基于语言的输出。

提示模板以字典作为输入，其中每个键代表提示模板中要填写的变量。

Prompt Templates 输出 PromptValue。此 PromptValue 可以传递给 LLM 或 ChatModel，也可以转换为字符串或消息列表。此 PromptValue 存在的原因是为了便于在字符串和消息之间切换。

### String PromptTemplates
这些提示模板用于格式化单个字符串，通常用于较简单的输入。例如，构造和使用 PromptTemplate 的常见方法如下：
```
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")

prompt_template.invoke({"topic": "cats"})
```

### ChatPromptTemplates
这些提示模板用于格式化消息列表。这些“模板”由模板本身的列表组成。例如，构建和使用 ChatPromptTemplate 的常见方法如下：
```
from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
])

prompt_template.invoke({"topic": "cats"})
```
在上面的例子中，这个 ChatPromptTemplate 在调用时会构造两个消息。第一个是系统消息，没有要格式化的变量。第二个是 HumanMessage，将由topic用户传入的变量格式化。

### MessagesPlaceholder
此提示模板负责在特定位置添加消息列表。

在上面的 ChatPromptTemplate 中，我们看到了如何格式化两条消息，每条消息都是一个字符串 。

但如果我们希望用户传入我们将插入特定位置的消息列表，该怎么办？这就是使用 MessagesPlaceholder 的方式。
```
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder("msgs")
])

prompt_template.invoke({"msgs": [HumanMessage(content="hi!")]})
```
这将生成两个消息的列表，第一个是系统消息，第二个是我们传入的 HumanMessage。如果我们传入了 5 条消息，那么它总共会生成 6 条消息（系统消息加上传入的 5 条消息）。这对于将消息列表插入特定位置非常有用。

不明确使用类来完成相同操作的另一种方法MessagesPlaceholder是：
```
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("placeholder", "{msgs}") # <-- This is the changed part
])
```

## Example selectors
为了获得更好的性能，一种常见的提示技巧是将示例作为提示的一部分。

这为语言模型提供了应如何表现的具体示例。有时这些示例被硬编码到提示中，但对于更高级的情况，动态选择它们可能更好。

示例选择器是负责选择示例并将其格式化为提示的类。

## Output parsers
负责获取模型的输出并将其转换为更适合下游任务的格式。当您使用 LLM 生成结构化数据或规范化聊天模型和 LLM 的输出时很有用。

LangChain 有许多不同类型的输出解析器。这是 LangChain 支持的输出解析器列表。下表包含各种信息：

**Name** ：输出解析器的名称

**Supports Streaming**：输出解析器是否支持流。

**Has Format Instructions:**：输出解析器是否具有格式指令。这通常是可用的，除非 (a) 提示中未指定所需架构，而是在其他参数中指定（如 OpenAI 函数调用），或者 (b) 当 OutputParser 包装另一个 OutputParser 时。

**Calls LLMM**：此输出解析器本身是否调用 LLM。这通常仅由尝试纠正格式错误的输出的输出解析器完成。

**Input Type**：预期输入类型。大多数输出解析器都适用于字符串和消息，但有些（如 OpenAI 函数）需要带有特定 kwargs 的消息。

**Output Type**：解析器返回的对象的输出类型。

**Description**：我们对此输出解析器的评论以及何时使用它。

## Chat history
大多数 LLM 应用程序都具有对话界面。对话的一个重要组成部分是能够引用对话中先前介绍的信息。对话系统至少应该能够直接访问过去消息的某些窗口。

概念ChatHistory是指 LangChain 中的一个类，可用于包装任意链。这ChatHistory将跟踪底层链的输入和输出，并将它们作为消息附加到消息数据库中。未来的交互将加载这些消息并将它们作为输入的一部分传递到链中。

## Documents
LangChain 中的 Document 对象包含一些数据的信息。

它有两个属性：
page_content: str：本文档的内容。目前仅为字符串。
metadata: dict：与此文档相关的任意元数据。可以跟踪文档 ID、文件名等。

## Document loaders
这些类加载 Document 对象。LangChain 与各种数据源有数百个集成，可从以下数据源加载数据：Slack、Notion、Google Drive 等。

每个 DocumentLoader 都有自己特定的参数，但它们都可以用相同的方法调用.load。示例用例如下

```
from langchain_community.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(
    ...  # <-- Integration specific parameters here
)
data = loader.load()
```

## Text splitters
加载文档后，您经常需要对它们进行转换，以更好地适应您的应用程序。最简单的例子是，您可能希望将较长的文档拆分为较小的块，以便放入模型的上下文窗口。LangChain 有许多内置的文档转换器，可轻松拆分、合并、过滤和以其他方式操作文档。

当您想要处理长文本时，需要将文本拆分成块。虽然这听起来很简单，但这里却存在很多潜在的复杂性。理想情况下，您希望将语义相关的文本片段放在一起。“语义相关”的含义可能取决于文本的类型。本笔记本展示了几种实现此目的的方法。

从高层次来看，文本分割器的工作原理如下：

将文本分成小的、语义上有意义的块（通常是句子）。
开始将这些小块组合成更大的块，直到达到一定大小（由某些函数衡量）。
一旦达到该大小，就将该块作为其自己的文本，然后开始创建具有一些重叠的新文本块（以保留块之间的上下文）。

这意味着您可以沿着两个不同的轴自定义文本分割器：
文本如何分割
如何测量块大小

## Embedding models
Embeddings 类是专为与文本嵌入模型交互而设计的类。有许多嵌入模型提供程序（OpenAI、Cohere、Hugging Face 等） - 此类旨在为所有这些提供程序提供标准接口。

嵌入会创建一段文本的向量表示。这很有用，因为这意味着我们可以在向量空间中思考文本，并执行语义搜索等操作，即在向量空间中寻找最相似的文本片段。

LangChain 中的基础 Embeddings 类提供了两种方法：一种用于嵌入文档，一种用于嵌入查询。前者接受多个文本作为输入，而后者接受单个文本。将它们作为两个独立方法的原因是，某些嵌入提供程序对文档（要搜索的文档）和查询（搜索查询本身）有不同的嵌入方法。

## Vector stores
存储和搜索非结构化数据的最常见方法之一是嵌入数据并存储生成的嵌入向量，然后在查询时嵌入非结构化查询并检索与嵌入查询“最相似”的嵌入向量。向量存储负责存储嵌入数据并为您执行向量搜索。

可以通过执行以下操作将向量存储转换为检索器接口：
```
vectorstore = MyVectorStore()
retriever = vectorstore.as_retriever()
```

## Retrievers
检索器是一种接口，可根据非结构化查询返回文档。它比向量存储更通用。检索器不需要能够存储文档，只需返回（或检索）文档即可。检索器可以从向量存储中创建，但也足够广泛，包括Wikipedia 搜索和Amazon Kendra。

检索器接受字符串查询作为输入并返回文档列表作为输出。

## Tools
工具是代理、链或聊天模型/LLM 可以用来与世界互动的接口。

工具由以下组件组成：

工具名称
该工具的功能描述
该工具输入的 JSON 模式
要调用的函数
工具的结果是否应直接返回给用户（仅与代理相关）
名称、描述和 JSON 模式作为 LLM 的上下文提供，从而允许 LLM 确定如何适当地使用该工具。

给定可用工具列表和提示，LLM 可以请求使用适当的参数调用一个或多个工具。

一般来说，在设计聊天模型或 LLM 使用的工具时，需要牢记以下几点：

针对工具调用进行过微调的聊天模型在工具调用方面会比未经微调的模型表现得更好。
未经微调的模型可能根本无法使用工具，尤其是在工具很复杂或需要多次工具调用的情况下。
如果工具具有精心选择的名称、描述和 JSON 模式，模型的性能将更好。
与复杂的工具相比，简单的工具通常更容易被模型使用。

## Toolkits
工具包是一组工具的集合，旨在一起用于特定任务。它们具有方便的加载方法。

所有工具包都公开一个get_tools返回工具列表的方法。因此您可以执行以下操作：
```
# Initialize a toolkit
toolkit = ExampleTookit(...)

# Get list of tools
tools = toolkit.get_tools()
```

## Agents
语言模型本身无法采取行动 - 它们只是输出文本。

LangChain 的一大用例是创建代理。

代理是使用 LLM 作为推理引擎来确定要采取哪些行动以及这些行动的输入应该是什么的系统。

然后可以将这些行动的结果反馈给代理，并确定是否需要更多行动，或者是否可以完成。

LangGraph是 LangChain 的一个扩展，专门用于创建高度可控制和可定制的代理。

LangChain 中有一个遗留的代理概念，我们正逐步弃用它：AgentExecutor。
AgentExecutor 本质上是代理的运行时。
它是一个很好的起点，但是，当您开始拥有更多自定义代理时，它不够灵活。
为了解决这个问题，我们构建了 LangGraph 作为这种灵活、高度可控的运行时。

## Multimodal
有些模型是多模态的，接受图像、音频甚至视频作为输入。这些仍然不太常见，这意味着模型提供商尚未就定义 API 的“最佳”方式进行标准化。多模态输出甚至更少见。因此，我们将多模态抽象保持在相当轻量级的水平，并计划随着该领域的成熟进一步巩固多模态 API 和交互模式。

在 LangChain 中，大多数支持多模式输入的聊天模型也接受 OpenAI 内容块格式的值。到目前为止，这仅限于图像输入。对于支持视频和其他字节输入的模型（如 Gemini），API 还支持本机、特定于模型的表示。

## Callbacks
LangChain 提供了一个回调系统，可让您连接到 LLM 应用程序的各个阶段。这对于日志记录、监控、流式传输和其他任务非常有用。

您可以使用callbacksAPI 中提供的参数订阅这些事件。此参数是处理程序对象的列表，这些对象应实现下面更详细描述的一个或多个方法。

### Callback handlers
回调处理程序可以是sync或async：

同步回调处理程序实现BaseCallbackHandler接口。
异步回调处理程序实现AsyncCallbackHandler接口。

在运行时，LangChain 配置适当的回调管理器（例如，CallbackManager或AsyncCallbackManager，它将负责在事件触发时调用每个“已注册”回调处理程序上的适当方法。

### Passing callbacks
该callbacks属性在整个 API（模型、工具、代理等）的大多数对象上均可用，位于两个不同位置：

回调在整个 API（模型、工具、代理等）的大多数对象上可用，位于两个不同的地方：

Request time callbacks：除了输入数据之外，在请求时传递。适用于所有标准Runnable对象。这些回调由定义它们的对象的所有子对象继承。例如chain.invoke({"number": 25}, {"callbacks": [handler]})。
Constructor callbacks：chain = TheNameOfSomeChain(callbacks=[handler])。这些回调作为参数传递给对象的构造函数。回调的作用域仅限于它们定义的对象，不会被对象的任何子对象继承。

