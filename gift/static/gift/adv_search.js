document.addEventListener("DOMContentLoaded", adv_search);

function adv_search(){
    const adv_form = document.getElementById('adv-form');
    const adv_board = document.querySelector('.adv-search');
    const btn_hide = document.getElementById('btn-hide')
    const btn_apply = document.getElementById('btn-apply');
    const btn_reset = document.getElementById('btn-reset');
    const adv_heading = document.querySelector('.header');
    // console.log(adv_heading);
   
    btn_hide.addEventListener('click', displayAdv);
    btn_apply.addEventListener('click', processForm);
    btn_reset.addEventListener('click', doReset);

    function doReset(event){
      event.preventDefault();
      window.location.assign('/reset_adv');
    }

    function processForm(event){
      event.preventDefault();
      adv_heading.style.color = 'lightgreen';
      // adv_heading.style.transition = 'all 1s';
      adv_form.submit();
    }

    function displayAdv(event){
      event.preventDefault();
      if (adv_board.classList.contains('adv-hide')){
        adv_board.classList.remove('adv-hide');
        adv_board.classList.add('adv-show');
      } 
      else {
        adv_board.classList.remove('adv-show');
        adv_board.classList.add('adv-hide');
      }
    }
}

