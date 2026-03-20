# 🎨 Yolo UNO Extension - Cảm biến màu TCS34725

Mục mở rộng của Yolo UNO cho cảm biến màu sắc **TCS34725**, cải tiến để nhận màu sắc tốt hơn.

> **💡 Code mẫu:** [Xem trên Ohstem App](https://app.ohstem.vn/#!/share/yolouno/3BA32qhAfV7BYGKyNzKZWMDkG1j)

---

## 🤖 Ý tưởng Robotics & STEM

### 1. Robot dò line nhiều màu
Thay vì chỉ dò line đen/trắng thông thường, robot đọc màu vạch để thực hiện lệnh khác nhau:
- 🛑 **Vạch đỏ**: dừng
- 🐢 **Vạch vàng**: giảm tốc
- ➡️ **Vạch xanh**: rẽ

*Dạy học sinh khái niệm "lệnh nhúng trong đường đi" rất trực quan.*

### 2. Robot phân loại vật thể theo màu
Robot dùng băng tải (servo + thanh trượt) đẩy vật vào ô tương ứng với màu sắc. 

*Dạy khái niệm tự động hóa công nghiệp đơn giản nhất.*

### 3. Hệ thống kiểm tra chất lượng sản phẩm (QC)
Băng chuyền mini chở các khối màu qua cảm biến, tự động loại ra khối "lỗi" (màu không đúng tiêu chuẩn). 

*Rất gần với thực tế nhà máy — phù hợp học sinh cấp 3 trở lên.*

### 4. Hệ thống đèn giao thông thích ứng
Cảm biến đọc màu thẻ xe (đỏ/xanh/vàng) đại diện cho loại phương tiện ưu tiên khác nhau, điều chỉnh thời gian đèn tự động. 

*Dạy thuật toán lập lịch.*

### 5. Board game vật lý điều khiển bằng thẻ màu
Mỗi thẻ màu = một lệnh (tiến/lùi/rẽ/nhảy). Học sinh đặt thẻ theo thứ tự để lập trình đường đi cho robot.

*Dạy tư duy thuật toán mà không cần màn hình, phù hợp lứa tuổi tiểu học.*

### 6. Đàn nhạc màu sắc
Mỗi màu phát ra một nốt nhạc khác nhau qua loa/buzzer. Học sinh "chơi nhạc" bằng cách đưa thẻ màu qua cảm biến theo nhịp.

*Giao thoa nghệ thuật + STEM.*

### 7. Trò chơi phản xạ
Màn hình hiển thị màu ngẫu nhiên, học sinh phải đưa đúng thẻ màu đó qua cảm biến càng nhanh càng tốt. Tính điểm, thi đua giữa các nhóm.

---

## 🎮 Ý tưởng Trò chơi & Giáo dục

### 8. Đèn giao thông thật
Làm cột đèn giao thông mini có 3 đèn LED. Học sinh cầm thẻ màu đỏ/vàng/xanh đưa vào cảm biến để điều khiển đèn. Sau đó đổi vai — một bạn điều khiển đèn, các bạn còn lại đi xe đạp/chạy bộ theo hiệu lệnh.

*Vui nhất khi chơi ngoài sân.*

### 9. Simon Says phiên bản màu
Màn hình/đèn hiển thị chuỗi màu ngẫu nhiên (đỏ-xanh-vàng-đỏ...), học sinh phải lặp lại đúng thứ tự bằng cách đưa thẻ màu qua cảm biến. Chuỗi dài dần sau mỗi vòng.

*Luyện trí nhớ ngắn hạn mà không nhàm.*

### 10. Cuộc đua robot màu
Chia đội, mỗi đội có một màu. Khi cảm biến nhận ra màu của đội nào thì robot tiến thêm một bước. Đội nào về đích trước thắng.

*Học sinh thi nhau đưa thẻ vào cảm biến thật nhanh — ồn ào và vui.*

### 11. Robot thú cưng đổi tâm trạng
Làm mặt robot bằng LED matrix hoặc màn hình nhỏ. Đưa thẻ màu vào:
- 🔴 **Đỏ**: mặt tức giận
- 🟡 **Vàng**: mặt vui
- 🟢 **Xanh lá**: mặt ngủ
- 🔵 **Xanh dương**: mặt buồn

Học sinh "dỗ" robot bằng cách tìm đúng màu làm robot vui trở lại. *Dạy nhận biết cảm xúc theo cách rất nhẹ nhàng.*

### 12. Máy cho quái vật ăn
Làm hộp hình miệng quái vật há to. Quái vật "yêu cầu" một màu cụ thể (đèn LED nhấp nháy màu đó). Học sinh tìm đúng thẻ màu nhét vào miệng — quái vật phát âm thanh nhai và "no bụng". Nhét sai thì quái vật kêu ré.

*Cực kỳ hút học sinh tiểu học.*

### 13. Vườn thú màu sắc
Mỗi con thú nhồi bông được gắn thẻ màu riêng. Cảm biến đọc màu → loa kêu đúng tiếng con vật đó + hiển thị tên con vật. Học sinh thi nhau "đánh thức" các con thú.

*Học từ vựng động vật bằng tiếng Anh kết hợp rất tự nhiên.*

### 14. Máy pha màu thần kỳ
Ba lọ nước màu đỏ/xanh/vàng, mỗi lọ có ống nhỏ giọt điều khiển bằng servo. Học sinh chọn màu muốn pha trên màn hình, máy tự nhỏ giọt đúng tỉ lệ vào cốc. Cảm biến đọc màu kết quả và so sánh với mục tiêu.

*Dạy lý thuyết màu sắc cơ bản mà học sinh tự tay làm.*

