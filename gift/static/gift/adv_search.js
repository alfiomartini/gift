document.addEventListener("DOMContentLoaded", adv_search);

function adv_search(){
    const adv_form = document.getElementById('adv-form');
    const adv_board = document.querySelector('.adv-search');
    const btn_hide = document.getElementById('btn-hide')
    const btn_apply = document.getElementById('btn-apply');
    const btn_reset = document.getElementById('btn-reset');
    const adv_heading = document.querySelector('.header');
    
   
    btn_hide.addEventListener('click', displayAdv);
    btn_apply.addEventListener('click', processForm);
    btn_reset.addEventListener('click', doReset);

    const created = document.getElementById('created');
    created.max = new Date().toISOString().split("T")[0];
    updated = document.getElementById('updated');
    updated.max = new Date().toISOString().split("T")[0];

    function doReset(event){
      event.preventDefault();
      window.location.assign('/reset_adv');
    }

  
    function processForm(event){
      // event.preventDefault();
      
      const style = window.getComputedStyle(adv_heading);
      const old_color = style.getPropertyValue('color');
      adv_heading.style.color = 'lightgreen';
      setTimeout(() => {adv_heading.style.color = old_color;}, 600);
      
      // if (created.value < created.min || created.value > created.max){
      //   const modal = new Modal('');
      //   modal.show(`Range of date values: ${created.min} - ${created.max}`);
      // }
      // else if (updated.value < updated.min || updated.value > updated.max){
      //   const modal = new Modal('');
      //   modal.show(`Range of date values: ${created.min} - ${created.max}`);
      // }
      // else{
      //   adv_form.submit();
      // }
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

