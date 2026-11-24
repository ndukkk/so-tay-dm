# Quy trình bảo trì Sổ tay Design Manager

Repo này chứa **bản công khai** (`index.html`) của Sổ tay. **Bản chính** là một artifact riêng tư trên claude.ai (mã artifact được ghi trong nhiệm vụ định kỳ). Mọi thay đổi nội dung được thực hiện trên bản chính, sau đó tạo lại bản công khai bằng `tools/build_static.py`.

## Dữ liệu nằm ở đâu trong bản chính
Toàn bộ nội dung là các hằng số JavaScript trong thẻ `<script>` cuối trang:
- `LAW`: danh mục văn bản (tên, ngày hiệu lực, tình trạng `on`/`chg`/`std`, trích yếu, link nguồn).
- `STEPS`: 9 bước chung của vòng đời dự án; mỗi bước tham chiếu văn bản qua khóa trong `LAW`.
- `TYPES`: 5 loại dự án, ghi chú và bước riêng của từng loại.
- `FG`: nhóm nguy hiểm cháy theo QCVN 06 (đã đối chiếu Bảng 6).
- Phần mô tả văn bản ở mục `#van-ban` (đoạn "Ba thay đổi lớn…").
- `RULES`, `KIN` và hàm `calcPop`, `calcK`: mục Tính nhanh (dân số nhà chung cư theo quyết định địa phương; chỗ đỗ xe theo QCVN 04:2021 và QCVN 01:2021 Bảng 2.19). Khi QCVN 01:2026/BXD có hiệu lực (01/01/2027) hoặc quyết định địa phương thay đổi, cập nhật chỉ tiêu tại đây và câu ghi chú cuối mục.
- Khối mã máy tính phải nằm TRƯỚC dòng `/* case library on db */`, vì `build_static.py` cắt bỏ phần từ dòng đó trở xuống.

## Nguyên tắc khi cập nhật văn bản pháp lý
1. Chỉ ghi nhận văn bản đã được ban hành chính thức, có số hiệu và ngày hiệu lực kiểm chứng được từ nguồn chính thống (chinhphu.vn, moc.gov.vn, vbpl.vn, congbao.chinhphu.vn) hoặc nguồn pháp luật uy tín (thuvienphapluat.vn, luatvietnam.vn).
2. Dự thảo, văn bản đang lấy ý kiến hoặc đang được Quốc hội thảo luận: chỉ đánh dấu `chg` và ghi chú, không thay nội dung đang hiệu lực.
3. Văn bản bị thay thế: cập nhật trích yếu và các bước liên quan, ghi rõ văn bản cũ hết hiệu lực từ ngày nào.
4. Chỉ gắn link đã mở được; không tự dựng đường dẫn.
5. Không ghi ngày rà soát lên giao diện. Ngày rà soát chỉ cập nhật trong trường `reviewed` (dữ liệu ẩn cho khung hỏi Claude).
6. Bản chính dùng giọng xưng hô thân mật; bản công khai do `build_static.py` chuyển sang văn phong chuyên môn. Nếu script báo `MISS`, cập nhật danh sách thay thế trong script cho khớp.
7. Ghi mỗi lần cập nhật vào `CHANGELOG.md` (ngày, văn bản mới, thay đổi, nguồn).

## Kiểm tra trước khi đẩy
- `node --check` cho phần script của cả hai bản.
- Mở bản công khai bằng trình duyệt không giao diện ở khổ 1240px và 390px: không lỗi script, không cuộn ngang.
