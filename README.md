# meet

用于按 Word 模板自动产出文档（保留模板中的字体、加粗等样式）。

## 用法

1. 准备模板文件（`.docx`），在模板中使用变量占位符，例如：`{{姓名}}`、`{{项目名称}}`。
2. 准备资料（二选一）：
   - `JSON` 文件：键名与模板变量一致
   - 文本文件：每行一个字段，格式为 `字段: 值` 或 `字段：值`
3. 执行生成：

```bash
python tools/fill_word_template.py \
  --template /absolute/path/template.docx \
  --material-txt /absolute/path/material.txt \
  --output /absolute/path/output.docx
```

或使用 JSON：

```bash
python tools/fill_word_template.py \
  --template /absolute/path/template.docx \
  --data-json /absolute/path/data.json \
  --output /absolute/path/output.docx
```

> 依赖安装：`pip install -r requirements.txt`
