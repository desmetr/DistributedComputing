$(document).ready(function() 
{

  $("#searchMap").click(function()
  {
    console.info("yes 1");
    var searchReq = $.get("/sendRequestMap/" + $("#query").val());
    searchReq.done(function(data) 
    {
      $("#googleResults").html(data);
    });
  });

  $("#searchPhoto").click(function()
  {
    console.info("yes 2");
    var searchReq = $.get("/sendRequestPhoto/" + $("#query").val());
    searchReq.done(function(data) 
    {
      $("#googleResults").html(data);
    });
  });
});