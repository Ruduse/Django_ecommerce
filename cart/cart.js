document.addEventListener("DOMContentLoaded", function () {
  const increaseButtons = document.querySelectorAll(".increase-quantity");
  const decreaseButtons = document.querySelectorAll(".decrease-quantity");

  increaseButtons.forEach(function (button) {
    button.addEventListener("click", function (event) {
      event.preventDefault();
      const productId = this.dataset.productId;
      updateCart(productId, "increase");
    });
  });

  decreaseButtons.forEach(function (button) {
    button.addEventListener("click", function (event) {
      event.preventDefault();
      const productId = this.dataset.productId;
      updateCart(productId, "decrease");
    });
  });

  function updateCart(productId, action) {
    const url = "/update-cart/";
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        productId: productId,
        action: action,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Refresh the page or update the cart display as needed
        console.log(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
