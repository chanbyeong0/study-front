# API 명세서 (최소 필수 + 권장 확장)

Base URL: `${BACKEND_URL}` (기본 `http://localhost:8080`)

공통 헤더:

```http
Content-Type: application/json
```

에러 응답(권장):

```json
{ "error": { "code": "STRING", "message": "설명" } }
```

---

## 1. 방(Rooms)

### 1.1 방 생성

```
POST /api/rooms
```

요청 예:

```json
{ "character": "아인슈타인" }
```

응답 예:

```json
{ "roomId": "0d9b1a1e-9a93-4a7c-9a6e-4b2c1f0f9b10" }
```

### 1.2 방 정보 조회 (권장)

```
GET /api/rooms/{roomId}
```

응답 예:

```json
{
  "roomId": "0d9b1a1e-9a93-4a7c-9a6e-4b2c1f0f9b10",
  "character": "아인슈타인",
  "createdAt": "2025-08-09T12:34:56Z",
  "messageCount": 12
}
```

### 1.3 대화 초기화 (권장)

```
POST /api/rooms/{roomId}/reset
```

응답 예:

```json
{
  "roomId": "0d9b1a1e-9a93-4a7c-9a6e-4b2c1f0f9b10",
  "clearedAt": "2025-08-09T12:40:00Z"
}
```

### 1.4 방 삭제 (선택)

```
DELETE /api/rooms/{roomId}
```

응답 예:

```json
{ "ok": true }
```

---

## 2. 메시지(Messages)

### 2.1 메시지 전송(응답 생성)

```
POST /api/rooms/{roomId}/messages
```

요청 예:

```json
{ "content": "안녕하세요! 시간은 절대적인가요?" }
```

응답 예(최소):

```json
{ "content": "상대성이론에 따르면 시간은 관측자에 따라 상대적입니다..." }
```

응답 예(확장 허용):

```json
{
  "messageId": "msg_12345",
  "role": "assistant",
  "content": "상대성이론에 따르면 시간은 관측자에 따라 상대적입니다...",
  "createdAt": "2025-08-09T12:35:30Z"
}
```

### 2.2 히스토리 조회 (권장)

```
GET /api/rooms/{roomId}/messages?limit=50&before=msg_12345
```

응답 예:

```json
{
  "messages": [
    { "messageId": "msg_1", "role": "user", "content": "...", "createdAt": "..." },
    { "messageId": "msg_2", "role": "assistant", "content": "...", "createdAt": "..." }
  ],
  "hasMore": false
}
```

### 2.3 스트리밍 (선택)

```
GET /api/rooms/{roomId}/messages/stream?content=...
Accept: text/event-stream
```

이벤트 예:

```
event: chunk
data: {"delta":"상대성"}

event: chunk
data: {"delta":"이론은 ..."}

event: done
data: {"messageId":"msg_999","createdAt":"2025-08-09T12:35:30Z"}
```

---

## 3. 캐릭터(선택)

### 3.1 목록

```
GET /api/characters
```

응답 예:

```json
{
  "characters": [
    { "slug": "einstein", "name": "아인슈타인", "emoji": "🧠", "themeColor": "#4CAF50" },
    { "slug": "trump", "name": "트럼프", "emoji": "🇺🇸", "themeColor": "#FF9800" }
  ]
}
```

### 3.2 추천 질문

```
GET /api/characters/{slug}/suggestions
```

응답 예:

```json
{ "suggestions": ["질문1", "질문2", "..."] }
```

---

## 4. 헬스체크(운영 편의)

```
GET /api/health
```

응답 예:

```json
{ "ok": true, "version": "1.0.0", "time": "2025-08-09T12:00:00Z" }
```


