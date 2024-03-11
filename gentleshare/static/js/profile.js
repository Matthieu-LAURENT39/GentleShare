const totp_qr_code = document.getElementById('totp-qr-code');
totp_qr_code.addEventListener('click', () => {
    totp_qr_code.classList.toggle("blurred");
});