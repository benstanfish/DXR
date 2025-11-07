switches = Array(
    "notes-toggle-switch",
    "nte-toggle-switch",
    "npr-toggle-switch",
    "brackets-toggle-switch",
    "add-toggle-switch",
    "del-toggle-switch",
    "add-color-toggle-switch",
    "del-color-toggle-switch",
    "show-deletions-toggle-switch",
    "eng-toggle-switch",
    "met-toggle-switch",
    "rid-toggle-switch",
    "rtl-toggle-switch",
    "color-rid-toggle-switch",
    "color-rtl-toggle-switch",
    "srf-toggle-switch",
    "stl-toggle-switch",
    "color-srf-toggle-switch",
    "color-stl-toggle-switch",
    "sub-toggle-switch",
    "color-sub-toggle-switch",
    "toggle_all"
)


set_up_toggle_by_class('nte-toggle-switch', '.display_NTE');
set_up_toggle_by_class('npr-toggle-switch', '.display_NPR');
set_up_toggle_by_class('add-toggle-switch', '.display_ADD');
set_up_toggle_by_class('del-toggle-switch', '.display_DEL');

set_up_toggle_by_class('eng-toggle-switch', '.display_ENG');
set_up_toggle_by_class('met-toggle-switch', '.display_MET');
set_up_toggle_by_class('rid-toggle-switch', '.display_RID');
set_up_toggle_by_class('rtl-toggle-switch', '.display_RTL');

set_up_toggle_by_class('srf-toggle-switch', '.display_SRF');
set_up_toggle_by_class('stl-toggle-switch', '.display_STL');
set_up_toggle_by_class('sub-toggle-switch', '.display_SUB', 'inline');

toggle_bracket_style('brackets-toggle-switch', '.brackets')

set_up_toggle_by_tag('notes-toggle-switch', 'HDR');
set_up_toggle_by_tag('notes-toggle-switch', 'NTE');
set_up_toggle_by_tag('notes-toggle-switch', 'NPR');
set_up_toggle_by_tag('notes-toggle-switch', 'AST');
set_up_toggle_by_tag('show-deletions-toggle-switch', 'DEL')

toggle_color_style('add-color-toggle-switch', 'add', 'var(--add-color)')
toggle_color_style('del-color-toggle-switch', 'del', 'var(--del-color)')

toggle_color_style('color-rid-toggle-switch', 'rid', 'var(--rid-color)', 'var(--rid-bg')
toggle_color_style('color-rtl-toggle-switch', 'rtl', 'var(--rtl-color)', 'var(--rtl-bg)')
toggle_color_style('color-srf-toggle-switch', 'srf', 'var(--srf-color)', 'var(--srf-bg')

toggle_color_style('color-stl-toggle-switch', 'stl', 'var(--stl-color)', 'var(--stl-bg)')
toggle_color_style('color-sub-toggle-switch', 'sub', 'var(--sub-color)')


document.getElementById('notes-toggle-switch').checked = false;
document.getElementById('brackets-toggle-switch').checked = true;
document.getElementById('rid-toggle-switch').checked = false;
document.getElementById('del-color-toggle-switch').checked = true;
document.getElementById('show-deletions-toggle-switch').checked = false;
document.getElementById('color-rid-toggle-switch').checked = true;
document.getElementById('color-srf-toggle-switch').checked = true;
document.getElementById('color-sub-toggle-switch').checked = true;


function set_up_toggle_by_tag(toggle_element_id, target_elements_tag_name, display_style='inline') {
    let toggle_element = document.getElementById(toggle_element_id)
    let target_elements = document.querySelectorAll(target_elements_tag_name)
    toggle_element.addEventListener('change', () => {
        target_elements.forEach( item => {
            if (toggle_element.checked) {
                item.style.display = display_style;
            } else {
                item.style.display = 'none';
            }
        })
    })
}

function set_up_toggle_by_class(toggle_element_id, target_elements_class_name, display_style='inline') {
    let toggle_element = document.getElementById(toggle_element_id)
    let target_elements = document.querySelectorAll(target_elements_class_name)
    toggle_element.addEventListener('change', () => {
        target_elements.forEach( item => {
            if (toggle_element.checked) {
                item.style.display = display_style;
            } else {
                item.style.display = 'none';
            }
        })
    })
}

function toggle_bracket_style(toggle_element_id, target_elements_class_name) {
    let toggle_element = document.getElementById(toggle_element_id)
    let target_elements = document.querySelectorAll(target_elements_class_name)
    toggle_element.addEventListener('change', () => {
        target_elements.forEach( item => {
            if (toggle_element.checked) {
                item.style.backgroundColor = 'yellow';
            } else {
                item.style.backgroundColor = 'transparent';
            }
        })
    })
}

function toggle_color_style(toggle_element_id, target_elements_class_name, custom_color, custom_bg_color='') {
    let toggle_element = document.getElementById(toggle_element_id)
    let target_elements = document.querySelectorAll(target_elements_class_name)
    toggle_element.addEventListener('change', () => {
        target_elements.forEach( item => {
            if (toggle_element.checked) {
                item.style.color = custom_color;
                if (custom_bg_color.length != 0) {
                    item.style.backgroundColor = custom_bg_color
                }
            } else {
                item.style.color = 'var(--standard-text-color)';
                item.style.backgroundColor = 'transparent';
            }
        })
    })
}


function toggle_all_tags(toggle_element) {
    const all_display_tags = document.querySelectorAll('[class^="display_"]');
    toggle_element.addEventListener('change', () => {
        all_display_tags.forEach( item => {
            if (toggle_element.checked) {
                item.style.display = 'inline';
            } else {
                item.style.display = 'none';
            }
        })
    })
}


let topButton = document.getElementById("topBtn");
let menuButton = document.getElementById("menuBtn");
menuButton.onclick = function() {toggleMenu()};

let toggleAllButton = document.getElementById("toggle-all-switch")
toggle_all_tags(toggleAllButton)


window.onscroll = function() {scrollFunction()};
function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    topButton.style.display = "block";
  } else {
    topButton.style.display = "none";
  }
}

let tocButton = document.getElementById("indexBtn");
tocButton.onclick = function() {tocFunction()};
function tocFunction() {
    window.location.href = 'index.html'
}

function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

function toggleMenu() {
    let menuElement = document.querySelector('.user-selections');
    let mainElement = document.querySelector('main');
    if (menuElement.style.display != 'block') {
        menuElement.style.display = 'block';
        mainElement.style.marginTop = '200px';
    } else {
        menuElement.style.display = 'none';
        mainElement.style.marginTop = '72px';
    }
}