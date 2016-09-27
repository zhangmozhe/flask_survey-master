var main=function() {
    $('.btn').click(function(){
        var post = $('.status-box').val();
        // $('<li>').text(post).prependTo('.posts');
        // $('.status-box').val('');
        $('.counter').text('360');
        $('.btn').addClass('disabled');
    })
    $('.status-box').keyup(function(){
        var postLength = $(this).val().length;
        characterLeft = 360 - postLength;
        $('.counter').text(characterLeft);
        if (characterLeft < 0)
        {
            $('.btn').addClass('disabled');
        }
        else if (characterLeft === 360)
        {
            $('.btn').addClass('disabled');
        }
        else
        {
            $('.btn').removeClass('disabled');
        }
    })
    $('.btn').addClass('disabled');
}

$(document).ready(main);