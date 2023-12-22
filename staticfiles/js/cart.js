document.addEventListener('DOMContentLoaded', function () {
    // Update Cart
    var updateBtns = document.getElementsByClassName('update-cart');

    for (var i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function () {
            var productId = this.dataset.product;
            var action = this.dataset.action;
            var quantityInput = document.getElementById('quantityInput_' + productId);  // Adjust this based on your actual HTML structure
            var quantity = quantityInput ? quantityInput.value : 1;

            console.log('Before Fetch - productId:', productId);
            console.log('Before Fetch - action:', action);
            console.log('Before Fetch - quantity:', quantity);

            fetch('/update_item/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'productId': productId,
                    'action': action,
                    'quantity': quantity,
                }),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Response:', data);
                location.reload();
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Product Quantity
    $('.quantity button').on('click', function () {
        var button = $(this);
        var inputField = button.closest('.quantity').find('input');
        var oldValue = parseFloat(inputField.val());

        if (button.hasClass('btn-plus')) {
            var newVal = oldValue + 1;
        } else {
            newVal = Math.max(0, oldValue - 1);
        }

        inputField.val(newVal);
    });
});



document.addEventListener('DOMContentLoaded', function() {
    var dropdown = document.getElementById('categoryDropdown');
    var dropdownMenu = dropdown.querySelector('.dropdown-c');

    dropdown.addEventListener('click', function() {
        dropdownMenu.style.display = (dropdownMenu.style.display === 'block') ? 'none' : 'block';
    });

    // Close the dropdown if the user clicks outside of it
    window.addEventListener('click', function(event) {
        if (!event.target.matches('.rd-nav-link')) {
            dropdownMenu.style.display = 'none';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var dropdown = document.getElementById('settingDropdown');
    var dropdownMenu = dropdown.querySelector('.dropdown-c');

    dropdown.addEventListener('click', function() {
        dropdownMenu.style.display = (dropdownMenu.style.display === 'block') ? 'none' : 'block';
    });

    // Close the dropdown if the user clicks outside of it
    window.addEventListener('click', function(event) {
        if (!event.target.matches('.rd-nav-link')) {
            dropdownMenu.style.display = 'none';
        }
    });
});