# NLLB Translator

> Select a language below to view the documentation inline. Each section expands on click (GitHub-friendly i18n tabs without JavaScript).

<div align="center">
<a href="#lang-vi">🇻🇳 Tiếng Việt</a> ·
<a href="#lang-en">🇬🇧 English</a> ·
<a href="#lang-ja">🇯🇵 日本語</a> ·
<a href="#lang-ko">🇰🇷 한국어</a> ·
<a href="#lang-zh">🇨🇳 中文</a> ·
<a href="#lang-de">🇩🇪 Deutsch</a>
</div>

---

<details id="lang-vi" open>
<summary><strong>🇻🇳 Tiếng Việt</strong></summary>

## Giới thiệu
- Dịch máy đa ngôn ngữ dựa trên mô hình [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) (hơn 200 cặp ngôn ngữ).
- Triển khai bằng FastAPI, trả về JSON giữ nguyên ký tự Unicode (giữ nguyên dấu tiếng Việt).
- Tùy chọn thay mô hình qua biến môi trường `MODEL_NAME`.

## Yêu cầu
- Docker và Docker Compose (v3.9 trở lên).
- Ít nhất 4 GB RAM cho container, CPU 2 vCPU để suy luận ổn định.

## Khởi chạy bằng Docker Compose
1. `docker compose up -d`
2. Dịch vụ lắng nghe tại `http://localhost:1111`

Để dừng dịch vụ: `docker compose down`

## API
- `GET /translate`
- Tham số truy vấn:
  - `q` (bắt buộc): nội dung cần dịch. Có thể dùng `text` như alias.
  - `src`: mã ngôn ngữ nguồn (mặc định `eng_Latn`).
  - `tgt`: mã ngôn ngữ đích (mặc định `vie_Latn`).

Ví dụ:

```bash
curl "http://localhost:1111/translate?q=Hola&src=spa_Latn&tgt=eng_Latn"
```

Phản hồi mẫu:

```json
{
  "source": "Hola",
  "translated": "Hello"
}
```

## Cấu hình nâng cao
- Đặt `MODEL_NAME` để thay mô hình, ví dụ `MODEL_NAME=facebook/nllb-200-distilled-1.3B`.
- Container tự động phát hiện các mã ngôn ngữ hợp lệ từ tokenizer; nếu `src` hoặc `tgt` không nằm trong danh sách này, API sẽ trả lỗi HTTP 400.

## Ghi chú
- Endpoint hiện tại chỉ trả về bản dịch một câu/đoạn; độ dài đầu vào bị giới hạn ở 512 token.
- Khi thay mô hình, đảm bảo tokenizer có trường `lang_code_to_id` hoặc cung cấp danh sách ngôn ngữ tương thích để ánh xạ đúng mã `src`/`tgt`.

## Hướng dẫn sử dụng
1. Khởi động dịch vụ: `docker compose up -d`.
2. Gửi yêu cầu dịch thông qua `curl`, Postman hoặc bất kỳ HTTP client nào.
3. Theo dõi log (tùy chọn): `docker compose logs -f translator`.
4. Dừng dịch vụ khi không dùng nữa: `docker compose down`.

## Tác giả
- Lê Ngọc Anh Quân (<quan.dev.30.06.2001@gmail.com>)

</details>

---

<details id="lang-en">
<summary><strong>🇬🇧 English</strong></summary>

## Overview
- Multilingual machine translation powered by [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) covering 200+ language pairs.
- Built with FastAPI and returns Unicode-safe JSON responses.
- Replace the underlying model via the `MODEL_NAME` environment variable.

## Requirements
- Docker and Docker Compose (v3.9+).
- At least 4 GB RAM and 2 vCPUs for smooth inference inside the container.

## Run with Docker Compose
1. `docker compose up -d`
2. Service listens on `http://localhost:1111`

Stop the service with `docker compose down`.

## API
- `GET /translate`
- Query parameters:
  - `q` (required): text to translate. `text` is accepted as an alias.
  - `src`: source language code (default `eng_Latn`).
  - `tgt`: target language code (default `vie_Latn`).

Example:

```bash
curl "http://localhost:1111/translate?q=Hola&src=spa_Latn&tgt=eng_Latn"
```

Sample response:

```json
{
  "source": "Hola",
  "translated": "Hello"
}
```

## Advanced Configuration
- Set `MODEL_NAME` to switch models, e.g. `MODEL_NAME=facebook/nllb-200-distilled-1.3B`.
- The container discovers supported language codes from the tokenizer; unsupported `src`/`tgt` values trigger HTTP 400.

## Notes
- Endpoint currently handles one sentence/paragraph per request with an input cap of 512 tokens.
- When swapping models, make sure the tokenizer exposes `lang_code_to_id` or provides a compatible language list for `src`/`tgt`.

## Usage Guide
1. Start the service: `docker compose up -d`.
2. Send translation requests via `curl`, Postman, or any HTTP client.
3. (Optional) Tail logs: `docker compose logs -f translator`.
4. Stop the service when done: `docker compose down`.

## Author
- Lê Ngọc Anh Quân (<quan.dev.30.06.2001@gmail.com>)

</details>

---

<details id="lang-ja">
<summary><strong>🇯🇵 日本語</strong></summary>

## 概要
- [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) を利用した多言語機械翻訳（200以上の言語ペアに対応）。
- FastAPI で実装され、Unicode を保持した JSON レスポンスを返します。
- `MODEL_NAME` 環境変数で使用するモデルを切り替えられます。

## 前提条件
- Docker と Docker Compose (v3.9 以上)。
- コンテナ内で安定して推論するには 4 GB 以上の RAM と 2 vCPU が必要です。

## Docker Compose で起動
1. `docker compose up -d`
2. サービスは `http://localhost:1111` で待ち受けます。

停止するには `docker compose down` を実行します。

## API
- `GET /translate`
- クエリパラメータ:
  - `q`（必須）: 翻訳するテキスト。エイリアスとして `text` も利用できます。
  - `src`: ソース言語コード（デフォルト `eng_Latn`）。
  - `tgt`: ターゲット言語コード（デフォルト `vie_Latn`）。

例:

```bash
curl "http://localhost:1111/translate?q=Hola&src=spa_Latn&tgt=eng_Latn"
```

レスポンス例:

```json
{
  "source": "Hola",
  "translated": "Hello"
}
```

## 高度な設定
- `MODEL_NAME` を設定してモデルを変更できます（例: `MODEL_NAME=facebook/nllb-200-distilled-1.3B`）。
- コンテナは tokenizer から対応言語コードを自動検出します。`src` または `tgt` が範囲外の場合は HTTP 400 を返します。

## 注意事項
- 現在のエンドポイントはリクエストごとに 1 文（または 1 段落）のみを処理し、入力は最大 512 トークンに制限されます。
- モデルを切り替える際は、tokenizer が `lang_code_to_id` を提供しているか、`src`/`tgt` に対応する言語一覧を用意してください。

## 使い方ガイド
1. サービスを起動: `docker compose up -d`
2. `curl`、Postman などの HTTP クライアントで翻訳リクエストを送信。
3. （任意）`docker compose logs -f translator` でログを確認。
4. 利用後は `docker compose down` で停止。

## 作者
- Lê Ngọc Anh Quân (<quan.dev.30.06.2001@gmail.com>)

</details>

---

<details id="lang-ko">
<summary><strong>🇰🇷 한국어</strong></summary>

## 개요
- [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) 기반 다국어 기계 번역으로 200개 이상의 언어 쌍을 지원합니다.
- FastAPI로 구현되어 있으며 Unicode 문자를 그대로 유지한 JSON 응답을 제공합니다.
- `MODEL_NAME` 환경 변수를 통해 사용 모델을 변경할 수 있습니다.

## 요구 사항
- Docker 및 Docker Compose(v3.9 이상).
- 컨테이너에서 안정적으로 추론하려면 최소 4 GB RAM과 2 vCPU가 필요합니다.

## Docker Compose로 실행
1. `docker compose up -d`
2. 서비스는 `http://localhost:1111` 에서 대기합니다.

중지하려면 `docker compose down` 을 실행합니다.

## API
- `GET /translate`
- 쿼리 파라미터:
  - `q` (필수): 번역할 텍스트. `text` 별칭도 허용됩니다.
  - `src`: 소스 언어 코드(기본값 `eng_Latn`).
  - `tgt`: 대상 언어 코드(기본값 `vie_Latn`).

예시:

```bash
curl "http://localhost:1111/translate?q=Hola&src=spa_Latn&tgt=eng_Latn"
```

응답 예시:

```json
{
  "source": "Hola",
  "translated": "Hello"
}
```

## 고급 설정
- `MODEL_NAME` 값을 지정해 다른 모델을 사용할 수 있습니다 (예: `MODEL_NAME=facebook/nllb-200-distilled-1.3B`).
- 컨테이너는 tokenizer에서 지원 언어 코드를 자동으로 감지하며, 범위 밖의 `src`/`tgt` 는 HTTP 400 오류를 반환합니다.

## 참고
- 현재 엔드포인트는 요청당 한 문장 또는 문단만 처리하며, 입력은 최대 512 토큰으로 제한됩니다.
- 모델을 교체할 때는 tokenizer가 `lang_code_to_id` 를 제공하거나 `src`/`tgt` 에 맞는 언어 목록을 준비해야 합니다.

## 사용 가이드
1. 서비스 시작: `docker compose up -d`
2. `curl`, Postman 등 HTTP 클라이언트로 번역 요청 전송
3. (선택) `docker compose logs -f translator` 로 로그 확인
4. 종료 시 `docker compose down` 실행

## 작성자
- Lê Ngọc Anh Quân (<quan.dev.30.06.2001@gmail.com>)

</details>

---

<details id="lang-zh">
<summary><strong>🇨🇳 中文</strong></summary>

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
- 通过设置 `MODEL_NAME` 更换模型，例如 `MODEL_NAME=facebook/nllb-200-distilled-1.3B`。
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

</details>

---

<details id="lang-de">
<summary><strong>🇩🇪 Deutsch</strong></summary>

## Überblick
- Mehrsprachige maschinelle Übersetzung mit [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M), unterstützt über 200 Sprachpaare.
- Implementiert mit FastAPI und liefert JSON-Antworten, die Unicode-Zeichen erhalten.
- Über die Umgebungsvariable `MODEL_NAME` lässt sich das zugrunde liegende Modell austauschen.

## Voraussetzungen
- Docker und Docker Compose (ab Version 3.9).
- Für stabile Inferenz im Container werden mindestens 4 GB RAM und 2 vCPUs empfohlen.

## Start mit Docker Compose
1. `docker compose up -d`
2. Der Dienst lauscht auf `http://localhost:1111`.

Anhalten mit `docker compose down`.

## API
- `GET /translate`
- Query-Parameter:
  - `q` (erforderlich): Zu übersetzender Text. Alias `text` wird akzeptiert.
  - `src`: Quellsprache (Standard `eng_Latn`).
  - `tgt`: Zielsprache (Standard `vie_Latn`).

Beispiel:

```bash
curl "http://localhost:1111/translate?q=Hola&src=spa_Latn&tgt=eng_Latn"
```

Beispielantwort:

```json
{
  "source": "Hola",
  "translated": "Hello"
}
```

## Erweiterte Konfiguration
- Mit `MODEL_NAME` können Sie ein anderes Modell setzen, z. B. `MODEL_NAME=facebook/nllb-200-distilled-1.3B`.
- Der Container ermittelt unterstützte Sprachcodes automatisch über den Tokenizer; ungültige `src`/`tgt` Werte führen zu HTTP 400.

## Hinweise
- Der Endpunkt verarbeitet pro Anfrage einen Satz oder Absatz; die Eingabe ist auf 512 Tokens begrenzt.
- Beim Modellwechsel sollte der Tokenizer `lang_code_to_id` bereitstellen oder eine kompatible Sprachenliste für `src`/`tgt` liefern.

## Anleitung
1. Dienst starten: `docker compose up -d`.
2. Übersetzungsanfragen per `curl`, Postman oder einem anderen HTTP-Client senden.
3. (Optional) Logs verfolgen: `docker compose logs -f translator`.
4. Dienst beenden: `docker compose down`.

## Autor
- Lê Ngọc Anh Quân (<quan.dev.30.06.2001@gmail.com>)

</details>
