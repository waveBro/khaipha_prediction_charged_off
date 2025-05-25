document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('finance-detail-form');
    if (!form) return;

    form.addEventListener('submit', async function (e) {
        e.preventDefault(); // NGĂN SUBMIT MẶC ĐỊNH

        // Lấy dữ liệu từ form
        const formData = new FormData(form);
        const data = {};
        for (const [key, value] of formData.entries()) {
            data[key] = value;
        }

        try {
            const response = await fetch('/api/kiem_tra_no2', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            if (result.success) {
                localStorage.setItem('predict_result', JSON.stringify(result));
                // Redirect to result page in model2 folder
                window.location.href = '/src/model/model2/result.html';
            } else {
                alert(result.message || 'Có lỗi xảy ra!');
            }
        } catch (error) {
            alert('Không thể kết nối máy chủ!');
        }
    });
});