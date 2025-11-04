# NLLB Translator

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
- `TRANSLATOR_MODEL`（互換性のために `MODEL_NAME` も可）を設定してモデルを変更できます（例: `TRANSLATOR_MODEL=facebook/nllb-200-distilled-1.3B`）。
- `MAX_INPUT_LENGTH` を設定して入力トークン数の上限を制御します（デフォルト 512）。
- python-dotenv により `.env` ファイルからこれらの環境変数を自動読み込みできます。
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
