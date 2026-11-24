"""Tạo bản công khai (index.html) từ bản chính của Sổ tay.
Cách dùng: python3 tools/build_static.py <bản_chính.html> <index.html>
In ra MISS nếu một chuỗi cần thay không còn tồn tại trong bản chính."""
import re, sys
SRC=sys.argv[1] if len(sys.argv)>1 else '/home/claude/dm-handbook/index.html'
OUT=sys.argv[2] if len(sys.argv)>2 else '/home/claude/dm-handbook/static/index.html'
MAIN='https://claude.ai/artifact/S5vHq5V1rFkQx35fkJR7xT'
s=open(SRC,encoding='utf-8').read()
def cut_section(s,sid,repl):
    a=s.index(f'<section class="band" id="{sid}">'); b=s.index('</section>',a)+len('</section>')
    return s[:a]+repl+s[b:]
note=lambda sid,h,t:f'<section class="band" id="{sid}"><div class="wrap"><h2>{h}</h2><p>{t}</p><a class="btn" href="{MAIN}">Mở bản chính trên claude.ai</a></div></section>'
s=cut_section(s,'tinh-huong',note('tinh-huong','Thư viện tình huống','Tình huống là ghi chép riêng của mày nên chỉ nằm ở bản chính trên claude.ai, không đưa lên bản công khai này.'))
s=cut_section(s,'hoi',note('hoi','Hỏi Claude','Khung hỏi Claude chỉ chạy trên bản chính, vì nó dùng Claude có sẵn của claude.ai. Bản này là bản dự phòng để tra cứu.'))
# JS: drop case library + ask blocks, and lines touching removed elements
a=s.index('/* case library on db */'); b=s.index('renderChips();setType(cur,true)')
s=s[:a]+s[b:]
s=s.replace("$('#sugg').innerHTML=SUGG.map(q=>`<button type=\"button\">${esc(q)}</button>`).join('');\n","")
s=re.sub(r"\$\('#c-type'\)\.innerHTML=.*?\n","",s)
# head + banner
s=s.replace('<meta name="viewport"','<meta name="robots" content="noindex, nofollow">\n<meta name="viewport"',1)
s=s.replace('<header class="band">',f'<div style="background:var(--ink);color:var(--bg);padding:10px max(5vw,16px);font-size:14px">Bản dự phòng chỉ để tra cứu. Hỏi Claude và thư viện tình huống ở <a href="{MAIN}" style="color:inherit;font-weight:700">bản chính trên claude.ai</a>.</div>\n<header class="band">',1)
s=s.replace('Claude để hỏi ngay trong trang.','Claude để hỏi ở bản chính.')
open(OUT,'w',encoding='utf-8').write(s)
print('built',len(s))

# ---- public, formal edition ----
s=open(OUT,encoding='utf-8').read()
def drop(s,start,end_tag):
    a=s.index(start); b=s.index(end_tag,a)+len(end_tag); return s[:a]+s[b:]
# remove backup banner + header block; keep hidden counters for script
s=drop(s,'<div style="background:var(--ink);color:var(--bg);padding:10px','</div>\n')
s=drop(s,'<header class="band">','</header>')
s=s.replace('<nav aria-label="Mục lục">','<span id="f-steps" hidden></span><span id="f-laws" hidden></span>\n<nav aria-label="Mục lục">',1)
# remove case and ask sections + nav links
s=drop(s,'<section class="band" id="tinh-huong">','</section>')
s=drop(s,'<section class="band" id="hoi">','</section>')
s=s.replace('<a href="#tinh-huong">Tình huống</a>','').replace('<a href="#hoi">Hỏi Claude</a>','')
R=[
 ('Cây quyết định: dự án của mày đi tuyến nào?','Cây quyết định: xác định tuyến pháp lý của dự án'),
 ('Trả lời 6 câu, trang sẽ chỉ ra các nhánh pháp lý phải đi và bước cần mở ra xem.','Trả lời 6 câu hỏi để xác định các nhánh pháp lý áp dụng và các bước cần xem xét.'),
 ('Bấm vào một ga để mở bước đó. Đây là khung chung','Chọn một ga để xem chi tiết bước tương ứng. Đây là khung chung'),
 ('Không thấy. Thử từ khác, hoặc hỏi Claude cuối trang.','Không tìm thấy kết quả phù hợp. Vui lòng thử từ khóa khác.'),
 ("'Hết tuyến. Xem thư viện tình huống để ghi lại bài học của dự án.'","'Đây là bước cuối cùng của tuyến.'"),
 ('<h4>DM cần để ý</h4>','<h4>Lưu ý cho quản lý thiết kế</h4>'),
 ('Không thấy văn bản.','Không tìm thấy văn bản phù hợp.'),
 ('Chốt sai nhóm ở concept là sai dây chuyền tới BCNCKT.','Xác định sai nhóm ở giai đoạn concept sẽ kéo theo sai sót đến hồ sơ BCNCKT.'),
 ('Sales sẽ hỏi DM về mốc móng.','Bộ phận kinh doanh cần mốc này để lập kế hoạch mở bán.'),
 ('<h3>DM phía chủ đầu tư cần làm gì</h3>','<h3>Việc cần làm của quản lý thiết kế phía chủ đầu tư</h3>'),
 ('<h3>Câu hỏi khi phỏng vấn chủ đầu tư khách sạn</h3>','<h3>Câu hỏi cần làm rõ khi tham gia dự án khách sạn</h3>'),
 ("'Hai trang trên do cá nhân làm, có thể ngưng bất cứ lúc nào. Phần cốt lõi (nhóm F, bộ văn bản PCCC, vòng đời) đã chép vào sổ tay này để không phụ thuộc.'","'Hai công cụ trên do cá nhân phát triển và có thể ngừng hoạt động. Nội dung cốt lõi (nhóm nguy hiểm cháy, bộ văn bản PCCC, vòng đời dự án) đã được tổng hợp trong sổ tay này.'"),
 ("['Rủi ro khi dựa vào trang ngoài',","['Lưu ý khi sử dụng công cụ ngoài',"),
 ("Của Võ Đỗ Hùng, chỉ để tham khảo.","Tác giả: Võ Đỗ Hùng. Chỉ mang tính tham khảo."),
 ("Dùng khi dự án theo hình thức đối tác công tư.","Áp dụng cho dự án theo hình thức đối tác công tư."),
 ("['Mở bảng tính','Dữ liệu mẫu mã VD-, xoá trước khi dùng thật. Tải về được dạng .xlsx.','https://claude.ai/artifact/PkApujUrrjqHhyb9SXPDKT']","['Cách áp dụng','Thiết lập từ tuần đầu dự án, cập nhật trước mỗi cuộc họp kỹ thuật và gửi báo cáo trước cuộc họp với lãnh đạo.']"),
 ('<h3 style="margin-top:28px">Bộ 5 công cụ quản lý thiết kế (bảng tính DM Toolkit)</h3>','<h3 style="margin-top:28px">Bộ 5 công cụ quản lý thiết kế</h3>'),
 ('Tài liệu tham khảo cá nhân, không thay thế tư vấn pháp lý và không dùng làm căn cứ thẩm định.','Bản dự phòng phục vụ tra cứu. Tài liệu chỉ mang tính tham khảo, không thay thế tư vấn pháp lý và không dùng làm căn cứ thẩm định.'),
 ("Tuyến chính: '","Tuyến chính: '"),
 ("'Chưa có 1/500: lập quy hoạch","'Chưa có quy hoạch 1/500: lập quy hoạch"),
 ("Kiểm tra ngay tình trạng 1/500 với phòng pháp lý: đây là đầu vào của mọi việc thiết kế.","Cần xác minh tình trạng quy hoạch 1/500 với bộ phận pháp lý, vì đây là đầu vào của toàn bộ công tác thiết kế."),
 ("Đã có 1/500: đọc kỹ chỉ tiêu","Đã có quy hoạch 1/500: rà soát kỹ chỉ tiêu"),
 ("Thiết kế lệch chỉ tiêu thì phải điều chỉnh quy hoạch.","Thiết kế sai khác chỉ tiêu sẽ phải điều chỉnh quy hoạch."),
 ("Xác định cấp công trình sớm: nó quyết định BIM, thẩm tra và thẩm quyền thẩm định.","Cần xác định cấp công trình sớm, vì cấp công trình quyết định yêu cầu BIM, thẩm tra và thẩm quyền thẩm định."),
 ("Khách mua tự sửa mặt tiền, phá vỡ tổng thể.","Người mua tự cải tạo mặt tiền, ảnh hưởng tính thống nhất kiến trúc."),
 ("Chốt sớm phương án bán: nền, thô hay hoàn thiện.","Cần chốt sớm phương án kinh doanh: bán nền, bán nhà thô hay bán nhà hoàn thiện."),
 ("Đọc kỹ trước khi giao nhiệm vụ cho tư vấn.","Cần rà soát kỹ trước khi giao nhiệm vụ cho tư vấn."),
 ("Hỏi sớm địa phương chọn hình thức nào.","Cần làm việc sớm với địa phương về hình thức thực hiện."),
]
R.append(("Sales mở bán trước khi đủ điều kiện; móng trễ làm trễ cả dòng tiền.","Mở bán trước khi đủ điều kiện pháp lý; chậm nghiệm thu móng làm chậm dòng tiền dự án."))
for a,b in R:
    if a not in s: print('MISS',a[:50])
    s=s.replace(a,b)
open(OUT,'w',encoding='utf-8').write(s)
print('formal edition built')
