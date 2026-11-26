# AI News & Vocabulary Learning Agent

**Project brief / MVP specification — v1.0**

## 1. Mục tiêu dự án

Xây dựng một hệ thống tự động thu thập các bài báo về AI bằng tiếng Anh, dịch sang tiếng Nhật và tiếng Việt, trích xuất từ vựng chuyên ngành, theo dõi tần suất xuất hiện của từng thuật ngữ và tạo flashcard để học tập.

Mỗi ngày, hệ thống tạo **3 file PDF** từ cùng một tập bài báo:

- **English PDF:** bài báo tiếng Anh gốc, có đánh dấu màu từ vựng.
- **Japanese PDF:** bản dịch tiếng Nhật, có đánh dấu màu tại thuật ngữ tương ứng.
- **Vietnamese PDF:** bản dịch tiếng Việt, không bắt buộc đánh dấu màu.

Số lượng bài báo mỗi ngày cần được cấu hình; ba file PDF là ba phiên bản ngôn ngữ, không phải ba bài báo riêng biệt.

## 2. Luồng hoạt động chính

```text
Daily Scheduler
      ↓
Collect AI News (English)
      ↓
Remove Duplicate Articles & Extract Article Text
      ↓
Extract Technical Vocabulary
      ↓
Translate English → Japanese and Vietnamese
      ↓
Update Vocabulary Memory & Occurrence Counts
      ↓
Assign Colors and Map EN Terms to JP Terms
      ↓
Generate 3 PDF Files
      ↓
Create / Update Flashcards
      ↓
Daily Processing Report
```

Các bước có thể được điều phối bằng một workflow Python. Không cần tạo một AI Agent độc lập cho từng bước. Chỉ dùng LLM ở những công việc cần hiểu ngôn ngữ, như dịch thuật và lựa chọn thuật ngữ; dùng code thông thường cho lưu trữ, đếm, phân loại và tạo file.

## 3. Quy tắc từ vựng và màu sắc

### 3.1. Nguồn thống kê

- Chỉ dùng **bài báo tiếng Anh gốc** làm nguồn chuẩn để trích xuất và đếm thuật ngữ.
- Chỉ đếm các thuật ngữ chuyên ngành đã được Vocabulary Extractor lựa chọn, không đếm mọi từ trong bài báo.
- Không cộng số lần xuất hiện trong bản dịch tiếng Nhật hoặc tiếng Việt vào bộ đếm. Bản dịch chỉ dùng để hiển thị và đối chiếu thuật ngữ.
- Tần suất được tích lũy trên toàn bộ các bài báo đã xử lý, không đặt lại mỗi ngày.

### 3.2. Occurrence-based counting

Đếm **tổng số lần một thuật ngữ xuất hiện** trong nội dung bài báo tiếng Anh đã được làm sạch.

| Lần xuất hiện tích lũy | Màu | Ý nghĩa |
|---:|---|---|
| 1 | Đỏ | Lần đầu xuất hiện |
| 2–5 | Vàng | Đã xuất hiện nhưng tần suất còn thấp |
| Từ 6 trở đi | Xanh | Tần suất cao |

Màu được xác định riêng cho từng lần xuất hiện theo thứ tự đọc. Ví dụ, nếu một thuật ngữ đang có bộ đếm là 4 và xuất hiện thêm 3 lần trong bài mới, ba lần đó lần lượt có màu vàng, xanh, xanh.

### 3.3. Chuẩn hóa thuật ngữ

- Mỗi khái niệm có một `concept_id` duy nhất để liên kết cách diễn đạt tiếng Anh, tiếng Nhật và tiếng Việt.
- Lưu thuật ngữ tiếng Anh chuẩn (`canonical_term`) để nhận diện cùng một thuật ngữ giữa các bài báo.
- Chỉ gộp biến thể như chữ hoa/chữ thường hoặc dạng số nhiều khi xác định được chúng cùng một thuật ngữ; không tự động gộp các từ có liên quan nhưng khác nghĩa.
- Thuật ngữ nhiều từ, ví dụ `Large Language Model`, được tính như một cụm thuật ngữ, không đếm riêng từng từ thành phần.

## 4. Vocabulary Memory — bộ nhớ dài hạn

Bộ nhớ từ vựng phải được lưu trong database, **không phụ thuộc vào lịch sử hội thoại hoặc trí nhớ ngữ cảnh của LLM**. Khi có bài báo mới, hệ thống chỉ xử lý các thuật ngữ trong bài mới và tra cứu database; không quét lại các PDF cũ để tính tần suất.

Thông tin tối thiểu cần lưu:

| Dữ liệu | Mục đích |
|---|---|
| `concept_id` | Định danh khái niệm |
| `canonical_term` | Thuật ngữ tiếng Anh chuẩn |
| `english_term` | Cách viết tiếng Anh |
| `japanese_term` | Thuật ngữ tiếng Nhật |
| `vietnamese_term` | Nghĩa tiếng Việt |
| `occurrence_count` | Tổng số lần xuất hiện tích lũy |
| `first_seen` / `last_seen` | Ngày xuất hiện đầu và gần nhất |
| `category` | Nhóm chuyên ngành, ví dụ AI, ML, LLM |
| `flashcard_id` | ID thẻ đã đồng bộ, nếu có |

Ngoài bảng khái niệm, cần lưu từng occurrence gắn với bài báo và vị trí trong văn bản tiếng Anh. Dữ liệu này giúp hệ thống đánh dấu chính xác từng lần xuất hiện trong PDF và tránh tăng bộ đếm hai lần khi chạy lại một bài báo.

**Nguyên tắc bắt buộc:** một bài báo đã được xử lý không được làm tăng bộ đếm lần thứ hai khi workflow chạy lại. Cần nhận diện bài trùng và lưu dấu từng occurrence đã ghi nhận.

## 5. Dịch thuật và liên kết thuật ngữ

- Dịch nội dung tiếng Anh sang tiếng Nhật và tiếng Việt theo ngữ cảnh.
- Vocabulary Extractor xác định thuật ngữ tiếng Anh và vị trí của chúng trong văn bản gốc.
- Translation step phải trả về cách diễn đạt tương ứng của thuật ngữ trong tiếng Nhật để PDF Generator có thể đánh dấu đúng vị trí.
- Không dùng phép thay thế chuỗi đơn giản để tô màu bản dịch. Một thuật ngữ có thể được dịch khác nhau tùy ngữ cảnh.
- Nếu không xác định chắc chắn vị trí thuật ngữ trong bản tiếng Nhật, đánh dấu mapping cần kiểm tra thay vì tô màu vào vị trí phỏng đoán.

## 6. Đầu ra

### 6.1. Ba PDF mỗi ngày

| File | Nội dung | Highlight |
|---|---|---|
| `AI_News_YYYY-MM-DD_EN.pdf` | Bài báo tiếng Anh gốc | Đỏ / Vàng / Xanh |
| `AI_News_YYYY-MM-DD_JP.pdf` | Bản dịch tiếng Nhật | Màu tương ứng với thuật ngữ EN |
| `AI_News_YYYY-MM-DD_VI.pdf` | Bản dịch tiếng Việt | Không bắt buộc |

PDF cần giữ bố cục dễ đọc và hỗ trợ đúng ký tự tiếng Nhật, tiếng Việt. Có thể hoàn thiện thiết kế và typography sau khi chức năng tạo file hoạt động ổn định.

### 6.2. Flashcards

Ứng dụng flashcard chưa phải quyết định cố định; **Anki + AnkiConnect** là lựa chọn đề xuất ban đầu vì hỗ trợ đồng bộ từ dữ liệu bên ngoài.

Một flashcard nên có:

- Thuật ngữ tiếng Anh.
- Thuật ngữ tiếng Nhật.
- Nghĩa tiếng Việt.
- Định nghĩa hoặc giải thích ngắn.
- Câu ví dụ tiếng Anh và tiếng Nhật.
- Nhóm chuyên ngành và nguồn bài báo.

Đề xuất mặc định cho MVP: tạo thẻ cho từ mới (đỏ) và từ tần suất thấp (vàng); không tạo thẻ mới cho từ xanh đã xuất hiện thường xuyên. Phải kiểm tra `concept_id` trước khi tạo để tránh thẻ trùng.

## 7. Kiến trúc và công nghệ cốt lõi

| Thành phần | Công nghệ đề xuất | Vai trò |
|---|---|---|
| Ngôn ngữ chính | Python | Workflow và xử lý dữ liệu |
| Thu thập bài báo | RSS / nguồn tin có thể truy cập | Lấy bài báo AI tiếng Anh |
| Dịch và chọn thuật ngữ | LLM API | Hiểu ngữ cảnh, dịch, trích xuất thuật ngữ |
| Bộ nhớ từ vựng | SQLite | Lưu khái niệm và occurrence lâu dài |
| Tạo PDF | ReportLab | Xuất ba phiên bản PDF |
| Tự động chạy | APScheduler hoặc Cron | Chạy workflow theo lịch |
| Flashcard | AnkiConnect (đề xuất) | Tạo và cập nhật thẻ |

Không cần database server, vector database, giao diện web hoặc framework multi-agent trong MVP. Có thể bổ sung khi dự án thực sự cần.

## 8. Các nguyên tắc thiết kế quan trọng

1. **Database là nguồn dữ liệu chuẩn:** bộ đếm từ vựng được lưu bền vững trong SQLite, không lưu trong context của Agent.
2. **Đếm bằng code:** quy tắc occurrence và màu sắc phải được xử lý bằng Python, không giao cho LLM tự quyết định.
3. **Chỉ xử lý dữ liệu mới:** không quét lại PDF hoặc toàn bộ lịch sử để tính tần suất.
4. **Không đếm trùng:** bài báo và occurrence đã ghi nhận không được xử lý lại làm tăng bộ đếm.
5. **Tách các bước:** thu thập, dịch, quản lý từ vựng, tạo PDF và đồng bộ flashcard là các module độc lập.
6. **Có thể chạy lại an toàn:** nếu bước đồng bộ flashcard lỗi, không cần chạy lại các bước trước đã hoàn thành.

## 9. Lộ trình triển khai

### Phase 1 — Vocabulary Memory Engine

- Tạo SQLite database.
- Xây dựng Vocabulary Manager và Occurrence Counter.
- Xử lý chuẩn hóa thuật ngữ và phân loại màu.
- Kiểm thử bộ đếm, lưu dữ liệu và chống đếm trùng bằng dữ liệu mẫu.

**Kết quả:** bộ máy từ vựng hoạt động chính xác và giữ được dữ liệu sau khi khởi động lại.

### Phase 2 — News Collection & Vocabulary Extraction

- Thu thập bài báo tiếng Anh từ RSS hoặc nguồn đã chọn.
- Lấy nội dung bài báo và loại bỏ nội dung trang không liên quan.
- Phát hiện bài trùng.
- Trích xuất thuật ngữ chuyên ngành cùng vị trí xuất hiện.
- Cập nhật Vocabulary Memory.

**Kết quả:** hệ thống thu thập bài báo mới và cập nhật tần suất từ vựng.

### Phase 3 — Translation & PDF Generation

- Dịch bài báo sang tiếng Nhật và tiếng Việt.
- Liên kết thuật ngữ tiếng Anh với vị trí tương ứng trong tiếng Nhật.
- Tạo ba PDF và đánh dấu màu trong bản tiếng Anh, tiếng Nhật.

**Kết quả:** bộ tài liệu đọc hàng ngày bằng ba ngôn ngữ.

### Phase 4 — Flashcard Integration

- Kết nối ứng dụng flashcard.
- Tạo thẻ từ dữ liệu Vocabulary Memory.
- Kiểm tra và cập nhật thẻ hiện có, tránh tạo trùng.

**Kết quả:** từ vựng được chuyển tự động thành flashcard.

### Phase 5 — Daily Automation

- Cấu hình lịch chạy tự động.
- Lưu trạng thái từng bước và log lỗi.
- Cho phép chạy lại từ bước thất bại mà không xử lý trùng dữ liệu.
- Tạo báo cáo kết quả mỗi ngày.

**Kết quả:** workflow vận hành tự động và có thể phục hồi khi gặp lỗi.

## 10. Tiêu chí hoàn thành MVP

MVP được xem là đạt yêu cầu khi:

- Có thể xử lý bài báo tiếng Anh và tạo bản dịch tiếng Nhật, tiếng Việt.
- Có thể trích xuất thuật ngữ và đếm chính xác từng occurrence theo quy tắc đã chốt.
- Màu sắc đúng: lần 1 đỏ, lần 2–5 vàng, từ lần 6 xanh.
- Cùng một occurrence được đánh dấu tương ứng trong PDF tiếng Anh và tiếng Nhật khi mapping xác định được.
- Tạo đủ ba file PDF.
- Dữ liệu từ vựng vẫn còn sau khi chương trình khởi động lại.
- Chạy lại cùng một bài báo không làm tăng bộ đếm hoặc tạo flashcard trùng.
- Có thể đồng bộ từ vựng đủ điều kiện sang ứng dụng flashcard.

## 11. Những nội dung để sau MVP

Các hạng mục sau không cần giải quyết ngay vì không ảnh hưởng đến việc chứng minh luồng chức năng cốt lõi:

- Dashboard hoặc giao diện web quản lý.
- Multi-agent framework và phân công sub-agent phức tạp.
- Vector database, RAG và semantic search.
- Thống kê nâng cao, biểu đồ và hệ thống phân tích tiến độ học.
- Tối ưu thiết kế PDF ở mức hoàn thiện cao.
- Hệ thống giám sát, cảnh báo và retry nâng cao.
- Audio, phát âm và bài kiểm tra từ vựng.
- Mở rộng sang nhiều nguồn tin hoặc nhiều chủ đề ngoài AI.

Chỉ bổ sung các hạng mục này khi có nhu cầu thực tế hoặc khi các Phase cốt lõi đã hoạt động ổn định.

---

## Quyết định đã chốt

- **Counting method:** Occurrence-based.
- **Counting source:** bài báo tiếng Anh gốc.
- **Color rules:** lần 1 đỏ; lần 2–5 vàng; từ lần 6 trở đi xanh.
- **Persistent memory:** SQLite database.
- **Daily output:** ba PDF EN / JP / VI.
- **Flashcard integration:** Anki + AnkiConnect là phương án đề xuất, chưa khóa lựa chọn.
