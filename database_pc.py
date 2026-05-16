# -*- coding: utf-8 -*-

# =========================================================================
# KHO DỮ LIỆU SIÊU CHUYÊN GIA PC - PHÁT TRIỂN BỞI LÊ VĂN CHUNG 10A4
# =========================================================================

# 1. KHO LỖI WINDOWS & PHẦN CỨNG NÂNG CAO (Màn hình xanh, Mã số hiệu, Hiện tượng)
LOI_HE_THONG = {
    "memory_management": {
        "ten": "Màn hình xanh MEMORY_MANAGEMENT (0x0000001A)",
        "loai": "Chuyên sâu",
        "nguyen_nhan": "Lỗi hệ thống quản lý bộ nhớ. RAM bị lỗi chip nhớ, chân cắm bị bụi bẩn, bám ô-xy hóa hoặc xung đột Bus giữa các thanh RAM.",
        "giai_phap": [
            "- Bước 1: Tắt nguồn, rút dây điện. Gạt lẫy tháo toàn bộ thanh RAM ra khỏi bo mạch chủ.",
            "- Bước 2: Dùng cục tẩy học sinh cọ thật sạch các chân vàng tiếp xúc của RAM. Dùng bóng thổi hoặc chổi mềm vệ sinh kỹ khe cắm RAM.",
            "- Bước 3: Nếu cắm nhiều thanh, hãy cắm thử lại ĐƠN LẺ từng thanh vào từng khe rồi bật máy để tìm ra thanh hoặc khe bị hỏng.",
            "- Bước 4: Nếu vào được Windows, nhấn Start gõ 'Windows Memory Diagnostic' để hệ thống quét sâu, phát hiện phần cứng hỏng."
        ]
    },
    "page_fault_in_nonpaged_area": {
        "ten": "Màn hình xanh PAGE_FAULT_IN_NONPAGED_AREA (0x00000050)",
        "loai": "Chuyên sâu",
        "nguyen_nhan": "Hệ thống yêu cầu dữ liệu từ bộ nhớ nhưng không tìm thấy. Nguyên nhân do ổ cứng (HDD/SSD) bị bad sector, lỗi driver card đồ họa hoặc lỗi bộ nhớ đệm L1/L2/L3 của CPU.",
        "giai_phap": [
            "- Bước 1: Khởi động vào chế độ Safe Mode (nếu có thể). Gỡ driver VGA hoặc driver phần cứng vừa cài đặt gần nhất.",
            "- Bước 2: Nhấp chuột phải vào nút Start -> chọn Terminal (Admin) hoặc CMD (Admin). Ghim lệnh 'chkdsk /f /r' rồi nhấn Enter để quét và tự động vá phân vùng ổ cứng.",
            "- Bước 3: Tải phần mềm CrystalDiskInfo để kiểm tra sức khỏe ổ cứng. Nếu báo 'Caution' hoặc 'Bad' thì cần thay SSD mới."
        ]
    },
    "0xc0000005": {
        "ten": "Mã lỗi phần mềm 0xc0000005 (Access Violation Error)",
        "loai": "Cơ bản",
        "nguyen_nhan": "Ứng dụng, phần mềm hoặc game cố tình truy cập dẫm chân vào vùng nhớ RAM không được phép, hoặc tệp tin core hệ thống bị virus/Windows Defender chặn xóa.",
        "giai_phap": [
            "- Bước 1: Tắt phần mềm diệt virus bên thứ ba và tạm thời vô hiệu hóa Real-time Protection của Windows Defender, sau đó mở lại game bằng quyền 'Run as administrator'.",
            "- Bước 2: Mở CMD bằng quyền Admin, gõ lệnh 'sfc /scannow' để Windows tự động tìm kiếm và phục hồi các file hệ thống bị hỏng.",
            "- Bước 3: Cài đặt lại các gói thư viện nền tảng Microsoft Visual C++ Redistributable và DirectX bản mới nhất để sửa lỗi liên kết thư viện động (.dll)."
        ]
    },
    "0x80070002": {
        "ten": "Mã lỗi cập nhật Windows Update 0x80070002",
        "loai": "Cơ bản",
        "nguyen_nhan": "Tiến trình cập nhật Windows thất bại do tệp tin tải về bị hỏng, tải thiếu dữ liệu hoặc dịch vụ (Services) điều khiển cập nhật bị dừng đột ngột.",
        "giai_phap": [
            "- Bước 1: Nhấn tổ hợp phím Windows + R, gõ 'services.msc'. Tìm dịch vụ 'Windows Update', chuột phải chọn 'Restart'.",
            "- Bước 2: Truy cập theo đường dẫn: C:\\Windows\\SoftwareDistribution\\Download. Xóa sạch sành sanh mọi file và thư mục nằm trong này.",
            "- Bước 3: Vào Cài đặt (Settings) -> Windows Update -> Bấm 'Check for updates' để hệ thống tải lại gói cài đặt sạch."
        ]
    },
    "màn hình đen": {
        "ten": "Hiện tượng máy lên nguồn, quạt quay nhưng MÀN HÌNH ĐEN XÌ",
        "loai": "Cơ bản",
        "nguyen_nhan": "Mất tín hiệu xuất hình giữa card màn hình (VGA) và màn hình, lỏng dây nguồn, lỏng dây cáp tín hiệu (HDMI/DisplayPort) hoặc BIOS bị treo cài đặt.",
        "giai_phap": [
            "- Bước 1: Nhấn tổ hợp phím nóng: 'Ctrl + Shift + Windows + B' để ép Windows nạp lại driver card màn hình ngay lập tức (máy sẽ bíp nhẹ một tiếng và chớp màn hình).",
            "- Bước 2: Kiểm tra jack cắm cáp. Rất nhiều người cắm nhầm dây màn hình vào cổng xuất hình trên Mainboard thay vì cắm vào cổng của Card màn hình rời (VGA).",
            "- Bước 3: Tháo dây nguồn, tháo viên pin CMOS hình tròn trên bo mạch chủ ra ngoài trong 5 phút để xả hết điện, đưa cài đặt BIOS về mặc định gốc (Reset BIOS)."
        ]
    }
}

# 2. KHO GIẢI MÃ TIẾNG KÊU BÁO LỖI CỦA MAINBOARD (BIOS Beep Codes)
BEEP_CODES = {
    "1 tít ngắn": {
        "tinh_trang": "Hệ thống vượt qua bài kiểm tra phần cứng (POST) thành công. Mọi linh kiện (CPU, RAM, VGA) đều hoạt động bình thường."
    },
    "tít dài liên tục": {
        "tinh_trang": "Bo mạch chủ không tìm thấy bộ nhớ RAM hoặc RAM bị lỗi kết nối vật lý.",
        "xu_ly": "Tháo toàn bộ RAM ra, dùng tẩy vệ sinh chân vàng thật kỹ, cắm chặt lại vào khe, nghe tiếng 'Cạch' ở 2 đầu lẫy khóa là chuẩn."
    },
    "1 tít dài 3 tít ngắn": {
        "tinh_trang": "Hệ thống lỗi hiển thị. Không nhận diện được Card màn hình rời (VGA), lỗi chip xử lý đồ họa hoặc thiếu nguồn phụ cấp cho VGA.",
        "xu_ly": "Kiểm tra xem đã cắm chặt các đầu nguồn phụ 6-pin/8-pin từ nguồn (PSU) vào card chưa. Tháo card VGA ra, lau sạch chân cắm PCI-E rồi gắn chặt lại."
    },
    "5 tít ngắn": {
        "tinh_trang": "Lỗi bộ vi xử lý trung tâm (CPU). CPU chưa được cấp nguồn, lỏng Socket, quạt tản nhiệt CPU không quay hoặc chân Socket trên mainboard bị cong gãy.",
        "xu_ly": "Kiểm tra dây nguồn 4-pin/8-pin mang chữ 'CPU' ở góc trên bên trái mainboard xem đã cắm chưa. Nếu tự ráp máy, cần nhấc CPU lên để kiểm tra xem chân socket của mainboard có bị cong hay không."
    }
}

# 3. KHO LINH KIỆN PC CHUYÊN SÂU & ĐỘ TƯƠNG THÍCH PHẦN CỨNG
LINH_KIEN_PC = {
    "i5-6500": {
        "ten": "Intel Core i5-6500 (Skylake Architecture)",
        "loai": "CPU (Bộ vi xử lý trung tâm)",
        "thong_so": "4 nhân 4 luồng, Xung nhịp cơ bản 3.2 GHz (Turbo tối đa 3.6 GHz), Bộ nhớ đệm 6MB Cache, Tiến trình 14nm, Điện năng tiêu thụ TDP 65W, tích hợp đồ họa Intel HD Graphics 530.",
        "socket": "LGA1151 (Chỉ chạy các chipset đời 100 và 200 series)",
        "main_tuong_thich": ["H110", "B150", "B250", "Z170", "Z270"],
        "nguon_khuyen_nghi": "Từ 350W công suất thực trở lên (Ví dụ: Antec, Xigmatek, Corsair).",
        "chuyen_gia_tu_van": "Đây là con CPU phân khúc tầm trung thuộc thế hệ thứ 6 của Intel. Điểm mạnh là cực kỳ mát và ăn ít điện. Để tối ưu hóa chi phí tốt nhất cho học sinh, Chung nên ghép cặp em CPU này với các bo mạch chủ dòng phổ thông như H110 (ví dụ H110M-DS2 của Gigabyte hoặc Asus H110M-E). Cấu hình này rất phù hợp làm máy học tập, văn phòng, làm video nhẹ trên CapCut, chơi mượt Liên Quân Mobile trên giả lập và LOL ở mức thiết lập cao."
    },
    "i3-12100f": {
        "ten": "Intel Core i3-12100F (Alder Lake Architecture)",
        "loai": "CPU (Bộ vi xử lý trung tâm)",
        "thong_so": "4 nhân 8 luồng (Sử dụng hoàn toàn 4 nhân hiệu năng cao P-core), Xung nhịp tối đa lên đến 4.3 GHz, Bộ nhớ đệm 12MB Intel Smart Cache, Hỗ trợ RAM DDR4 lẫn DDR5, KHÔNG tích hợp card đồ họa onboard (Hậu tố F).",
        "socket": "LGA1700 (Thế hệ 12, 13, 14)",
        "main_tuong_thich": ["H610", "B660", "B760", "Z690", "Z790"],
        "nguon_khuyen_nghi": "Từ 450W trở lên (Tính toán dựa trên việc đi chung với VGA rời dòng tầm trung).",
        "chuyen_gia_tu_van": "Đây là con chip 'quốc dân' vô địch trong tầm giá rẻ hiện tại. Sức mạnh đơn nhân của nó cực kỳ khủng khiếp, đè bẹp tất cả các dòng i7 thế hệ cũ (từ đời 9 trở xuống). Do không có đồ họa tích hợp, Chung BẮT BUỘC phải cắm kèm card màn hình rời (VGA) thì máy mới xuất hình được nhé. Để tối ưu ngân sách, hãy đi combo i3-12100F + Mainboard H610 để dành tiền đập vào card đồ họa ngon hơn."
    },
    "gtx 1650": {
        "ten": "NVIDIA GeForce GTX 1650",
        "loai": "VGA (Card đồ họa rời)",
        "thong_so": "Dung lượng bộ nhớ 4GB vRAM (Sử dụng chuẩn chuẩn GDDR5 hoặc GDDR6 tốc độ cao), Băng thông bộ nhớ 128-bit, kiến trúc Turing.",
        "nguon_khuyen_nghi": "350W công suất thực. Hầu hết các phiên bản không cần cắm thêm nguồn phụ (Lấy điện trực tiếp từ khe PCI-E 75W trên mainboard).",
        "chuyen_gia_tu_van": "Đây là dòng card rời thuộc phân khúc phổ thông cực kỳ bền bỉ và tiết kiệm điện năng. Ưu điểm lớn nhất là nhiệt độ hoạt động rất mát mẻ và không kén bộ nguồn (nguon noname tầm trung vẫn gánh tốt). Nó rất thích hợp để nâng cấp cho các dàn máy PC cũ (như dàn chạy chip i5-6500) giúp hồi sinh hiệu năng, đủ sức chiến mượt mà các tựa game Esport thịnh hành hiện tại như Valorant, Liên Minh Huyền Thoại, CS2 ở mức thiết lập đồ họa cao trên màn hình Full HD."
    }
}
