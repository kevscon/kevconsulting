
$(document).ready(function(){

  let shape_section_select = document.getElementById('shape_section');
  let shape_designation_select = document.getElementById('shape_designation');
  let shape_label_select = document.getElementById('shape_label');

  shape_section_select.onchange = function() {
    let shape_section = shape_section_select.value;
    fetch('/' + shape_section + '/shape-designations').then(function(response) {
      response.json().then(function(data) {
          let optionHTML = '<option value=-1>--select designation--</option>';
          for (let shape_designation of data.shape_designations) {
            optionHTML += '<option value="' + shape_designation + '">' + shape_designation + '</option>';
          }
          shape_designation_select.innerHTML = optionHTML;
      });
    });
  }

  shape_designation_select.onchange = function() {
    let shape_section = shape_section_select.value;
    let shape_designation = shape_designation_select.value;
    fetch('/' + shape_section + '/' + shape_designation + '/shape-labels').then(function(response) {
      response.json().then(function(data) {
          let optionHTML = '<option value=-1>--select label--</option>';
          for (let shape_label of data.shape_labels) {
            optionHTML += '<option value="' + shape_label + '">' + shape_label + '</option>';
          }
          shape_label_select.innerHTML = optionHTML;
      });
    });

  }
});
