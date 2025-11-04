# NLLB Translator

## 概述
- 基于 [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) 的多语种机器翻译，支持 200+ 个语言对。
- 使用 FastAPI 实现，返回保留 Unicode 字符的 JSON 响应。
- 可通过 `MODEL_NAME` 环境变量替换底层模型。

## 环境要求
- Docker 和 Docker Compose（v3.9 及以上）。
- 为确保容器内推理稳定，至少需要 4 GB 内存和 2 个 vCPU。

## 使用 Docker Compose 启动
1. `docker compose up -d`
2. 服务监听 `http://localhost:1111`

停止服务：`docker compose down`

## API
- `GET /translate`
- 查询参数：
  - `q`（必填）：需要翻译的内容，也接受 `text` 作为别名。
  - `src`：源语言代码（默认 `eng_Latn`）。
  - `tgt`：目标语言代码（默认 `vie_Latn`）。

示例：

```bash
curl "http://localhost:1111/translate?q=Hola&src=spa_Latn&tgt=eng_Latn"
```

示例响应：

```json
{
  "source": "Hola",
  "translated": "Hello"
}
```

## 高级配置
- 设置 `TRANSLATOR_MODEL`（兼容保留 `MODEL_NAME`）以更换模型，例如 `TRANSLATOR_MODEL=facebook/nllb-200-distilled-1.3B`。
- 设置 `MAX_INPUT_LENGTH` 以限制输入 token 数量（默认 512）。
- 借助 python-dotenv，可自动加载 `.env` 文件中的这些环境变量。
- 容器会从 tokenizer 自动发现受支持的语言代码；`src`/`tgt` 超出范围时会返回 HTTP 400 错误。

## 注意事项
- 当前端点每次仅处理一个句子或段落，输入长度限制为 512 个 token。
- 更换模型时，请确保 tokenizer 提供 `lang_code_to_id`，或提供与 `src`/`tgt` 兼容的语言列表。

## 使用指南
1. 启动服务：`docker compose up -d`。
2. 通过 `curl`、Postman 或其他 HTTP 客户端发送翻译请求。
3. （可选）查看日志：`docker compose logs -f translator`。
4. 使用结束后运行 `docker compose down` 停止服务。

## 作者
- Lê Ngọc Anh Quân (<quan.dev.30.06.2001@gmail.com>)
