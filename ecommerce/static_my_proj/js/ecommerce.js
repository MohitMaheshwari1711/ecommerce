$(document).ready(function () {

    window.addEventListener("click", function (event) {
        if (event.target.className == 'login-radio') {
            $(".form-1").css("display", "block");
            $(".form-2").css("display", "none");
        } else if (event.target.className == 'guest-radio') {
            $(".form-1").css("display", "none");
            $(".form-2").css("display", "block");
        }
    });



    let contactForm = $(".contact-form");
    let contactFormMethod = contactForm.attr("method");
    let contactFormEndpoint = contactForm.attr("action");

    function displaySubmitting(submitBtn, defaultText, doSubmit) {
        if (doSubmit) {
            submitBtn.addClass("disabled");
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...");
        } else {
            submitBtn.removeClass("disabled");
            submitBtn.html(defaultText)
        }
    }

    contactForm.submit(function (event) {
        event.preventDefault();
        let contactFormSubmitBtn = contactForm.find("[type='submit']");
        let contactFormSubmitBtnTxt = contactFormSubmitBtn.text();
        let contactFormData = contactForm.serialize();
        displaySubmitting(contactFormSubmitBtn, "", true)
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: function (data) {
                contactForm[0].reset();
                window.alert(data.message);
                displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
            },
            error: function (errorData) {
                let jsonData = errorData.responseJSON;
                let msg = "";
                $.each(jsonData, function (key, value) {
                    msg += key + ": " + value[0].message + "<br/>"
                })
                window.alert(msg);
                displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
            }
        })
    })


    let searchForm = $(".search-form");
    let searchInput = searchForm.find("[name='q']");
    let typingTimer;
    let typingInterval = 1500;
    let searchBtn = searchForm.find("[type='submit']");

    searchInput.keyup(function (event) {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(performSearch, typingInterval)
    });

    searchInput.keydown(function (event) {
        clearTimeout(typingTimer);
    });

    function displaySearching() {
        searchBtn.addClass("disabled");
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...");
    }

    function performSearch() {
        displaySearching();
        let query = searchInput.val();
        window.location.href = '/search/?q=' + query;
    }

    let productForm = $(".form-product-ajax")
    productForm.submit(function (event) {
        event.preventDefault();
        let thisForm = $(this)
        // let actionEndpoint = thisForm.attr("action");
        let actionEndpoint = thisForm.attr("data-endpoint");
        let httpMethod = thisForm.attr("method");
        let formData = thisForm.serialize();

        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function (data) {
                let submitSpan = thisForm.find(".submit-span")
                if (data.added) {
                    submitSpan.html("<span>In cart<button type='submit' class='btn btn-link' style='box-shadow: none;'>Remove ?</button></span>")
                } else {
                    submitSpan.html("<p class='bottom-area d-flex px-3'><button type='submit' class='btn add-to-cart text-center py-2 mr-1' style='background-color: black; color: #ffffff;'><span>Add to cart <i class='ion-ios-add ml-1'></i></span></button><button type='submit' class='btn buy-now text-center py-2' onclick='lets_go()' style='background-color: #ffa45c; color: #ffffff;'>Buy now<span><i class='ion-ios-cart ml-1'></i></span></button></p>")
                }
                let navbarCount = $(".navbar-cart-count")
                navbarCount.text("[" + data.cartItemCount + "]")
                let currentPath = window.location.href;
                if (currentPath.indexOf("cart") != -1) {
                    updateCart()
                }


            },
            error: function (errorData) {
                window.alert('An error occured.')
            }
        })
    })


    if ($('#DivID').length) {
        console.log('Found with Length');
        trial()
    }

    function trial() {
        $.ajax({
            url: `/api/related`,
            method: 'GET',
            data: {},
            success: function (data) {
                $.each(data.products, function (index, value) {
                    $("#related-products").prepend(
                        `<div class="col-sm-4 col-md-4 col-lg-4 ftco-animated">
                        <div class="product">
                            <a href='${value.url}' class="img-prod"><img class="img-fluid" src='${value.image_url}'
                                alt="Colorlib Template">
                                <div class="overlay"></div>
                            </a>
                            <div class="text py-3 px-3 text-center">
                                <h3><a href='${value.url}'>${value.name}</a></h3>
                                <div class="d-flex">
                                    <div class="pricing">
                                        <p class="price"><span class="price-sale">₹${value.price}</span></p>
                                    </div>
                                    <div class="rating">
                                        <p class="text-right">
                                            <a href="#"><span class="ion-ios-star-outline"></span></a>
                                            <a href="#"><span class="ion-ios-star-outline"></span></a>
                                            <a href="#"><span class="ion-ios-star-outline"></span></a>
                                            <a href="#"><span class="ion-ios-star-outline"></span></a>
                                            <a href="#"><span class="ion-ios-star-outline"></span></a>
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>`
                    )
                })
            }
        })
    }



    function updateCart() {
        let cartTable = $(".cart-table")
        let cartBody = cartTable.find(".cart-body")
        let productRows = cartBody.find(".cart-product")
        let currentUrl = window.location.href

        let updateCartUrl = '/api/cart/';
        let updateCartMethod = "GET";
        let data = {}
        $.ajax({
            url: updateCartUrl,
            method: updateCartMethod,
            data: data,
            success: function (data) {
                let hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                if (data.products.length > 0) {
                    productRows.html(" ")
                    i = data.products.length;
                    $.each(data.products, function (index, value) {
                        let newCartItemRemoveForm = hiddenCartItemRemoveForm.clone();
                        newCartItemRemoveForm.css("display", "block");
                        newCartItemRemoveForm.find(".cart-item-product-id").val(value.id);
                        cartBody.prepend("<tr class='text-center cart-product'><td class='product-name'>" + i + "</td><td class='image-prod'><div class='img' style='background-image:url(" + value.image_url + ")'></div></td><td class='product-name'><h3>" + value.name + "</h3>" + newCartItemRemoveForm.html() + "</td><td class='price'>" + value.price + "</td><tr>")
                        i--
                    })
                    document.getElementsByClassName("cart-subtotal")[0].innerHTML = "$" + data.subtotal
                    document.getElementsByClassName("cart-total-2")[0].innerHTML = "$" + data.total
                } else {
                    window.location.href = currentUrl
                }
            },
            error: function (errorData) {
                $.alert({
                    title: "Oops!",
                    content: "An error occured.",
                    theme: "modern"
                });
            }
        })
    }
})


function lets_go() {
    setTimeout(() => {
        window.location.href = '/cart'
    }, 500);
}



