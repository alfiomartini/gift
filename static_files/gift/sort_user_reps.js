document.addEventListener("DOMContentLoaded", sort_dropdown);

function sort_dropdown(){
  const userRepsOptions = document.querySelectorAll('.sort-options .dropdown-menu a');
  userRepsOptions.forEach(option  => {
    option.addEventListener('click', () =>{
      const sort = option.dataset.sort;
      const query = option.dataset.query;
      const page = option.dataset.page;
      location.assign(`/user/${query}/${sort}?page=${page}`);
    })
  });
}