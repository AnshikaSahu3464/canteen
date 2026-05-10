const cartQuantities = window.cartQuantities || {};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            const c = cookie.trim();
            if (c.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(c.slice(name.length + 1));
            }
        });
    }
    return cookieValue;
}

const CSRF_TOKEN = getCookie('csrftoken');

function showToast(message, type = 'success') {
    const existing = document.querySelector('.js-toast');
    if (existing) existing.remove();
    const toast = document.createElement('div');
    toast.className = 'js-toast alert alert-' + type + ' position-fixed';
    toast.style.cssText = 'top:80px;right:20px;z-index:9999;min-width:220px;' +
        'border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.15);';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => { if (toast.parentNode) toast.remove(); }, 2500);
}

function updateCartBadge(count) {
    const navBadge = document.getElementById('navCartCount');
    const showCount = document.getElementById('showCartCount');
    if (navBadge) {
        navBadge.textContent = count;
        navBadge.classList.add('bump');
        setTimeout(() => navBadge.classList.remove('bump'), 400);
    }
    if (showCount) showCount.textContent = count;
    const cartBar = document.getElementById('showCartBar');
    if (cartBar) {
        cartBar.className = count > 0 ? 'show-cart-bar visible' : 'show-cart-bar';
    }
}

function addToCart(itemId) {
    fetch('/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN
        },
        body: JSON.stringify({ item_id: itemId }),
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            cartQuantities[itemId] = data.item_quantity;
            showQtyControls(itemId, data.item_quantity);
            updateCartBadge(data.cart_count);
            updateShowCartTotal(data.cart_total);
            showToast('Added to cart!');
        } else {
            showToast(data.message || 'Error!', 'danger');
        }
    })
    .catch(() => showToast('Network error. Try again.', 'danger'));
}

function changeQty(itemId, delta) {
    const url = delta > 0 ? '/cart/add/' : '/cart/remove/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN
        },
        body: JSON.stringify({ item_id: itemId }),
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            cartQuantities[itemId] = data.item_quantity;
            updateQtyDisplay(
                itemId, data.item_quantity,
                data.cart_count, data.cart_total, data.item_subtotal
            );
            if (data.item_quantity === 0) {
                const qtyDiv = document.getElementById('qty-' + itemId);
                const addBtn = document.getElementById('add-btn-' + itemId);
                if (qtyDiv) qtyDiv.style.display = 'none';
                if (addBtn) addBtn.style.display = 'inline-flex';
                const cartRow = document.getElementById('cart-row-' + itemId);
                if (cartRow) {
                    cartRow.style.opacity = '0.5';
                    setTimeout(() => {
                        cartRow.remove();
                        checkEmptyCart();
                    }, 300);
                }
            }
        } else {
            showToast(data.message || 'Error!', 'danger');
        }
    });
}

function updateQtyDisplay(itemId, qty, cartCount, cartTotal, itemSubtotal) {
    const qtyCount = document.getElementById('qty-count-' + itemId);
    if (qtyCount) qtyCount.textContent = qty;
    const subtotalEl = document.getElementById('subtotal-' + itemId);
    if (subtotalEl && itemSubtotal) subtotalEl.textContent = '₹' + itemSubtotal;
    updateCartBadge(cartCount);
    updateShowCartTotal(cartTotal);
    const summaryTotal = document.getElementById('summaryTotal');
    const grandTotal   = document.getElementById('grandTotal');
    if (summaryTotal) summaryTotal.textContent = '₹' + cartTotal;
    if (grandTotal)   grandTotal.textContent   = '₹' + cartTotal;
}

function showQtyControls(itemId, qty) {
    const addBtn  = document.getElementById('add-btn-' + itemId);
    const qtyDiv  = document.getElementById('qty-' + itemId);
    const qtyCount = document.getElementById('qty-count-' + itemId);
    if (addBtn)   addBtn.style.display  = 'none';
    if (qtyDiv)   qtyDiv.style.display  = 'flex';
    if (qtyCount) qtyCount.textContent  = qty;
}

function updateShowCartTotal(total) {
    const el = document.getElementById('showCartTotal');
    if (el) el.textContent = total ? '₹' + total : '';
}

function checkEmptyCart() {
    const cartCard = document.querySelector('.cart-card');
    if (!cartCard) return;
    const items = cartCard.querySelectorAll('.cart-item');
    if (items.length === 0) {
        document.querySelector('.row.g-4').innerHTML = `
            <div class="col-12 text-center py-5">
                <div style="font-size:4rem;">🛒</div>
                <h3 class="mt-3">Your cart is empty!</h3>
                <a href="/home/" class="btn btn-primary btn-lg mt-2">
                    Browse Menu
                </a>
            </div>`;
        updateCartBadge(0);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    Object.keys(cartQuantities).forEach(itemId => {
        if (cartQuantities[itemId] > 0) {
            showQtyControls(itemId, cartQuantities[itemId]);
        }
    });
    const navBadge = document.getElementById('navCartCount');
    if (navBadge) {
        const count = parseInt(navBadge.textContent || '0');
        const cartBar = document.getElementById('showCartBar');
        if (cartBar && count > 0) cartBar.className = 'show-cart-bar visible';
    }
});