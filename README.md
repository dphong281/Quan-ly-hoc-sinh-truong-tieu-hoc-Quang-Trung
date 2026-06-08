                                    📚 Phần mềm Quản lý Học sinh Tiểu học Quang Trung

📝 Giới thiệu
    Ứng dụng Quản lý Học sinh Tiểu học Quang Trung là một phần mềm Desktop được thiết kế để hỗ trợ giáo viên và cán bộ hành 
    chính trong việc số hóa dữ liệu học sinh, giáo viên và điểm số. Với giao diện hiện đại, tốc độ xử lý nhanh và tính năng 
    bảo mật dữ liệu cơ bản, ứng dụng giúp giảm tải khối lượng công việc thủ công, hạn chế sai sót và tối ưu hóa quy trình 
    quản lý tại trường.

✨ Các tính năng chính
    - Quản lý Hồ sơ Học sinh: Thêm, sửa, xóa thông tin học sinh. Hệ thống tự động kiểm soát định dạng tên (không chứa số/ký 
        tự đặc biệt) và mã học sinh duy nhất.
    - Quản lý Giáo viên: Quản lý danh sách giáo viên, bộ môn giảng dạy với tính năng kiểm tra dữ liệu đầu vào chặt chẽ.
    - Quản lý Điểm số:
        + Nhập điểm giữa kỳ và cuối kỳ.
        + Tự động tính toán điểm trung bình cả năm theo công thức quy định.
        + Cơ chế xác thực điểm số (chỉ nhận số từ 0 - 10).
    - Xuất/Nhập dữ liệu (Excel): Hỗ trợ xuất danh sách ra file .xlsx để làm báo cáo hoặc nhập dữ liệu hàng loạt từ Excel vào hệ thống.
    - Tối ưu hóa hiệu năng: Sử dụng cơ chế đa luồng (Threading) kết hợp với Loading Screen, giúp ứng dụng không bị "đơ" hoặc treo khi xử lý hàng nghìn dòng dữ liệu.
    - Cơ chế an toàn (Validation): Ngăn chặn dữ liệu rác, bảo vệ cấu trúc file dữ liệu luôn ổn định.

🛠 Công nghệ sử dụng
    Ngôn ngữ: Python 3.14+
    Thư viện giao diện: CustomTkinter, Tkinter
    Xử lý dữ liệu: Pandas, NumPy, OpenPyXL
    Kiến trúc: Mô hình MVC (Model - View - Controller) giúp code sạch, dễ bảo trì và mở rộng.

🚀 Hướng dẫn cài đặt
    1.Yêu cầu: Đã cài đặt Python.
    2.Cài đặt thư viện: Mở Terminal tại thư mục dự án và chạy lệnh:
        Bash:
            pip install pandas numpy customtkinter openpyxl
    3.Khởi chạy: 
        Bash:
            python main.py

📂 Cấu trúc dự án
    Sanpham/assets/: Chứa các thành phần UI bổ trợ (Loading, Popup).
    Sanpham/common/: Chứa các class định nghĩa giao diện (View).
    Sanpham/model/: Chứa logic thao tác với file dữ liệu (Model).
    Sanpham/page/: Chứa các bộ điều khiển logic (Controller) cho từng chức năng.
    Sanpham/database/hocsinh.csv, giaovien.csv, diemso.csv: Các tệp lưu trữ dữ liệu chính.

💡 Hướng dẫn sử dụng
    Khi nhập liệu: Hãy đảm bảo Mã học sinh/Mã giáo viên là các chữ số. Hệ thống sẽ tự động chặn các thông tin không hợp lệ.
    Khi import Excel: Vui lòng sử dụng file Excel đúng định dạng cấu trúc của ứng dụng (có thể xuất một file mẫu từ ứng dụng để biết cấu trúc cột).
    Khi ứng dụng đang xử lý: Nếu thấy biểu tượng Loading hiện lên, vui lòng chờ trong giây lát để hệ thống hoàn tất xử lý dữ liệu ở luồng ngầm.
🛡 Bảo mật & Lưu ý
    Dữ liệu được lưu trữ tại máy cục bộ. Hãy thường xuyên sao lưu các file .csv ra ổ đĩa ngoài để tránh mất mát dữ liệu do lỗi hệ thống.
    Ứng dụng tích hợp cơ chế bảo vệ giao diện, tránh lỗi xung đột giữa các luồng xử lý. Mọi hành động sai lệch dữ liệu sẽ được thông báo trực tiếp qua messagebox.
    Dự án được xây dựng với mục tiêu tối ưu hóa công tác quản lý cho Trường Tiểu học Quang Trung.