function showPaymentForm(method) {
    const cashSection = document.getElementById('cash-section');
    const upiSection  = document.getElementById('upi-section');
    if (method === 'cash') {
        cashSection.style.display = 'block';
        upiSection.style.display  = 'none';
        document.querySelectorAll('#upi-section input').forEach(
            el => el.removeAttribute('required')
        );
    } else {
        cashSection.style.display = 'none';
        upiSection.style.display  = 'block';
        document.querySelectorAll('#upi-section input').forEach(
            el => el.setAttribute('required', 'required')
        );
    }
}

document.getElementById('paymentForm').addEventListener('submit', function(e) {
    const method = document.querySelector(
        'input[name="payment_method"]:checked'
    ).value;
    if (method === 'upi') {
        const txnId = document.querySelector(
            'input[name="transaction_id"]'
        ).value.trim();
        if (!txnId || txnId.length < 6) {
            e.preventDefault();
            alert('Please enter a valid Transaction / UTR number.');
            return;
        }
    }
    const btn = document.getElementById('placeOrderBtn');
    btn.disabled = true;
    btn.innerHTML =
        '<span class="spinner-border spinner-border-sm me-2"></span>' +
        'Placing Order...';
});