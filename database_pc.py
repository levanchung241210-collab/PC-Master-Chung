
# -*- coding: utf-8 -*-

# =========================================================================
# 1. KHO LỖI WINDOWS & PHẦN CỨNG (HỖ TRỢ FIX HÀNG NGÀN HIỆN TƯỢNG VÀ MÃ SỐ HIỆU)
# =========================================================================
LOI_HE_THONG = {
    # --- Nhóm mã màn hình xanh chuyên sâu (BSOD) ---
    "memory_management": {
        "ten": "Màn hình xanh MEMORY_MANAGEMENT",
        "loai": "Chuyên sâu",
        "nguyen_nhan": "Lỗi hệ thống quản lý bộ nhớ, RAM bị xung đột Bus, hỏng chip nhớ hoặc chân cắm bị oxy hóa bụi bẩn.",
        "giai_phap": [
            "Bước 1: Tắt máy hoàn toàn, rút dây nguồn. Tháo toàn bộ các thanh RAM ra ngoài.",
            "Bước 2: Dùng cục tẩy học sinh cọ thật sạch các chân tiếp xúc màu vàng của RAM, thổi bụi ở khe cắm trên Mainboard.",
            "Bước 3: Cắm lại từng thanh RAM vào từng khe riêng biệt để kiểm tra loại trừ (loại bỏ thanh hoặc khe bị hỏng).",
            "Bước 4: Nếu máy lên, vào Windows mở Start menu gõ 'Windows Memory Diagnostic' (hoặc lệnh mdsched.exe) để quét sâu lỗi RAM."
        ]
    },
    "page_fault_in_nonpaged_area": {
        "ten": "Màn hình xanh PAGE_FAULT_IN_NONPAGED_AREA",
        "loai": "Chuyên sâu",
        "nguyen_nhan": "Hệ thống tìm kiếm dữ liệu trong bộ nhớ nhưng không tồn tại. Thường do ổ cứng (HDD/SSD) bị bad sector nặng hoặc driver hệ thống bị lỗi.",
        "giai_phap": [
            "Bước 1: Tải và bật phần mềm CrystalDiskInfo kiểm tra trạng thái sức khỏe (Health) của ổ cứng xem có bị cảnh báo Vàng/Đỏ không.",
            "Bước 2: Click chuột phải vào nút Start, chọn Terminal/CMD (Admin), gõ lệnh 'chkdsk /f /r' để quét và tự vá lỗi phân vùng.",
            "Bước 3: Nếu dính lỗi sau khi nâng cấp phần cứng, hãy gỡ cài đặt driver vừa cập nhật (VGA, Chipset) trong Device Manager."
        ]
    },
    "critical_process_died": {
        "ten": "Màn hình xanh CRITICAL_PROCESS_DIED",
        "loai": "Chuyên sâu",
        "nguyen_nhan": "Một tiến trình cốt lõi cấu thành nên Windows bị dừng đột ngột do xung đột phần mềm nặng, lỗi file hệ thống hoặc dính virus cắn nát hệ điều hành.",
        "giai_phap": [
            "Bước 1: Mở CMD với quyền Administrator, chạy lệnh 'sfc /scannow' để quét và khôi phục các file core của Windows.",
            "Bước 2: Chạy tiếp lệnh 'DISM.exe /Online /Cleanup-image /Restorehealth' để sửa lỗi sâu từ bản image Windows.",
            "Bước 3: Gỡ bỏ các phần mềm bẻ khóa (Crack), phần mềm dọn rác máy tính vừa cài gần đây."
        ]
    },
    "system_service_exception": {
        "ten": "Màn hình xanh SYSTEM_SERVICE_EXCEPTION",
        "loai": "Chuyên sâu",
        "nguyen_nhan": "Xung đột trực tiếp giữa mã nguồn hệ điều hành với Driver thiết bị (thường do driver card màn hình hoặc phần mềm diệt virus bên thứ 3).",
        "giai_phap": [
            "Bước 1: Cập nhật Driver Card màn hình (NVIDIA/AMD) lên bản mới nhất ổn định.",
            "Bước 2: Nếu có cài phần mềm diệt virus ngoài (như Avast, Kaspersky), hãy gỡ bỏ hoàn toàn và dùng Windows Defender mặc định.",
            "Bước 3: Kiểm tra các bản cập nhật Windows Update còn sót và cài đặt hết."
        ]
    },

    # --- Nhóm mã số hiệu lỗi (Error Code) ---
    "0xc0000005": {
        "ten": "Mã lỗi phần mềm 0xc0000005 (Access Violation)",
        "loai": "Cơ bản",
        "nguyen_nhan": "Ứng dụng hoặc game cố tình truy cập và chiếm dụng vào vùng RAM không được phép, hoặc file thực thi .exe bị lỗi corrupt.",
        "giai_phap": [
            "Bước 1: Tắt các trình diệt virus ngoài và Windows Defender Ransomware Protection tạm thời rồi thử mở lại game.",
            "Bước 2: Vào CMD (Admin) gõ lệnh 'sfc /scannow' để sửa chữa phân vùng lưu trữ file core.",
            "Bước 3: Tải và cài đặt lại toàn bộ các gói thư viện 'Microsoft Visual C++ Redistributable' từ bản 2015 đến nay."
        ]
    },
    "0x80070002": {
        "ten": "Mã lỗi Windows Update 0x80070002",
        "loai": "Cơ bản",
        "nguyen_nhan": "Hệ thống không tìm thấy file cài đặt cập nhật do thư mục tải về tạm thời của Windows Update bị lỗi cấu trúc hoặc file bị thiếu.",
        "giai_phap": [
            "Bước 1: Nhấn tổ hợp phím Windows + R, gõ 'services.msc', tìm dịch vụ 'Windows Update', chuột phải chọn 'Stop'.",
            "Bước 2: Truy cập đường dẫn C:\\Windows\\SoftwareDistribution\\Download và tiến hành xóa sạch mọi file bên trong thư mục này.",
            "Bước 3: Quay lại bảng Services, chuột phải vào 'Windows Update' chọn 'Start' rồi tiến hành bấm Check for Update lại."
        ]
    },
    "0x800f081f": {
        "ten": "Mã lỗi .NET Framework 0x800f081f",
        "loai": "Cơ bản",
        "nguyen_nhan": "Windows Update không thể tìm thấy các file mã nguồn cần thiết để kích hoạt tính năng .NET Framework (yêu cầu để chạy game/phần mềm cũ).",
        "giai_phap": [
            "Bước 1: Tải file ISO Windows đúng với phiên bản máy đang dùng, mount vào ổ đĩa ảo.",
            "Bước 2: Mở CMD (Admin) gõ lệnh: 'dism /online /enable-feature /featurename:NetFX3 /All /Source:X:\\sources\\sxs /LimitAccess' (Thay X bằng ký tự ổ đĩa ảo).",
            "Bước 3: Đợi chạy đến 100% rồi khởi động lại máy tính."
        ]
    },

    # --- Nhóm lỗi hiện tượng thực tế (Keyword Matching) ---
    "màn hình đen": {
        "ten": "Lỗi máy lên nguồn, quạt quay nhưng Màn Hình Đen xì",
        "loai": "Cơ bản",
        "nguyen_nhan": "Mất tín hiệu xuất hình từ GPU sang màn hình, lỏng dây cáp hoặc Driver card đồ họa bị treo cứng đơ.",
        "giai_phap": [
            "Bước 1: Nhấn tổ hợp phím tắt 'Ctrl + Shift + Windows + B' để ép Windows khởi động lại trình điều khiển card đồ họa (máy sẽ bíp nhẹ 1 tiếng).",
            "Bước 2: Kiểm tra xem dây cáp (HDMI/DisplayPort) đã cắm đúng vào cổng xuất hình của Card rời (nằm phía dưới) chưa, tránh cắm nhầm lên cổng của Mainboard (phía trên).",
            "Bước 3: Tháo pin CMOS hình tròn trên bo mạch chủ ra ngoài khoảng 5 phút, lắp lại để đưa cài đặt BIOS về mặc định gốc."
        ]
    },
    "mất mạng": {
        "ten": "Lỗi mất mạng Internet (Chấm than vàng hoặc quả cầu vỡ)",
        "loai": "Cơ bản",
        "nguyen_nhan": "Địa
