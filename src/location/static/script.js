$(document).ready(function() {

  $("#searchMap").click(function() {
    var searchReq = $.get("/sendRequestMap/" + $("#query").val());
    searchReq.done(function(data) {
      $("#image").html(data);
    });
  });

  $("#searchPhoto").click(function() {
    var searchReq = $.get("/sendRequestPhoto/" + $("#query").val());
    searchReq.done(function(data) {
      $("#image").html(data);
    });
  });
});