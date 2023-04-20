const prev_button = document.querySelector(".previous")
const next_button = document.querySelector(".next")
const start_quiz_button = document.querySelector(".start_quiz")

var page_index = 0;
if(page_index == 0){
    prev_button.classList.add("hide");
}
showText();
prev_button.onclick = ()=>{
    page_index = page_index - 1;
    if(page_index == 0){
        prev_button.classList.add("hide");
    }
    if(page_index < 5){
        next_button.classList.remove("hide");
    }
    showText();
}
next_button.onclick = ()=>{
    page_index = page_index + 1;
    if(page_index > 0){
        prev_button.classList.remove("hide");
    }
    if(page_index == 5){
        next_button.classList.add("hide");
        start_quiz_button.classList.remove("hide")
    }
    showText();
}


function showText(){
    const text = document.querySelector(".text");
    const page_num = document.querySelector(".page_number");
    let page_tag = '<span>' + texts[page_index].number_page + '</span>';
    let text_tag = '<span>' + texts[page_index].information + '</span>';
    page_num.innerHTML = page_tag;
    text.innerHTML = text_tag;
}