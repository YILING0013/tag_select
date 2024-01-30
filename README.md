
# Flask 标签选择器项目

## 简介
标签选择器是一个基于 Flask 框架的 Web 应用程序，程序集成了蓝图（Blueprint），用于模块化和可重用性。你可以在此基础上不断进行扩展。

[![2024-01-30-103950.png](https://i.postimg.cc/cLp422HR/2024-01-30-103950.png)](https://postimg.cc/v4vs6P5T)*Tag选择*

[![2024-01-30-103532.png](https://i.postimg.cc/qMZ7XzHZ/2024-01-30-103532.png)](https://postimg.cc/D8LF7fZq)*画师选择（带预览图）*

[![2024-01-30-103856.png](https://i.postimg.cc/52Y2Pbx9/2024-01-30-103856.png)](https://postimg.cc/LJSS5dYG)*自定义Tag*

## 功能特点
- **蓝图集成**：使用 Flask 蓝图进行模块化设计。
- **YAML 文件管理**：根据类别动态加载 YAML 文件中的数据。
- **错误处理**：为文件未找到的情况提供适当的错误响应。
- **用户友好界面**：用于选择标签的 Web 界面。

## 项目结构
- `app.py`：主 Flask 应用程序。
- `tag_select.py`：标签选择模块的蓝图文件。
- `templates` 目录：包含 HTML 模板。
- `static` 目录：包含js脚本等内容。
- `tag_yaml` 目录：包含带有标签数据的 YAML 文件。

## 环境要求
- Python 3
- Flask
- PyYAML

## 安装与部署

1. **克隆仓库**：
   将此仓库克隆到本地机器或下载源代码。

   ```
   git clone https://github.com/YILING0013/tag_select.git
   ```

2. **创建虚拟环境**（可选但推荐）：

   ```
   python -m venv venv
   source venv/bin/activate  # Unix 或 MacOS
   venv\Scriptsctivate  # Windows
   ```

3. **安装依赖**：

   ```
   pip install flask PyYAML
   ```

4. **准备 YAML 文件**：将 YAML 文件放置在 `tag_yaml` 目录中。每个文件应对应一个标签类别。

5. **运行应用程序**：
   
   执行以下命令启动 Flask 应用程序：

   ```
   python app.py
   ```

   这将启动 Flask 开发服务器，您应该看到显示服务器正在 `http://127.0.0.1:5000/` 上运行的输出。

6. **访问 Web 界面**：

   打开浏览器，访问 `http://127.0.0.1:5000/` 以使用标签选择界面。

7. **API 使用**：

   要从特定类别获取标签，请使用以下 API 端点：

   ```
   http://127.0.0.1:5000/api_tag/get_tags/<类别>
   ```

   将 `<类别>` 替换为 `tag_yaml` 目录中对应的 YAML 文件的类别名称。

---

本 README 提供了 Flask 标签选择器项目的基本概述和设置指南。根据您的项目的具体需求和背景，进行适当的调整和扩展。
