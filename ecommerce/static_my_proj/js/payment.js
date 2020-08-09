$(document).ready(function () {
    if (document.getElementsByClassName("payment-form").length == 1) {

        let pubKey = document.getElementsByClassName("payment-form")[0].getAttribute("data-token");
        let nextURL = document.getElementsByClassName("payment-form")[0].getAttribute("data-next-url")
        let stripe = Stripe(pubKey);
        // Create an instance of Elements.
        let elements = stripe.elements();
        let style = {
            base: {
                color: '#32325d',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: 'antialiased',
                fontSize: '16px',
                '::placeholder': {
                    color: '#aab7c4'
                }
            },
            invalid: {
                color: '#fa755a',
                iconColor: '#fa755a'
            }
        };
        // Create an instance of the card Element.
        let card = elements.create('card', { style: style });
        // Add an instance of the card Element into the `card-element` <div>.
        card.mount('#card-element');
        // Handle real-time validation errors from the card Element.
        card.on('change', function (event) {
            var displayError = document.getElementById('card-errors');
            if (event.error) {
                displayError.textContent = event.error.message;
            } else {
                displayError.textContent = '';
            }
        });
        // Handle form submission.
        let form = document.getElementById('payment-form');
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            stripe.createToken(card).then(function (result) {
                if (result.error) {
                    // Inform the user if there was an error.
                    let errorElement = document.getElementById('card-errors');
                    errorElement.textContent = result.error.message;
                } else {
                    // Send the token to your server.
                    stripeTokenHandler(result.token, nextURL);
                }
            });
        });

        // Submit the form with the token ID.
        function stripeTokenHandler(token, nextURL) {
            let endpoint = '/billing/payment/create';
            let data = {
                'token': token.id
            }

            $.ajax({
                data: data,
                url: endpoint,
                method: 'POST',
                success: function (data) {
                    card.clear();
                    createSnackbar(data.message);
                    setTimeout(() => {
                        window.location.href = `${window.location.origin}/cart/checkout`
                    }, 1500);
                },
                error: function (error) {
                    createSnackbar(error.message)
                }
            })
        }
    }










    let createSnackbar = (function () {
        // Any snackbar that is already shown
        let previous = null;

        return function (message, actionText, action) {
            if (previous) {
                previous.dismiss();
            }
            let snackbar = document.createElement('div');
            snackbar.className = 'paper-snackbar';
            snackbar.dismiss = function () {
                this.style.opacity = 0;
            };
            let text = document.createTextNode(message);
            snackbar.appendChild(text);
            if (actionText) {
                if (!action) {
                    action = snackbar.dismiss.bind(snackbar);
                }
                let actionButton = document.createElement('button');
                actionButton.className = 'action';
                actionButton.innerHTML = actionText;
                actionButton.addEventListener('click', action);
                snackbar.appendChild(actionButton);
            }
            setTimeout(function () {
                if (previous === this) {
                    previous.dismiss();
                }
            }.bind(snackbar), 3000);

            snackbar.addEventListener('transitionend', function (event, elapsed) {
                if (event.propertyName === 'opacity' && this.style.opacity == 0) {
                    this.parentElement.removeChild(this);
                    if (previous === this) {
                        previous = null;
                    }
                }
            }.bind(snackbar));



            previous = snackbar;
            document.body.appendChild(snackbar);
            // In order for the animations to trigger, I have to force the original style to be computed, and then change it.
            getComputedStyle(snackbar).top;
            snackbar.style.left = '40%';
            snackbar.style.bottom = '88%';
            snackbar.style.opacity = 1;
        };
    })();
})