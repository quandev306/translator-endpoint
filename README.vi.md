# NLLB Translator

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
- Đặt `TRANSLATOR_MODEL` (hoặc `MODEL_NAME`) để thay mô hình, ví dụ `TRANSLATOR_MODEL=facebook/nllb-200-distilled-1.3B`.
- Đặt `MAX_INPUT_LENGTH` để giới hạn số token đầu vào (mặc định 512).
- Có thể khai báo các biến này trong file `.env` (ứng dụng tự động nạp bằng python-dotenv).
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
