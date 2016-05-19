$(".alert").delay(4000).slideUp(500, function() {
    $(this).alert('close');
});

$('.question-list > .question').click(function() {
  var question = $(this);
  var answers = $(this).next();
  if (answers.is(':visible')) {
    answers.slideUp();
    question.removeClass('active');
  } else {
    answers.slideDown();
    question.addClass('active');
  }
});