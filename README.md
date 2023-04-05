# chatgpt_termnial
这个仓库的目的是改善在网页上使用 ChatGPT 的不便之处, 以便可以在终端快速的与 ChatGPT 进行交互, 提供更稳定的交互体验。使用 [OpenAI](https://github.com/openai/openai-python) 提供的 Python 包以及每个账户的免费额度($18 期限3个月)。用户可以通过管道方式将文本数据传输给 ChatGPT 进行处理，也可以通过交互式方式进行提问，或者仅仅向 ChatGPT 提出一个问题。

## 使用方法
- [echo "question" |] chatgpt [-i] "translate chinese"
  - 选项[-i] 表示进入交互命令行, 不加则回答完后程序结束
  - 管道给 chatgpt
- 注意事项
  - 要能连接外网

example
```sh
echo "衬衫的价格为9榜15便士" | chatgpt "给我讲讲这个出自哪里" -i
```
![](./images/chatgpt.gif)

## 配置介绍

1. `pip3 install openai`
2. [openai 官网生成 api-keys](https://platform.openai.com/account/api-keys)
3. chatgpt.py 57行左右处替换自己的 key
```
chatgpt "ask your question"
chatgpt -i  # 进入交互模式 
使用 Ctrl-Z(win) 或 Ctrl-D(unix) 结束输入
Ctrl-C 退出
```

### Windows
- `vim $PROFILE` 添加下面这个自定义函数
- 修改 `$path` 为自己的路径
- `. $PROFILE` 刷新配置文件
```
function chatgpt {
  begin {
    $variable = ""
    $path = "C:\Users\XX\scripts\chatgpt.py"
  }
  process {
    if($input) {
      $variable += "`n" + $_
    }else{
      $variable = ""
    }
  }
  end {
    if ($variable -eq $null -or $variable -eq "") {
        python $path $args
    } else {
        python $path $variable $args
    }
  }
}
```

### Linux
- `mv chatapt.py chatapt`
- `chmod a+x chatapt`
- 放置在 $path 路径下

### MacOS
没测试过, 可以尝试 Linux 一样配置


todo
- 清空 message