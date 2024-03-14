document.addEventListener('DOMContentLoaded', () => {
    const totp_qr_code = document.getElementById('totp-qr-code');
    if (totp_qr_code) {
        totp_qr_code.addEventListener('click', () => {
            totp_qr_code.classList.toggle("blurred");
        });
    }
});
