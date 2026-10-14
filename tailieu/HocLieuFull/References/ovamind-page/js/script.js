// Khởi tạo tập lệnh khi tài liệu đã sẵn sàng
document.addEventListener('DOMContentLoaded', function () {
    console.log("Giao diện NovaMind Welcome Page đã được tải thành công!");

    // Bạn có thể thêm các hiệu ứng bắt sự kiện click cho nút tại đây nếu cần thiết
    const getStartedBtn = document.querySelector('.btn-primary-custom');
    const signInBtn = document.querySelector('.btn-outline-custom');

    if(getStartedBtn) {
        getStartedBtn.addEventListener('click', function() {
            alert('Chuyển hướng đến trang Đăng ký!');
        });
    }

    if(signInBtn) {
        signInBtn.addEventListener('click', function() {
            alert('Chuyển hướng đến trang Đăng nhập!');
        });
    }
});