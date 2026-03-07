# Trawpaw

他至少是图灵完备的

## 用法

### Python

版本: 7.4.1

#### 用我们的命令行

现在, trawpaw支持Windows, MacOS和Linux. 你可以用命令行界面
执行Trawpaw代码.

从 [这里](https://github.com/LiaoxyuCM/trawpaw/releases) 下载最新的发行版，
解压他. 你可以在你终端里跑下面的命令:

```sh
##### WINDOWS, MACOS 或 LINUX #####
trawpaw # 打开 Trawpaw 交互式环境
trawpaw --help # 获取更多信息
trawpaw --usage # 显示Trawpaw用法
trawpaw --version # 显示trawpaw版本
trawpaw filepath # 运行文件里面的代码
```

打开交互式环境后, 你会看到 `[c:0 v:0]`. `c:0` 意味着当前指针的地址是0，
`v:0` 意味着0个（没有）变量被定义.

在v7.2及以后，交互式环境会生成 `.tphistories`
如果你想清除交互式环境的历史记录 \(v7.2及以后\), 删掉这个文件就行了

如果你不想生成那个文件, 请使用 `--nohistories`.

#### 在你的python程序中执行

你得先克隆这个仓库+创建虚拟环境\(可选，但推荐\)+安装依赖.

在你的终端运行以下命令:

注意: 如果前一个命令运行不了, 你要检查这个命令
是否已安装或者网络是否通畅，然后重试.

```sh
## 克隆仓库
git clone https://github.com/LiaoxyuCM/trawpaw.git
cd trawpaw
## 创建虚拟环境
python -m venv pyenv # Or custom name of virtual env
pyenv/Scripts/activate
## 安装依赖
pip install --upgrade pip
pip install -r requirements.txt
```

然后你可以在你的代码里导入 `trawpaw` 库，
使用 `Trawpaw` 类来执行 Trawpaw 代码.

需要 Python 解释器 v3.10 或更高.

```py
import trawpaw;
executor = trawpaw.Trawpaw(
    # 格子的长度, 默认为 128 (0 < cells <= 65536)
    # 在v6.0之前他叫 "memories"
    cells=128,
    # 每个格子的最大值, 默认为 127 (0 < maxvaluepercell <= 65536)
    # 在v6.0之前他叫 "maxvaluepermem"
    maxvaluepercell=127,
);
result = executor.execute(
    "你的trawpaw源代码",
    "输入 如果这个程序需要输入（可选）",
    
    clearData=False, # clearData: 默认值是 False
    
    startAtCol=0, # 永远不要传这个参数; 他只会在内部执行时要求传参.

    # 参数名在v6.0及以后使用驼峰命名法
    # 在v6.0之前, 他使用蛇形命名法.
    # 你可以使用下面的其中之一来传参:
    # - TrawpawExecutionMethod.printManually: 直接打印结果 (默认)
    #                                         然后做 `~.storeInResult` (看后面)
    # - TrawpawExecutionMethod.storeInResult: 将结果保存下来
    #                                         运行结束时返回结果
    executionMethod=trawpaw.TrawpawExecutionMethod.printManually
); # 在v6.0之前返回 “dict” , 在v6.0及以后返回 “TrawpawResult”
```

##### 处理结果

在 v6.0 之前

```py
if trawpaw_result["status"] == 1:
  print(result.get("message", "ERR: 未知异常."))
else:
  print(result.get("result", ""))

```

在 v6.0 之后

```py
if trawpaw_result.status == 1:
  print(result.message)
else:
  print(result.result)
```

`Treapaw().execute()` 在v6.0之前返回一个字典
但在v6.0及以后返回一个 `TrawpawResult` 对象

- status

| status | 意味      |
| ------ | --------- |
| 0      | 正常      |
| 1      | 报错      |
| 2      | 中途结束  |

- message: 当status是 1, 这个键会包含错误信息.
  反之，它不存在

- result: 当status是 0 或 2, 这个键会包含Trawpaw代码
  的最终输出. 反之，它不存在

- cursor: 在运行代码后指针的地址.
  \(不推荐, 只有REPL才需要\)

- datalistlength: 在运行代码后的数据列表.
  \(不推荐, 只有REPL才需要\)

### JavaScript (前端)

注意: **我们已对Trawpaw JavaScript终止支持
请使用Trawpaw python**

版本: 1.1.1

```js
import { Trawpaw } from "./trawpaw.js";
document.addEventListener("DOMContentLoaded", () => {
  const trawpaw = new Trawpaw();
  let result = trawpaw.execute(
    "你的trawpaw代码",
    "输入 如果这个程序需要输入（可选）",
    clearHistory=false /* or true */
  );
  if (result["status"] === 1) {
    console.error(result["message"]);
  } else {
    console.log(result["result"]);
  };
});
```

## Hello World 在 Trawpaw

v4.5 之前

```trawpaw
!##[[[[[[+]]]+]]].>#[[[[[[+]+]]]+]]+.[[+]+]+..[+]+.>#[[[[[+]]+]+]].[[[-]-]].<[[[+]]].[[[-]]].[+]+.[[-]-].[[[-]]].>+.#<#<#
```

v4.5 及以后

```trawpaw
!!#$ai$as"Hello, world!"!$print$a
```

## 进阶教程

### 注册自定义功能

看下面的代码:

```py
@trawpaw_executor.registerCustomModule(
    # 参数 name: str: 这个功能的名称.
    # ---- 注意: 不要在名称里包含 "$"
    name="module name",
    # 参数 availableDatatypes: trawpaw.TrawpawDatatypes:
    # ---- 这个功能可以处理的数据类型.
    # ---- 注意: TrawpawDatatypes 是标志枚举, 你可以
    # ----     连接 多个数据类型 使用管道符 (|).
    availableDatatypes=trawpaw.TrawpawDatatypes.String | trawpaw.TrawpawDatatypes.Number,
    # param handleResult: trawpaw.TrawpawHandleModuleResult:
    # ---- 处理结果的方法.
    # ---- 默认值是 `TrawpawHandleModuleResult.printManually`
    handleResult=trawpaw.TrawpawHandleModuleResult.printManually
)
def foo(arg: str | int) -> str: # 你的功能必需且只有一个参数要传
    return f"你输入的是 {arg}"
```

如果新的功能跟之前任意一个功能重名了,
新的功能会覆盖掉之前的功能.

请阅读 `customModulesExample.py` 获取更多示例.

#### 数据类型对照表

| trawpaw内部数据类型  | python类         | 标志枚举 TrawpawDatatypes    |
| -------------------- | ---------------- | ---------------------------- |
| "string"             | str              | TrawpawDatatypes.String      |
| "number"             | int              | TrawpawDatatypes.Number      |
| "function"           | TrawpawFunction  | TrawpawDatatypes.Function    |
| "linkcell"           | TrawpawLinkCell  | TrawpawDatatypes.LinkCell    |

注意: 在 v7.0 之前, "linkcell" 叫 "linkmemory".

- 我们会判断trawpaw该用的数据类型
  在你自定义功能的返回值的类型为基础.
  \(python类 =&gt; trawpaw内部数据类型\)

  失败的话，解释器会抛出异常

- 同理，我们会判断自定义功能传的参数该用的数据类型
  以`executor.registerCustomModule`内的参数`availableDatatypes`为基础

  \(TrawpawDatatypes =&gt; python类\)

  失败的话，一样的，解释器会抛出异常

#### 处理自定义功能的结果

使用 `TrawpawHandleModuleResult` 来处理自定义功能的结果.

| 选项            | 意味                                                       |
| --------------- | ---------------------------------------------------------- |
| assignToVar     | 把结果存回到传的参数里                                     |
| storeToCurrCell | 保存在trawpaw当前的格子里 \(仅int\)                        |
| printManually   | 直接打印结果\(默认\) \(仅str \| int\)                      |

#### 注销你的自定义功能

```py
executor.unregisterCustomModule("功能名称")
```

是的，`unregisterCustomModule` 不是装饰器.

但在 7.0_1 之前, 请使用 `del executor.customModules["module name"]`.

#### TrawpawFunction 和 TrawpawLinkCell

定义对象

```py
TrawpawFunction(函数内容: str)
TrawpawLinkCell(指针地址: int)
```

获取内容

```py
trawpaw_function.value # trawpaw_function 是 TrawpawFunction 的实例
trawpaw_link_cell.value # trawpaw_link_cell 是 TrawpawLinkCell 的实例
```

### 别名

只有 7.3 或更高版本 可以使用别名

```txt
Tem = TrawpawExecutionMethod
Thmr = TrawpawHandleModuleResult
Tdt = TrawpawDatatypes
Trst = TrawpawResult
Tfun = TrawpawFunction
Tlc = TrawpawLinkCell
```

## 版本规则

### 标准

```versionrule
<major>.<minor_l1>[.<minor_l2>[.<minor_l3>[...]]][_<patch>][-waste<tag>]
```

### 预发布 & 候选发布

```versionrule
<major>.0-(pre|rc)<minor>[_<patch>][-waste<tag>]
```

## 感谢

- [Waste-Preview](https://github.com/ChenQingMua/WasteLanguage-Preview)
- Brainf\*\*k
