# NLLB Translator

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
- `TRANSLATOR_MODEL` (또는 호환용 `MODEL_NAME`) 값을 지정해 다른 모델을 사용할 수 있습니다 (예: `TRANSLATOR_MODEL=facebook/nllb-200-distilled-1.3B`).
- `MAX_INPUT_LENGTH` 값을 설정해 입력 토큰 길이 상한을 조정합니다 (기본값 512).
- python-dotenv 을 통해 `.env` 파일에 설정한 환경 변수를 자동으로 불러옵니다.
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
