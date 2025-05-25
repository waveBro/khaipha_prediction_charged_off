document.addEventListener('DOMContentLoaded', function () {
    const result = JSON.parse(localStorage.getItem('predict_result'));
    const content = document.getElementById('result-content');
    if (result) {
        let modelHtml = `<div class="result-model">Sử dụng: <b>Model 2</b></div>`;
        if (result.prediction === 1) {
            content.innerHTML = `
                ${modelHtml}
                <div class="result-prediction" style="color:#d9534f;">Khách hàng <b>CÓ NGUY CƠ VỠ NỢ</b></div>
                <div class="result-proba">Xác suất vỡ nợ: <b>${(result.probability*100).toFixed(2)}%</b></div>
            `;
        } else {
            content.innerHTML = `
                ${modelHtml}
                <div class="result-prediction" style="color:#5cb85c;">Khách hàng <b>KHÔNG CÓ NGUY CƠ VỠ NỢ</b></div>
                <div class="result-proba">Xác suất vỡ nợ: <b>${(result.probability*100).toFixed(2)}%</b></div>
            `;
        }
    } else {
        content.innerHTML = `<div style="color:#d9534f;">Không có dữ liệu kết quả!</div>`;
    }
});