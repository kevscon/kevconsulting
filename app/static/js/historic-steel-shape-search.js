
$(document).ready(function(){

  let edition_select = document.getElementById('edition');
  let shape_type_select = document.getElementById('shape_type');
  let shape_section_select = document.getElementById('shape_section');
  let shape_label_select = document.getElementById('shape_label');

  shape_type_select.onchange = function() {
    let edition = edition_select.value;
    let shape_type = shape_type_select.value;
    fetch('/' + edition + '/' + shape_type + '/historic-shape-sections').then(function(response) {
      response.json().then(function(data) {
          let optionHTML = '<option value=-1>--select section--</option>';
          for (let shape_section of data.shape_sections) {
            optionHTML += '<option value="' + shape_section + '">' + shape_section + '</option>';
          }
          shape_section_select.innerHTML = optionHTML;
      });
    });
  }

  shape_section_select.onchange = function() {
    let edition = edition_select.value;
    let shape_section = shape_section_select.value;
    fetch('/' + edition + '/' + shape_section + '/historic-shape-labels').then(function(response) {
      response.json().then(function(data) {
          let optionHTML = '<option value=-1>--select label--</option>';
          for (let shape_label of data.shape_labels) {
            optionHTML += '<option value="' + shape_label + '">' + shape_label + '</option>';
          }
          shape_label_select.innerHTML = optionHTML;
      });
    });
  }
  //
  // shape_designation_select.onchange = function() {
  //   let shape_section = shape_section_select.value;
  //   let shape_designation = shape_designation_select.value;
  //   fetch('/' + shape_section + '/' + shape_designation + '/shape-size').then(function(response) {
  //     response.json().then(function(data) {
  //         let optionHTML = '<option value=-1>--select size--</option>';
  //         for (let shape_label of data.shape_labels) {
  //           optionHTML += '<option value="' + shape_label + '">' + shape_label + '</option>';
  //         }
  //         shape_label_select.innerHTML = optionHTML;
  //     });
  //   });
  //
  // }
});
