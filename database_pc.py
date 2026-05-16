# -*- coding: utf-8 -*-

# =========================================================================
# KHO SIÊU DỮ LIỆU HỆ CHUYÊN GIA PC ĐA TẦNG - PHÁT TRIỂN BỞI LÊ VĂN CHUNG 10A4
# =========================================================================

# [DANH MỤC 1]: KHO LỖI WINDOWS, MÀN HÌNH XANH (BSOD) & HIỆN TƯỢNG PHẦN CỨNG NÂNG CAO
LOI_HE_THONG = {
    "memory_management": {
        "ten": "Màn hình xanh MEMORY_MANAGEMENT (0x0000001A)",
        "loai": "Chuyên sâu - Phần cứng RAM",
        "nguyen_nhan": "Lỗi nghiêm trọng trong hệ thống quản lý bộ nhớ. RAM bị lỗi chip nhớ vật lý, chân cắm bị bụi bẩn, rỉ sét do oxy hóa, hoặc xung đột thông số Bus/XMP giữa các thanh RAM.",
        "giai_phap": [
            "- Bước 1: Tắt nguồn, rút dây điện. Gạt lẫy tháo toàn bộ thanh RAM ra khỏi bo mạch chủ.",
            "- Bước 2: Dùng cục tẩy học sinh cọ thật sạch các chân vàng tiếp xúc của RAM. Dùng bóng thổi hoặc chổi mềm vệ sinh kỹ khe cắm RAM.",
            "- Bước 3: Nếu cắm nhiều thanh, hãy cắm thử lại ĐƠN LẺ từng thanh vào từng khe rồi bật máy để tìm ra thanh hoặc khe bị lỗi.",
            "- Bước 4: Vào Windows, nhấn Start gõ 'Windows Memory Diagnostic' để hệ thống quét sâu, phát hiện phần cứng hỏng."
        ]
    },
    "page_fault_in_nonpaged_area": {
        "ten": "Màn hình xanh PAGE_FAULT_IN_NONPAGED_AREA (0x00000050)",
        "loai": "Chuyên sâu - Lưu trữ & Driver",
        "nguyen_nhan": "Hệ thống yêu cầu dữ liệu từ bộ nhớ nhưng không tìm thấy. Nguyên nhân do ổ cứng (HDD/SSD) bị bad sector, phân vùng hệ thống bị hỏng, lỗi driver card đồ họa hoặc lỗi bộ nhớ đệm L1/L2/L3 của CPU.",
        "giai_phap": [
            "- Bước 1: Khởi động vào chế độ Safe Mode. Gỡ driver VGA hoặc driver phần cứng vừa cài đặt gần nhất.",
            "- Bước 2: Mở CMD bằng quyền Administrator (Admin), gõ lệnh 'chkdsk /f /r' rồi nhấn Enter để quét và tự động vá phân vùng ổ cứng.",
            "- Bước 3: Tải phần mềm CrystalDiskInfo kiểm tra sức khỏe ổ cứng. Nếu báo 'Caution' hoặc 'Bad' thì cần sao lưu dữ liệu và thay SSD mới."
        ]
    },
    "0xc0000005": {
        "ten": "Mã lỗi phần mềm 0xc0000005 (Access Violation Error)",
        "loai": "Cơ bản - Xung đột phần mềm",
        "nguyen_nhan": "Ứng dụng hoặc game cố tình truy cập dẫm chân vào vùng nhớ RAM không được phép, hoặc tệp tin core hệ thống bị virus phá hoại/Windows Defender chặn xóa nhầm.",
        "giai_phap": [
            "- Bước 1: Tắt phần mềm diệt virus bên thứ ba và tạm thời vô hiệu hóa Real-time Protection của Windows Defender, sau đó mở lại game bằng quyền Admin.",
            "- Bước 2: Mở CMD bằng quyền Admin, gõ lệnh 'sfc /scannow' để Windows tự động tìm kiếm và phục hồi các file hệ thống (.dll) bị hỏng.",
            "- Bước 3: Cài đặt lại các gói thư viện nền tảng Microsoft Visual C++ Redistributable trọn bộ từ năm 2005 đến nay và DirectX bản mới nhất."
        ]
    },
    "dpc_watchdog_violation": {
        "ten": "Màn hình xanh DPC_WATCHDOG_VIOLATION (0x00000133)",
        "loai": "Chuyên sâu - Xung đột Driver phần cứng",
        "nguyen_nhan": "Cơ chế quản lý lệnh (DPC) bị treo quá lâu mà không nhận được phản hồi. Thường do driver ổ cứng SSD dòng NVMe bị cũ, hoặc firmware SSD bị lỗi xung đột với Windows 10/11.",
        "giai_phap": [
            "- Bước 1: Nhấn chuột phải vào nút Start -> Chọn Device Manager.",
            "- Bước 2: Tìm mục 'IDE ATA/ATAPI controllers', chuột phải vào driver điều khiển ổ cứng và chọn 'Update driver'.",
            "- Bước 3: Truy cập trang chủ hãng SSD (Samsung, Kingston, Crucial...) để tải phần mềm quản lý ổ cứng và cập nhật Firmware mới nhất."
        ]
    },
    "critical_process_died": {
        "ten": "Màn hình xanh CRITICAL_PROCESS_DIED (0x000000EF)",
        "loai": "Nghiêm trọng - Lỗi Core Hệ Thống",
        "nguyen_nhan": "Một tiến trình sống còn của hệ điều hành Windows (như csrss.exe, wininit.exe) đột ngột bị đóng hoặc bị hỏng nặng, khiến máy tính lập tức sập để bảo vệ linh kiện.",
        "giai_phap": [
            "- Bước 1: Vào CMD (Admin) gõ liên tục hai lệnh sau để vá sâu: 'DISM.exe /Online /Cleanup-image /Restorehealth' rồi đến 'sfc /scannow'.",
            "- Bước 2: Gỡ cài đặt bản cập nhật Windows (Windows Update) vừa cài đặt gần đây thông qua Control Panel.",
            "- Bước 3: Nếu vẫn bị liên tục, hệ thống đã bị virus cắn nát file hệ điều hành, giải pháp triệt để nhất là cài lại một bản Windows sạch hoàn toàn."
        ]
    },
    "inaccessible_boot_device": {
        "ten": "Màn hình xanh INACCESSIBLE_BOOT_DEVICE (0x0000007B)",
        "loai": "Chuyên sâu - Khởi động & BIOS",
        "nguyen_nhan": "Windows trong quá trình khởi động bị mất liên lạc đột ngột với phân vùng chứa hệ điều hành. Do lỏng cáp SATA, lỗi chip điều khiển ổ cứng, hoặc cấu hình SATA Mode trong BIOS bị đổi sai giữa AHCI và IDE.",
        "giai_phap": [
            "- Bước 1: Khởi động lại máy, bấm liên tục phím Del/F2 để vào BIOS.",
            "- Bước 2: Tìm mục 'SATA Configuration' hoặc 'Storage Controller Mode'. Nếu đang là IDE thì chuyển sang AHCI (hoặc ngược lại) rồi bấm F10 để lưu và khởi động lại.",
            "- Bước 3: Mở thùng máy, rút dây cáp nguồn và cáp dữ liệu SATA của ổ cứng ra, cọ sạch bụi rồi cắm sang một cổng SATA khác trên mainboard."
        ]
    },
    "0x80070002": {
        "ten": "Mã lỗi cập nhật Windows Update 0x80070002",
        "loai": "Cơ bản - Hệ điều hành",
        "nguyen_nhan": "Tiến trình cập nhật Windows thất bại do tệp tin tải về bị hỏng, tải thiếu dữ liệu hoặc dịch vụ (Services) điều khiển cập nhật bị dừng đột ngột.",
        "giai_phap": [
            "- Bước 1: Nhấn tổ hợp phím Windows + R, gõ 'services.msc'. Tìm dịch vụ 'Windows Update', chuột phải chọn 'Restart'.",
            "- Bước 2: Truy cập theo đường dẫn: C:\\Windows\\SoftwareDistribution\\Download. Xóa sạch sành sanh mọi file và thư mục nằm trong này.",
            "- Bước 3: Vào Cài đặt (Settings) -> Windows Update -> Bấm 'Check for updates' để hệ thống tải lại gói cài đặt sạch."
        ]
    },
    "0x800f081f": {
        "ten": "Mã lỗi .NET Framework 0x800f081f",
        "loai": "Cơ bản - Thư viện nền tảng",
        "nguyen_nhan": "Windows Update không tìm thấy các file nguồn để kích hoạt tính năng .NET Framework 3.5 hoặc 4.8, thường do bộ cài Windows ẩn bị lược bỏ bớt.",
        "giai_phap": [
            "- Bước 1: Tải file phần mềm '.NET Framework 3.5 Offline Installer' chính chủ từ Microsoft.",
            "- Bước 2: Hoặc mở CMD (Admin), gõ lệnh: 'dism /online /enable-feature /featurename:NetFX3 /All /Source:D:\\sources\\sxs /LimitAccess' (Với D: là ổ đĩa chứa bộ cài Windows)."
        ]
    },
    "màn hình đen": {
        "ten": "Hiện tượng máy lên nguồn, quạt quay nhưng MÀN HÌNH ĐEN XÌ",
        "loai": "Cơ bản - Lỗi tín hiệu xuất hình",
        "nguyen_nhan": "Mất tín hiệu xuất hình giữa card màn hình (VGA) và màn hình, lỏng dây nguồn, lỏng dây cáp tín hiệu (HDMI/DisplayPort) hoặc BIOS bị treo cài đặt xung đột phần cứng.",
        "giai_phap": [
            "- Bước 1: Nhấn tổ hợp phím nóng: 'Ctrl + Shift + Windows + B' để ép Windows nạp lại driver card màn hình ngay lập tức (máy sẽ bíp nhẹ một tiếng và chớp màn hình).",
            "- Bước 2: Kiểm tra jack cắm cáp. Rất nhiều người cắm nhầm dây màn hình vào cổng xuất hình trên Mainboard thay vì cắm vào cổng của Card màn hình rời (VGA).",
            "- Bước 3: Tháo dây nguồn, tháo viên pin CMOS hình tròn trên bo mạch chủ ra ngoài trong 5 phút để xả hết điện, đưa cài đặt BIOS về mặc định gốc (Reset BIOS)."
        ]
    },
    "máy chạy sập": {
        "ten": "Hiện tượng máy tính bật lên dùng được vài phút rồi ĐỘT NGỘT SẬP NGUỒN HOÀN TOÀN",
        "loai": "Nghiêm trọng - Quá nhiệt & Nguồn điện",
        "nguyen_nhan": "CPU bị quá nhiệt vượt ngưỡng an toàn (trên 100 độ C) do keo tản nhiệt bị khô hoặc quạt tản không quay; hoặc do bộ nguồn (PSU) bị sụt áp, không gánh nổi công suất máy khi vào tải nặng.",
        "giai_phap": [
            "- Bước 1: Bật máy vào BIOS hoặc dùng phần mềm HWMonitor kiểm tra nhiệt độ CPU. Nếu CPU vượt quá 85-90 độ khi chạy không tải, chắc chắn do quá nhiệt.",
            "- Bước 2: Gỡ tản nhiệt CPU, lau sạch lớp keo cũ bám trên bề mặt chip, bôi một lớp keo tản nhiệt mới (như MX-4) rồi siết chặt ốc tản nhiệt đều 4 góc.",
            "- Bước 3: Kiểm tra quạt tản nhiệt CPU xem dây nguồn quạt có bị lỏng không. Nếu quạt không quay khi bật máy, cần thay quạt mới ngay."
        ]
    }
}

# [DANH MỤC 2]: KHO GIẢI MÃ TIẾNG KÊU BÁO LỖI CỦA MAINBOARD (BIOS Beep Codes)
BEEP_CODES = {
    "1 tít ngắn": {
        "tinh_trang": "HỆ THỐNG HOÀN HẢO. Máy vượt qua bài kiểm tra phần cứng khởi động (POST) thành công. Mọi linh kiện (CPU, RAM, VGA) đều kết nối tốt."
    },
    "tít dài liên tục": {
        "tinh_trang": "LỖI KẾT NỐI RAM. Bo mạch chủ không tìm thấy bộ nhớ RAM hoặc RAM bị lỏng, lỗi chân cắm vật lý.",
        "xu_ly": "Tháo toàn bộ thanh RAM ra, dùng cục tẩy vệ sinh chân vàng tiếp xúc thật kỹ, cắm chặt lại vào khe, nghe tiếng 'Cạch' ở cả 2 đầu lẫy khóa bo mạch là chuẩn."
    },
    "1 tít dài 3 tít ngắn": {
        "tinh_trang": "LỖI ĐỒ HỌA (VGA). Hệ thống không nhận diện được Card màn hình rời (VGA), lỗi chip xử lý đồ họa hoặc bạn quên chưa cắm dây nguồn phụ cấp cho VGA.",
        "xu_ly": "Kiểm tra xem đã cắm chặt các đầu nguồn phụ 6-pin/8-pin từ nguồn (PSU) vào card đồ họa chưa. Tháo card VGA ra khỏi khe PCI-E, lau sạch chân cắm rồi ấn chặt lại."
    },
    "5 tít ngắn": {
        "tinh_trang": "LỖI XỬ LÝ TRUNG TÂM (CPU). CPU chưa được cấp nguồn điện, lỏng chân cắm Socket, quạt tản nhiệt CPU không hoạt động hoặc chân Socket trên mainboard bị cong gãy.",
        "xu_ly": "Kiểm tra dây nguồn 4-pin/8-pin mang chữ 'CPU' ở góc trên bên trái bo mạch chủ xem đã cắm chưa. Nếu tự ráp máy, cần nhấc CPU lên để kiểm tra xem hệ thống chân socket của mainboard có bị cong hay không."
    },
    "3 tít ngắn": {
        "tinh_trang": "LỖI BỘ NHỚ ĐỆM 64KB ĐẦU TIÊN (RAM Fail). RAM bị hỏng hoàn toàn một chip nhớ core, không thể nạp tầng dữ liệu nền móng để khởi động.",
        "xu_ly": "Trường hợp này vệ sinh không hết lỗi thì bắt buộc phải thay thế thanh RAM khác để hệ thống tiếp tục hoạt động."
    },
    "1 tít dài 2 tít ngắn": {
        "tinh_trang": "LỖI BO MẠCH CHỦ HOẶC ĐỘ PHÂN GIẢI MÀN HÌNH (Display/Motherboard Error). Bo mạch không thể giao tiếp với chip điều khiển xuất hình hoặc màn hình không hỗ trợ tần số quét hiện tại.",
        "xu_ly": "Rút cáp màn hình ra cắm lại, đổi sang cổng xuất hình khác (DVI/HDMI/DisplayPort). Nếu không được, tiến hành tháo pin CMOS để reset bo mạch chủ."
    }
}

# [DANH MỤC 3]: KHO LINH KIỆN PC CHUYÊN SÂU & ĐỘ TƯƠNG THÍCH ĐỐI ĐẦU (Dùng cho Engine So Sánh)
LINH_KIEN_PC = {
    "i5-6500": {
        "ten": "Intel Core i5-6500 (Skylake Architecture - Thế hệ 6)",
        "loai": "CPU (Bộ vi xử lý trung tâm)",
        "thong_so": "4 nhân 4 luồng, Xung nhịp cơ bản 3.2 GHz (Turbo tối đa 3.6 GHz), Bộ nhớ đệm 6MB Cache, Tiến trình 14nm, Điện năng tiêu thụ TDP 65W, tích hợp đồ họa Onboard Intel HD Graphics 530.",
        "socket": "LGA1151 (Chỉ chạy các chipset đời 100 và 200 series)",
        "main_tuong_thich": ["H110", "B150", "B250", "Z170", "Z270"],
        "nguon_khuyen_nghi": "Từ 350W công suất thực trở lên (Ví dụ: Antec, Xigmatek, Corsair).",
        "chuyen_gia_tu_van": "CPU huyền thoại tầm trung đời 6. Điểm mạnh là cực kỳ mát và ăn ít điện. Để tối ưu hóa chi phí tốt nhất cho học sinh, Chung nên ghép cặp em CPU này với các bo mạch chủ dòng phổ thông như H110 (ví dụ H110M-DS2 của Gigabyte hoặc Asus H110M-E). Cấu hình này rất phù hợp làm máy học tập, văn phòng, làm video nhẹ trên CapCut, chơi mượt Liên Quân Mobile trên giả lập và LOL ở mức thiết lập cao."
    },
    "i3-12100f": {
        "ten": "Intel Core i3-12100F (Alder Lake Architecture - Thế hệ 12)",
        "loai": "CPU (Bộ vi xử lý trung tâm)",
        "thong_so": "4 nhân 8 luồng (Sử dụng hoàn toàn 4 nhân hiệu năng cao P-core), Xung nhịp tối đa lên đến 4.3 GHz, Bộ nhớ đệm 12MB Intel Smart Cache, Hỗ trợ RAM DDR4 lẫn DDR5, KHÔNG tích hợp card đồ họa onboard (Hậu tố F).",
        "socket": "LGA1700 (Thế hệ 12, 13, 14)",
        "main_tuong_thich": ["H610", "B660", "B760", "Z690", "Z790"],
        "nguon_khuyen_nghi": "Từ 450W trở lên (Tính toán dựa trên việc đi chung với VGA rời dòng tầm trung).",
        "chuyen_gia_tu_van": "Chip quốc dân vô địch trong tầm giá rẻ. Sức mạnh đơn nhân của nó cực kỳ khủng khiếp, đè bẹp hoàn toàn tất cả các dòng i7 thế hệ cũ (từ đời 9 trở xuống). Do không có đồ họa tích hợp, Chung BẮT BUỘC phải cắm kèm card màn hình rời (VGA) thì máy mới xuất hình được nhé. Để tối ưu ngân sách, hãy đi combo i3-12100F + Mainboard H610 để dành tiền đập vào card đồ họa ngon hơn."
    },
    "i5-12400f": {
        "ten": "Intel Core i5-12400F (Alder Lake Architecture - Thế hệ 12)",
        "loai": "CPU (Bộ vi xử lý trung tâm)",
        "thong_so": "6 nhân 12 luồng (6 nhân hiệu năng cao P-core), Xung nhịp Turbo tối đa 4.4 GHz, Bộ nhớ đệm 18MB Cache, TDP 65W. Không tích hợp đồ họa Onboard.",
        "socket": "LGA1700 (Thế hệ 12, 13, 14)",
        "main_tuong_thich": ["H610", "B660", "B760", "Z690"],
        "nguon_khuyen_nghi": "Từ 550W công suất thực trở lên.",
        "chuyen_gia_tu_van": "Quái vật hiệu năng phân khúc tầm trung. Nhờ có 6 nhân 12 luồng thực sự, con chip này vừa chơi mượt các game nặng cấu hình cao (AAA) vừa có khả năng gánh tốt các phần mềm làm video chuyên sâu hoặc chạy nhiều tab giả lập Android cùng lúc mà không bị nghẹn cổ chai."
    },
    "gtx 1650": {
        "ten": "NVIDIA GeForce GTX 1650",
        "loai": "VGA (Card đồ họa rời)",
        "thong_so": "Dung lượng bộ nhớ 4GB vRAM (Chuẩn GDDR5 hoặc GDDR6), Băng thông bộ nhớ 128-bit, kiến trúc Turing, 896 nhân CUDA.",
        "nguon_khuyen_nghi": "350W công suất thực. Hầu hết các phiên bản không cần cắm thêm nguồn phụ (Lấy điện trực tiếp từ khe PCI-E 75W trên mainboard).",
        "chuyen_gia_tu_van": "Dòng card rời phân khúc phổ thông bền bỉ và cực kỳ tiết kiệm điện năng. Ưu điểm lớn nhất là nhiệt độ hoạt động rất mát mẻ và không kén bộ nguồn. Nó rất thích hợp để nâng cấp cho các dàn máy PC cũ (như dàn chạy chip i5-6500) giúp hồi sinh hiệu năng, đủ sức chiến mượt mà các tựa game Esport thịnh hành hiện tại như Valorant, Liên Minh Huyền Thoại, CS2 ở mức thiết lập đồ họa cao trên màn hình Full HD."
    },
    "rtx 3060": {
        "ten": "NVIDIA GeForce RTX 3060 (Ampere Architecture)",
        "loai": "VGA (Card đồ họa rời)",
        "thong_so": "Dung lượng bộ nhớ KHỦNG 12GB vRAM GDDR6, Băng thông 192-bit, Hỗ trợ công nghệ tối tân Ray Tracing (Dò tia ánh sáng) và DLSS (Tăng tốc độ khung hình bằng AI).",
        "nguon_khuyen_nghi": "Từ 550W công suất thực trở lên (Yêu cầu 1 đầu cấp nguồn phụ 8-pin).",
        "chuyen_gia_tu_van": "Card đồ họa tầm trung cực mạnh giúp làm chủ hoàn toàn độ phân giải Full HD và 2K. Với lợi thế 12GB vRAM, card này thách thức mọi tựa game đồ họa nặng nhất, đồng thời cực kỳ tối ưu cho các bạn học làm đồ họa 3D, dựng phim chuyên nghiệp hoặc chạy các mô hình AI cục bộ."
    }
}
