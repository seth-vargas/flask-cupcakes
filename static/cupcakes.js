$(".delete-cupcake").click(deleteCupcake);
$("#new-cupcake-form").submit(createCupcake);

async function deleteCupcake() {
  const id = $(this).data("id");
  await axios.delete(`/api/cupcakes/${id}`);
  $(this).parent().remove();
}

async function createCupcake(e) {
  e.preventDefault();
  // https://stackoverflow.com/questions/2276463/how-can-i-get-form-data-with-javascript-jquery/24012884#24012884
  // Shoutout to neuront for the serializing function below!
  const data = $("#new-cupcake-form")
    .serializeArray()
    .reduce(function (obj, item) {
      obj[item.name] = item.value;
      return obj;
    }, {});
    $("#new-cupcake-form").trigger("reset")

    try {
      const resp = await axios.post("/api/cupcakes", data);

    // Create new li and append it to the ul
    const newCupcake = resp.data.cupcake;
    console.log(newCupcake);
    const newLi = $(`
        <li class="py-1">
        <a href="/cupcakes/${newCupcake.id}">
        Flavor: ${newCupcake.flavor}. Size: ${newCupcake.size}. Rating: ${newCupcake.rating}
        </a>
        <button class="btn btn-danger btn-sm delete-cupcake" data-id="${newCupcake.id}">X</button>
        </li>
        `);
    $("#cupcake-container").append(newLi);
    $(".delete-cupcake").click(deleteCupcake);
  } catch (error) {
    for(let input of error.response.data["invalid_inputs"]) {
        $(`#${input}`).append(`<p class="bg-danger p-3">${input} cannot be null</p>`)
    }
  }
}
