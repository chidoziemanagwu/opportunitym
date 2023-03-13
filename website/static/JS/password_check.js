$('input[name="password1"]').keyup(function(event) {
  var specialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/;
  console.log(specialChar)
  var input_text = $(this).val();
  $('p.Length-error').attr('hidden', false);
  $('p.Lowercase-error').attr('hidden', false);
  $('p.Uppercase-error').attr('hidden', false);
  $('p.Number-error').attr('hidden', false);
  $('p.SpecialChar-error').attr('hidden', false);

  if (input_text.length >= 8) {
    $('p.Length-error').attr('hidden', true);
  }
  for(var i = 0; i < input_text.length; i++){
    if(input_text.charAt(i).toLowerCase() != input_text.charAt(i).toUpperCase()){
        if (input_text.charAt(i) == input_text.charAt(i).toUpperCase()){
          $('p.Uppercase-error').attr('hidden', true);
        }
        if (input_text.charAt(i) == input_text.charAt(i).toLowerCase()){
          $('p.Lowercase-error').attr('hidden', true);
        }
    }
    if(input_text.charAt(i).match(/^[0-9]+$/) != null){
        $('p.Number-error').attr('hidden', true);
    }
    if(specialChar.test(input_text.charAt(i))){
        $('p.SpecialChar-error').attr('hidden', true);
    }
  }
})

$('input[name="password2"]').keyup(function(event){
    $('p.Matching-error').attr('hidden', false);
    password1 = $('input[name="password1"]').val();
    if($(this).val() == password1){
        $('p.Matching-error').attr('hidden', true);
    }
})