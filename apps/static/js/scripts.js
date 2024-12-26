function addProduct() {
    const productsDiv = document.getElementById('products');
    const newProduct = document.createElement('div');
    newProduct.classList.add('product', 'mb-3');
    newProduct.innerHTML = `
        <input type="text" class="form-control mb-2 product-name" name="product_details" placeholder="Product Name" required>
        <input type="number" class="form-control mb-2 quantity" name="quantity" placeholder="Quantity" required>
        <input type="number" class="form-control mb-2 price" name="price" placeholder="Price" step="0.01" readonly required>
    `;
    productsDiv.appendChild(newProduct);
    bindProductEvents();
}

function bindProductEvents() {
    $(".product-name").on("blur", function () {
        const productName = $(this).val();
        const priceField = $(this).closest('.product').find('.price');

        if (productName) {
            $.ajax({
                url: "/product_details",
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify({ product_name: productName }),
                success: function (response) {
                    priceField.val(response.price);
                },
                error: function () {
                    alert("Product not found");
                    priceField.val("");
                },
            });
        }
    });

    $(".quantity, .price").on("input", calculateTotal);
}

function calculateTotal() {
    let total = 0;
    $(".product").each(function () {
        const quantity = $(this).find(".quantity").val();
        const price = $(this).find(".price").val();
        if (quantity && price) {
            total += quantity * price;
        }
    });
    $("#total_amount").val(total.toFixed(2));
}

$(document).ready(function () {
    bindProductEvents();
});
