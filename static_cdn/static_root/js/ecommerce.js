$(document).ready(function () {
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
        let thisForm = $(this);
        displaySubmitting(contactFormSubmitBtn, "", true)
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: function (data) {
                contactForm[0].reset();
                $.alert({
                    title: "Success!",
                    content: data.message,
                    theme: "modern"
                });
                displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
            },
            error: function (errorData) {
                let jsonData = errorData.responseJSON;
                let msg = "";
                $.each(jsonData, function (key, value) {
                    msg += key + ": " + value[0].message + "<br/>"
                })
                $.alert({
                    title: "Oops!",
                    content: msg,
                    theme: "modern"
                });
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
                    submitSpan.html("In cart<button type='submit' class='btn btn-link'>Remove ?</button>")
                } else {
                    submitSpan.html("<button type='submit' class='btn btn-success'>Add to cart</button>")
                }
                let navbarCount = $(".navbar-cart-count")
                navbarCount.text(data.cartItemCount)
                let currentPath = window.location.href;
                if (currentPath.indexOf("cart") != -1) {
                    updateCart()
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
    })

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
                        cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name +
                            "</a>" + newCartItemRemoveForm.html() + "</td><td>" + value.price + "</td><tr>")
                        i--
                    })
                    cartBody.find(".cart-subtotal").text(data.subtotal)
                    cartBody.find(".cart-total").text(data.total)
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