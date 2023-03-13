console.log("Sanity check!");

// Get Stripe publishable key
fetch("/payment/config/")
  .then((result) => {
    return result.json();
  })
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // new
    // Event handler
    $("#submitBtn").click(() => {
      //   console.log("testing");
      // Get Checkout Session ID
      fetch("/payment/create_checkout_session")
        .then((result) => {
          return result.json();
        })
        .then((data) => {
          console.log(data);
          // Redirect to Stripe Checkout
          return stripe.redirectToCheckout({ sessionId: data.sessionId });
        })
        .then((res) => {
          console.log(res);
        });
    });
  });
