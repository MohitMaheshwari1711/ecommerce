function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');




$(document).ready(function () {


    //------------------------------------SECURITY RELATED------------------------------//
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    //------------------------------------SECURITY RELATED------------------------------//



    window.addEventListener("click", function (event) {
        if (event.target.className == 'login-radio') {
            $(".form-1").css("display", "block");
            $(".form-2").css("display", "none");
        } else if (event.target.className == 'register-radio') {
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




    if ($('#DivID').length) {
        get_related_products()
    }

    function get_related_products() {
        $.ajax({
            url: `/api/related`,
            method: 'GET',
            data: {},
            success: function (data) {
                $.each(data.products, function (index, value) {
                    $("#related-products").prepend(
                        `<div class="col-sm-3 col-md-3 col-lg-3 ftco-animated">
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
                                </div>
                            </div>
                        </div>
                    </div>`
                    )
                })
            }
        })
    }
});















function lets_go() {
    setTimeout(() => {
        window.location.href = '/cart'
    }, 500);
}



function update_wishlist(val) {
    let formData = {
        'csrfmiddlewaretoken': csrftoken,
        'product_id': val
    }
    $.ajax({
        url: '/api/wishlist/add-remove/',
        method: 'POST',
        data: formData,
        success: function (data) {
            $(`#add-wishlist-${val}`).empty();
            if (data.added) {
                $(`#add-wishlist-${val}`).prepend(
                    `<i onclick='update_wishlist(${val})' class='ion-ios-heart ml-1' style="color: red; cursor: pointer;"></i>`
                )
            } else if (!data.added) {
                $(`#add-wishlist-${val}`).prepend(
                    `<i onclick='update_wishlist(${val})' class='ion-ios-heart ml-1' style='cursor: pointer;'></i>`
                )
            }
        },
        error: function (error) {
            console.log(error.responseText)
        }
    })
}



function removeFromWishlist(val) {
    let formData = {
        'csrfmiddlewaretoken': csrftoken,
        'product_id': val
    }
    $.ajax({
        url: '/api/wishlist/remove/',
        method: 'POST',
        data: formData,
        success: function (data) {
            let navbarCount = $(".navbar-cart-count")
            navbarCount.text("[" + data.count + "]")
            cart_remove_html(data)
        }
    })
}



function wishlist_all() {
    let wishListUrl = '/api/wishlist/all/';
    let wishListMethod = "GET";

    $.ajax({
        url: wishListUrl,
        method: wishListMethod,
        data: {},
        success: function (data) {
            cart_remove_html(data)
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




function cart_remove_html(val) {
    $("#product-index").empty();
    $.each(val.products, function (index, value) {
        $("#product-index").prepend(
            `<div class="col-sm-3 col-md-3 col-lg-3 ftco-animated">
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
                            </div>
                            <div class="submit-span">
                                <p class='d-flex ml-6' style="position: absolute; top: -335px;">
                                    <i onclick="removeFromWishlist(${value.id})" class='ion-ios-close ml-1' style="font-size: 21px; cursor: pointer;"></i>
                                </p>
                                <p class='bottom-area d-flex px-3'>
                                    <button onclick="onOpen(${value.id})" class='btn add-to-cart text-center py-2 mr-1' style='background-color: #ffa45c; color: #ffffff; margin-left: auto; margin-right: auto;'>Move to Bag<span><i class='ion-ios-cart ml-1'></i></span></button>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>`
        )
    })
}





let selected_size = '';
let default_quantity = 1

function small(id) {
    document.getElementById(`small-${id}`).style.backgroundColor = '#ffa45c';
    document.getElementById(`medium-${id}`).style.backgroundColor = 'white';
    document.getElementById(`large-${id}`).style.backgroundColor = 'white';
    document.getElementById(`extra_large-${id}`).style.backgroundColor = 'white';

    selected_size = 'S';
    document.getElementById(`state-${id}`).removeAttribute("disabled");
}

function medium(id) {
    document.getElementById(`small-${id}`).style.backgroundColor = 'white';
    document.getElementById(`medium-${id}`).style.backgroundColor = '#ffa45c';
    document.getElementById(`large-${id}`).style.backgroundColor = 'white';
    document.getElementById(`extra_large-${id}`).style.backgroundColor = 'white';

    selected_size = 'M';
    document.getElementById(`state-${id}`).removeAttribute("disabled");
}

function large(id) {
    document.getElementById(`small-${id}`).style.backgroundColor = 'white';
    document.getElementById(`medium-${id}`).style.backgroundColor = 'white';
    document.getElementById(`large-${id}`).style.backgroundColor = '#ffa45c';
    document.getElementById(`extra_large-${id}`).style.backgroundColor = 'white';

    selected_size = 'L';
    document.getElementById(`state-${id}`).removeAttribute("disabled");
}

function extra_large(id) {
    document.getElementById(`small-${id}`).style.backgroundColor = 'white';
    document.getElementById(`medium-${id}`).style.backgroundColor = 'white';
    document.getElementById(`large-${id}`).style.backgroundColor = 'white';
    document.getElementById(`extra_large-${id}`).style.backgroundColor = '#ffa45c';

    selected_size = 'XL';
    document.getElementById(`state-${id}`).removeAttribute("disabled");
}



function quantity_change(event) {
    default_quantity = +event.target.value
}



function onOpen(id) {
    document.getElementById(`state-${id}`).setAttribute("disabled", true);
}


function clear_modal_values(product_id) {
    default_quantity = 1
    document.getElementById(`small-${product_id}`).style.backgroundColor = 'white';
    document.getElementById(`medium-${product_id}`).style.backgroundColor = 'white';
    document.getElementById(`large-${product_id}`).style.backgroundColor = 'white';
    document.getElementById(`extra_large-${product_id}`).style.backgroundColor = 'white';

    document.getElementById(`quantity-select-${product_id}`).value = '1';
}




function add_to_cart(product_id) {
    let addToCartUrl = '/api/cart/add';
    let addToCartMethod = "POST";
    let formData = {
        'csrfmiddlewaretoken': csrftoken,
        'product_id': product_id,
        'quantity': default_quantity,
        'size': selected_size,
    }
    $.ajax({
        url: addToCartUrl,
        method: addToCartMethod,
        data: formData,
        success: function (data) {
            default_quantity = 1
            document.getElementById(`small-${product_id}`).style.backgroundColor = 'white';
            document.getElementById(`medium-${product_id}`).style.backgroundColor = 'white';
            document.getElementById(`large-${product_id}`).style.backgroundColor = 'white';
            document.getElementById(`extra_large-${product_id}`).style.backgroundColor = 'white';

            document.getElementById(`quantity-select-${product_id}`).value = '1';

            document.getElementById("navbar-cart-count").innerText = `[${data.cartItemCount}]`;

            if (window.location.href.includes("wishlist")) {
                wishlist_all()
            } else {
                let len = $(`#add-wishlist-${product_id}`).length
                if (len > 0) {
                    $(`#add-wishlist-${product_id}`).empty();
                    $(`#add-wishlist-${product_id}`).prepend(
                        `<i onclick='update_wishlist(${product_id})' class='ion-ios-heart ml-1' style='cursor: pointer;'></i>`
                    )
                } else {
                    document.getElementById(`state-${product_id}`).setAttribute("disabled", true);
                }
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




function remove_from_cart(cart_item_id) {
    let removeToCartUrl = '/api/cart/remove';
    let removeToCartMethod = "POST";
    let formData = {
        'csrfmiddlewaretoken': csrftoken,
        'cart_item_id': cart_item_id,
    }
    $.ajax({
        url: removeToCartUrl,
        method: removeToCartMethod,
        data: formData,
        success: function (data) {
            updateCart()
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
            if (data.products.length > 0) {
                productRows.html(" ")
                i = data.products.length;
                $.each(data.products, function (index, value) {
                    cartBody.append(
                        `
                        <tr class="text-center cart-product">
                            <td class="product-quantity">${index + 1}</td>
                            <td class="image-prod">
                                <div class="img" style="background-image:url('${value.image_url}');"></div>
                            </td>
                            <td class="product-name">
                                <h3>${value.name}</h3>
                                <button class="btn btn-link btn-sm" id="cart-item-remove-form" onclick="remove_from_cart(${value.cart_item_id})">Remove ?</button>
                            </td>
                            <td class="price">${value.size}</td>
                            <td class="price">X ${value.quantity}</td>
                            <td class="price">₹ ${value.price}</td>
                        </tr>
                        `
                    )
                    i--
                })
                document.getElementsByClassName("cart-subtotal")[0].innerHTML = "₹" + data.subtotal;
                document.getElementsByClassName("cart-total-2")[0].innerHTML = "₹" + data.total;
                document.getElementById("navbar-cart-count").innerText = `[${data.cartItemCount}]`;
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



