window.addEventListener("load", async ev => {
  const resp = await fetch(configUrl);
  const data = await resp.json();

  const stripe = Stripe(data.publicKey);

  const btnCheckout = document.querySelector('#btn-checkout');

  btnCheckout.addEventListener("click", async e => {
    const resp = await fetch(checkoutSessionUrl);
    const data = await resp.json();
    return stripe.redirectToCheckout({sessionId: data.sessionId});
  });
});
