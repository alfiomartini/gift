document.addEventListener("DOMContentLoaded", search);

function search() {
  const search_btn = document.getElementById("search-btn");
  const select = document.getElementById("find-select");
  const input = document.querySelector('input[type="search"]');

  select.addEventListener("change", () => {
    const value = select.value;
    input.value = value;
    input.focus();
  });
}
