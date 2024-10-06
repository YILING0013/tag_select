以下是修改后的 Markdown 文档，添加了关于翻译 API 的配置说明，并调整了安装方法：

---

# Flask 标签选择器项目

## 简介

标签选择器是一个基于 Flask 框架的 Web 应用程序，程序集成了蓝图（Blueprint），用于模块化和可重用性。该项目允许用户选择不同的标签类别，并提供可扩展的翻译 API 集成。项目改编自 [NovelAI-tag-generator](https://github.com/WolfChen1996/NovelAI-tag-generator)。

[![2024-01-30-103950.png](https://i.postimg.cc/cLp422HR/2024-01-30-103950.png)](https://postimg.cc/v4vs6P5T) *Tag选择*

[![2024-01-30-103532.png](https://i.postimg.cc/qMZ7XzHZ/2024-01-30-103532.png)](https://postimg.cc/D8LF7fZq) *画师选择（带预览图）*

[![2024-01-30-103856.png](https://i.postimg.cc/52Y2Pbx9/2024-01-30-103856.png)](https://postimg.cc/LJSS5dYG) *自定义Tag*

## 体验网站

- **网站地址**：https://idlecloud.cc/

## 功能特点

- **蓝图集成**：使用 Flask 蓝图进行模块化设计。
- **YAML 文件管理**：根据类别动态加载 YAML 文件中的数据。
- **错误处理**：为文件未找到的情况提供适当的错误响应。
- **翻译 API 集成**：支持通过百度翻译 API 对标签进行自动翻译。
- **用户友好界面**：用于选择标签的 Web 界面。

## 项目结构

- `app.py`：主 Flask 应用程序。
- `tag_select.py`：标签选择模块的蓝图文件。
- `translate.py`：集成翻译 API 的模块。
- `templates` 目录：包含 HTML 模板。
- `static` 目录：包含 JavaScript、CSS 文件等。
- `tag_yaml` 目录：包含带有标签数据的 YAML 文件。

## 配置翻译 API

### 1. `config.yaml` 配置

项目支持使用百度翻译 API 进行翻译。请在项目根目录下创建 `config.yaml` 文件，并添加以下内容：

```yaml
baidu_translate_credentials:
  - app_id: 'YOUR_APP_ID_1'
    secret_key: 'YOUR_SECRET_KEY_1'
  - app_id: 'YOUR_APP_ID_2'
    secret_key: 'YOUR_SECRET_KEY_2'
  - app_id: 'YOUR_APP_ID_3'
    secret_key: 'YOUR_SECRET_KEY_3'
```

此配置允许您添加多个百度翻译的 `APP_ID` 和 `SECRET_KEY`，系统会自动轮询这些凭据。

### 2. 翻译 API 调用

在标签选择的过程中，如果需要翻译，可以通过调用内置的翻译 API 来获取翻译结果。每次翻译时，程序会自动轮询不同的 API 密钥

## 环境要求

- Python 3.x
- Flask
- PyYAML
- requests
- BeautifulSoup4
- jieba
- python-Levenshtein

## 安装与部署

### 1. **克隆仓库**：

将此仓库克隆到本地机器或下载源代码：

```bash
git clone https://github.com/YILING0013/tag_select.git
```

### 2. **创建虚拟环境**（可选但推荐）：

```bash
python -m venv venv
source venv/bin/activate  # Unix 或 MacOS
venv\Scripts\activate  # Windows
```

### 3. **安装依赖**：

安装 `requirements.txt` 文件中的依赖项：

```bash
pip install -r requirements.txt
```

### 4. **准备 YAML 文件**：

将 YAML 文件放置在 `tag_json` 目录中。每个文件应对应一个标签类别。

### 5. **配置翻译 API**：

根据上文中的 "配置翻译 API" 步骤，在根目录下创建并配置 `config.yaml` 文件，添加百度翻译的 `APP_ID` 和 `SECRET_KEY`。

### 6. **运行应用程序**：

执行以下命令启动 Flask 应用程序：

```bash
python app.py
```

这将启动 Flask 开发服务器，您可以访问 `http://127.0.0.1:5000/` 以使用标签选择界面。

## API 使用

要从特定类别获取标签，请使用以下 API 端点：

```bash
http://127.0.0.1:5000/api_tag/get_tags/<类别>
```

将 `<类别>` 替换为 `tag_json` 目录中对应的 JSON 文件的类别名称。

---
